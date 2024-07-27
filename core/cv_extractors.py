from langchain_core.prompts import ChatPromptTemplate

from core.cv_structures import (
    ExtractedProject,
    ExtractedDegree,
    ExtractedRole,
    ExtractedWebsite,
    ExtractedSocialProfile,
    ExtractedOtherSearchable,
)
from core.llm_loader import get_llm

extraction_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are data extractor. "
            "You are provided with distinct sections of CVs, "
            "you are to extract the specified data out of them. "
            "You are provided with a clear task and topic, "
            "your job is to strictly follow the instructions. ",
        ),
        (
            "user",
            "Current section: ```{section}``` Data: ```{data}```",
        ),
    ]
)

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
