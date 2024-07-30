from typing import Literal, Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field


class ExtractedProject(BaseModel):
    """Extracted private non-commercial project."""

    title: str = Field(description="Project title", required=True)
    code_links: list[str] = Field(
        description="Links to project's codebase", required=False
    )
    social_links: list[str] = Field(
        description="Other links related to project", required=False
    )
    technologies: list[str] = Field(
        description="List of technologies used in this project", required=True
    )
    people: list[str] = Field(
        description="Other people collaborating on this project", required=False
    )


class ExtractedInstitution(BaseModel):
    """Extracted educational institution."""

    name: str = Field(
        description="Name of the educational institution (e.g. Massachusetts Institute of Technology)",
        required=True,
    )
    fields: list[str] = Field(
        description="General field of operations of this institution (IT, Private Equity, etc.)",
        required=True,
    )
    note: str = Field(
        description="Additional notes about this university (e.g. Top Polish university)",
        required=False,
    )


class ExtractedDegree(BaseModel):
    """Extracted college degree."""

    title: str = Field(
        description="Degree title (e.g. Master of AI Engineering)", required=True
    )
    field: str = Field(
        description="Field of degree (e.g. Civics engineering, Software Development)",
        required=True,
    )
    seniority: str = Field(
        description="Degree level (e.g. Bachelor, PhD, Doctorate)", required=True
    )


class ExtractedWorkplace(BaseModel):
    """Extracted workplace."""

    name: str = Field(description="Company's name", required=True)
    sector: str = Field(
        description="Company's area of operation (IT, Equity, etc.)", required=True
    )
    size: int = Field(description="Approximate company size", required=False)


class ExtractedRole(BaseModel):
    """Extracted job position and role."""

    title: str = Field(
        description="Job role title (e.g. Senior Software Engineer)", required=True
    )
    field: str = Field(
        description="Job field (e.g. Marketing, Research)", required=True
    )
    seniority: str = Field(
        description="Role seniority (e.g. Lead, Junior)", required=True
    )


class ExtractedSocialProfile(BaseModel):
    """Extracted social account."""

    # use to gather details
    full_url: str = Field(description="Entire extracted URL", required=True)


class ExtractedWebsite(BaseModel):
    """Extracted personal website."""

    # scan for technologies and originality
    url: str = Field(description="Website's full url", required=True)
    is_owner: bool = Field(description="Is this a personal website?", required=False)


class ExtractedOtherSearchable(BaseModel):
    """Other extracted data which could be useful."""

    title: str = Field(description="Point of interest title", required=True)
    data: list[str] = Field(
        description="Data relevant to this point of interest", required=True
    )


class StructuredCV:
    full_name: str = "N/A"
    commercial_experience: list[ExtractedRole] = []
    private_experience: list[ExtractedProject] = []
    degrees: list[ExtractedDegree] = []
    websites: list[ExtractedWebsite] = []
    socials: list[ExtractedSocialProfile] = []
    other_poi: list[ExtractedOtherSearchable] = []


SectionsEnum = Optional[
    Literal[
        "private_details",
        "work",
        "project",
        "education",
        "websites",
        "socials",
        "other_poi",
    ]
]

available_categories = [
    "private_details",
    "work",
    "project",
    "education",
    "socials",
    "websites",
    "other_poi",
]

concatenated_categories = "\n".join(
    ["- " + category for category in available_categories]
)


extraction_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "you are data extractor. "
            "you are provided with distinct sections of CVs, "
            "you are to extract the specified data out of them. "
            "you are provided with a clear task and topic, "
            "your job is to strictly follow the instructions. ",
        ),
        (
            "user",
            "Current section: ```{section}``` Data: ```{data}```",
        ),
    ]
)

classification_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "you are data classifier. "
            "you are provided with unknown sections of CVs, "
            "you are to determine the category of those sections. "
            "your job is to strictly follow the instructions. "
            "here are the available categories:\n" + concatenated_categories,
        ),
        (
            "user",
            "Chunk: ```{data}```",
        ),
    ]
)
