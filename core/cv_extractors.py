import math

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


def extract_education(text: str) -> ExtractedDegree:
    structured_llm = functional_llm.with_structured_output(ExtractedDegree)
    workflow = extraction_prompt | structured_llm
    return ensure_workflow_output(workflow, {"data": text, "section": "education"})


def extract_commercial_experience(text: str) -> ExtractedRole:
    structured_llm = functional_llm.with_structured_output(ExtractedRole)
    workflow = extraction_prompt | structured_llm
    return ensure_workflow_output(
        workflow, {"data": text, "section": "commercial_experience"}
    )


def extract_private_experience(text: str) -> ExtractedProject:
    structured_llm = functional_llm.with_structured_output(ExtractedProject)
    workflow = extraction_prompt | structured_llm
    return ensure_workflow_output(
        workflow, {"data": text, "section": "private_experience"}
    )


def extract_websites(text: str) -> ExtractedWebsite:
    structured_llm = functional_llm.with_structured_output(ExtractedWebsite)
    workflow = extraction_prompt | structured_llm
    return ensure_workflow_output(workflow, {"data": text, "section": "websites"})


def extract_social_profiles(text: str) -> ExtractedSocialProfile:
    structured_llm = functional_llm.with_structured_output(ExtractedSocialProfile)
    workflow = extraction_prompt | structured_llm
    return ensure_workflow_output(
        workflow, {"data": text, "section": "social_profiles"}
    )


def extract_searchable_data(text: str) -> ExtractedOtherSearchable:
    structured_llm = functional_llm.with_structured_output(ExtractedOtherSearchable)
    workflow = extraction_prompt | structured_llm
    return ensure_workflow_output(
        workflow, {"data": text, "section": "searchable_data"}
    )


def extracted_to_structured_cv(extracted_cv: ExtractedCV) -> StructuredCV:
    structured_cv = StructuredCV()

    structured_cv.full_name = extracted_cv.full_name

    for text in extracted_cv.commercial_experience:
        structured_cv.commercial_experience.append(extract_commercial_experience(text))

    for text in extracted_cv.private_experience:
        structured_cv.private_experience.append(extract_private_experience(text))

    for text in extracted_cv.degrees:
        structured_cv.degrees.append(extract_education(text))

    for text in extracted_cv.socials:
        structured_cv.socials.append(extract_social_profiles(text))

    for text in extracted_cv.websites:
        structured_cv.websites.append(extract_websites(text))

    for text in extracted_cv.other_poi:
        structured_cv.other_poi.append(extract_searchable_data(text))

    return structured_cv


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
            workflow, {"data": cv_slice, "section": "Entire CV"}
        )
        print("--- FRAGMENT ---")
        print(cv_fragment)
        if extracted_cv is None:
            extracted_cv = cv_fragment
        else:
            extracted_cv.extend(cv_fragment)

    return extracted_cv
