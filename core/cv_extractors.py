from core.cv_structures import (
    ExtractedProject,
    ExtractedDegree,
    ExtractedRole,
    ExtractedWebsite,
    ExtractedSocialProfile,
    ExtractedOtherSearchable,
    extraction_prompt,
    ClassifiedChunkList,
    SectionsEnum,
    ExtractedStructuredCV,
)
from core.llm_loader import get_llm

functional_llm = get_llm()

# Either:
# - ai regroups chunks of text into structured list jsons
# or
# - ai extracts single entries
#
# the former will be much easier to implement, as no need for entry splitting will be necessary

# in all of the following cases, text is guaranteed to provide the extraction goal


def extract_education(text: str) -> ExtractedDegree:
    structured_llm = functional_llm.with_structured_output(ExtractedDegree)
    workflow = extraction_prompt | structured_llm
    result = workflow.invoke({"data": text, "section": "education"})
    return result


def extract_commercial_experience(text: str) -> ExtractedRole:
    structured_llm = functional_llm.with_structured_output(ExtractedRole)
    workflow = extraction_prompt | structured_llm
    result = workflow.invoke({"data": text, "section": "commercial_experience"})
    return result


def extract_private_experience(text: str) -> ExtractedProject:
    structured_llm = functional_llm.with_structured_output(ExtractedProject)
    workflow = extraction_prompt | structured_llm
    result = workflow.invoke({"data": text, "section": "private_experience"})
    return result


def extract_websites(text: str) -> ExtractedWebsite:
    structured_llm = functional_llm.with_structured_output(ExtractedWebsite)
    workflow = extraction_prompt | structured_llm
    result = workflow.invoke({"data": text, "section": "websites"})
    return result


def extract_social_profiles(text: str) -> ExtractedSocialProfile:
    structured_llm = functional_llm.with_structured_output(ExtractedSocialProfile)
    workflow = extraction_prompt | structured_llm
    result = workflow.invoke({"data": text, "section": "social_profiles"})
    return result


def extract_searchable_data(text: str) -> ExtractedOtherSearchable:
    structured_llm = functional_llm.with_structured_output(ExtractedOtherSearchable)
    workflow = extraction_prompt | structured_llm
    result = workflow.invoke({"data": text, "section": "searchable_data"})
    return result


def extract_from_classified_list(classified_chunks: ClassifiedChunkList):
    converted_chunks: list[[SectionsEnum, any]] = []

    for chunk in classified_chunks:
        classification: SectionsEnum = chunk[0]
        raw_data: str = chunk[1]
        extracted_data = None

        if classification == "private_details":
            extracted_data = "N/A"
        elif classification == "work":
            extracted_data = extract_commercial_experience(raw_data)
        elif classification == "project":
            extracted_data = extract_private_experience(raw_data)
        elif classification == "education":
            extracted_data = extract_education(raw_data)
        elif classification == "socials":
            extracted_data = extract_social_profiles(raw_data)
        elif classification == "websites":
            extracted_data = extract_websites(raw_data)
        elif classification == "other_poi":
            extracted_data = extract_searchable_data(raw_data)

        converted_chunks.append([classification, extracted_data])

    return converted_chunks


def extract_entire_cv(raw_chunks: list[str]):
    text = "\n".join(raw_chunks)
    structured_llm = functional_llm.with_structured_output(ExtractedStructuredCV)
    workflow = extraction_prompt | structured_llm
    result = workflow.invoke({"data": text, "section": "searchable_data"})
    return result
