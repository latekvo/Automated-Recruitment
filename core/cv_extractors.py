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

functional_llm = get_llm()


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


def extract_cv_entries(raw_chunks: list[str]):
    text = "\n".join(raw_chunks)
    structured_llm = functional_llm.with_structured_output(ExtractedCV)
    workflow = extraction_prompt | structured_llm
    result = workflow.invoke({"data": text, "section": "searchable_data"})
    return result
