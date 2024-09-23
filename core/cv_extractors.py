import math
from dataclasses import dataclass
from typing import TypeVar, Type

from pydantic import BaseModel

from core.cv_structures import (
    ExtractedProject,
    ExtractedDegree,
    ExtractedRole,
    ExtractedWebsite,
    ExtractedSocialProfile,
    ExtractedOtherSearchable,
    extraction_prompt,
    ExtractedCV,
    StructuredCV,
)
from core.llm_loader import get_llm
from core.utils import ensure_workflow_output

functional_llm = get_llm()

# During data extraction, retries are likely to only occur when the text input is malformed beyond being useful
TEXT_TO_STRUCTURE_RETRIES = 3
PydanticStructure = TypeVar(
    "PydanticStructure",
    ExtractedRole,
    ExtractedProject,
    ExtractedDegree,
    ExtractedSocialProfile,
    ExtractedWebsite,
    ExtractedOtherSearchable,
)


def text_to_structure(
    text: str, structure: Type[PydanticStructure], text_hint: str
) -> PydanticStructure:
    structured_llm = functional_llm.with_structured_output(structure)
    workflow = extraction_prompt | structured_llm
    return ensure_workflow_output(
        workflow,
        {"data": text, "hint": text_hint},
        TEXT_TO_STRUCTURE_RETRIES,
    )


@dataclass
class CVSection:
    name: str
    type: Type[PydanticStructure]


def extracted_to_structured_cv(extracted_cv: ExtractedCV) -> StructuredCV:
    structured_cv = StructuredCV()

    structured_cv.full_name = extracted_cv.full_name

    cv_intermediate_dict = structured_cv.dump()

    cv_sections = [
        CVSection("commercial_experience", ExtractedRole),
        CVSection("private_experience", ExtractedProject),
        CVSection("degrees", ExtractedDegree),
        CVSection("socials", ExtractedSocialProfile),
        CVSection("websites", ExtractedWebsite),
        CVSection("other_poi", ExtractedOtherSearchable),
    ]

    for section in cv_sections:
        for text in extracted_cv[section]:
            cv_intermediate_dict[section.name].append(
                text_to_structure(text, section.type, section.name)
            )

    return structured_cv.load(cv_intermediate_dict)


length_threshold = 2000


def divide_cv(text) -> list[str]:
    # non-LLM method is quicker and more reliable for now
    # structured_llm = functional_llm.with_structured_output(SplitCV)
    # workflow = division_prompt | structured_llm
    # fragments = ensure_workflow_output(workflow, {"data": text})

    parts = math.ceil(len(text) / length_threshold)
    fragment_length = len(text) // parts
    remainder = len(text) % parts

    fragments = []
    start = 0

    for i in range(parts):
        end = start + fragment_length + (1 if i < remainder else 0)
        fragments.append(text[start:end])
        start = end

    print("--- FRAGMENTS ---")
    print(fragments)
    return fragments


def extract_cv_entries(text: str) -> ExtractedCV:
    text_slices = divide_cv(text)

    structured_llm = functional_llm.with_structured_output(ExtractedCV)
    workflow = extraction_prompt | structured_llm

    extracted_cv = None

    for cv_slice in text_slices:
        cv_fragment = ensure_workflow_output(
            workflow, {"data": cv_slice, "section": "Entire Resume"}
        )
        print("--- FRAGMENT ---")
        print(cv_fragment)
        if extracted_cv is None:
            extracted_cv = cv_fragment
        else:
            extracted_cv.extend(cv_fragment)

    return extracted_cv
