from dataclasses import dataclass

from langchain_core.pydantic_v1 import BaseModel, Field


@dataclass
class ExtractedProject(BaseModel):
    # scan for originality, technologies and scope of project
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


@dataclass
class ExtractedInstitution(BaseModel):
    # scan for technologies and broad quality
    # asking the latest flagship models directly with no further research
    # will yield good enough results for most recognized facilities
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


@dataclass
class ExtractedDegree(BaseModel):
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


@dataclass
class ExtractedWorkplace(BaseModel):
    # scan for technologies and area operand
    # asking the latest flagship models directly with no further research
    # will yield good enough results for most recognized employers
    name: str = Field(description="Company's name", required=True)
    sector: str = Field(
        description="Company's area of operation (IT, Equity, etc.)", required=True
    )
    size: int = Field(description="Approximate company size", required=False)


@dataclass
class ExtractedRole(BaseModel):
    title: str = Field(
        description="Job role title (e.g. Senior Software Engineer)", required=True
    )
    field: str = Field(
        description="Job field (e.g. Marketing, Research)", required=True
    )
    seniority: str = Field(
        description="Role seniority (e.g. Lead, Junior)", required=True
    )


@dataclass
class ExtractedSocialProfile(BaseModel):
    # use to gather details
    full_url: str = Field(description="Entire extracted URL", required=True)


@dataclass
class ExtractedWebsite(BaseModel):
    # scan for technologies and originality
    url: str = Field(description="Website's full url", required=True)
    is_owner: bool = Field(description="Is this a personal website?", required=False)


@dataclass
class ExtractedOtherSearchable(BaseModel):
    # document other points of interest not yet covered by the algo
    title: str = Field(description="Point of interest title", required=True)
    data: list[str] = Field(
        description="Data relevant to this point of interest", required=True
    )


@dataclass
class StructuredCV:
    # a flattened dataset of the above data, complete with the original file, sources etc.
    full_name: str
    commercial_experience: list[ExtractedRole]
    private_experience: list[ExtractedProject]
    degrees: list[ExtractedDegree]
    websites: list[ExtractedWebsite]
    socials: list[ExtractedSocialProfile]
    other_poi: list[ExtractedOtherSearchable]
