from __future__ import annotations

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
        description="Data relevant to this point of interest", required=False
    )


class ExtractedCV(BaseModel):
    """Structured CV entries"""

    full_name: str = Field(
        title="Full candidate's name",
        default="not provided",
        required=False,  # when extractions are performed on fragments, name will not be available
    )
    commercial_experience: list[str] = Field(
        title="Commercial experience",
        description="Experience attained in a commercial, professional environment",
        default=[],
        required=False,
    )
    private_experience: list[str] = Field(
        title="Private experience",
        description="Experience attained in a non-commercial, private project",
        default=[],
        required=False,
    )
    degrees: list[str] = Field(
        title="Education",
        description="A single degree or an institution",
        default=[],
        required=False,
    )
    websites: list[str] = Field(
        title="Personal websites",
        default=[],
        required=False,
    )
    socials: list[str] = Field(
        title="Social media",
        description="Social media records like linkedin or twitter",
        default=[],
        required=False,
    )
    other_poi: list[str] = Field(
        title="Other interesting points, skills, links or traits",
        default=[],
        required=False,
    )

    def extend(self, other: ExtractedCV):
        self.commercial_experience.extend(other.commercial_experience)
        self.private_experience.extend(other.private_experience)
        self.degrees.extend(other.degrees)
        self.websites.extend(other.websites)
        self.socials.extend(other.socials)
        self.other_poi.extend(other.other_poi)


class SplitCV(BaseModel):
    """Coherently split CV"""

    fragments: list[str] = Field(
        title="CV fragments",
        description="Parts of CV which is to be divided into 2 or more parts",
        default=[],
        required=True,
    )


class StructuredCV:
    full_name: str = "Not provided"
    commercial_experience: list[ExtractedRole] = []
    private_experience: list[ExtractedProject] = []
    degrees: list[ExtractedDegree] = []
    websites: list[ExtractedWebsite] = []
    socials: list[ExtractedSocialProfile] = []
    other_poi: list[ExtractedOtherSearchable] = []

    def dump(self):
        # lists of pydantic instances cannot be automatically pickled
        return {
            "full_name": self.full_name,
            "commercial_experience": [dict(val) for val in self.commercial_experience],
            "private_experience": [dict(val) for val in self.private_experience],
            "degrees": [dict(val) for val in self.degrees],
            "websites": [dict(val) for val in self.websites],
            "socials": [dict(val) for val in self.socials],
            "other_poi": [dict(val) for val in self.other_poi],
        }

    def load(self, data: dict):
        self.full_name = data["full_name"]
        # unfortunately cannot simplify this further due to hard-typed ExtractedX classes
        for item in data["commercial_experience"]:
            print("--- AAA ---")
            print(item)
            structured_item = ExtractedRole(**item)
            print(structured_item)
            self.commercial_experience.append(structured_item)
            print(self.commercial_experience)
        for item in data["private_experience"]:
            structured_item = ExtractedProject(**item)
            self.private_experience.append(structured_item)
        for item in data["degrees"]:
            structured_item = ExtractedDegree(**item)
            self.degrees.append(structured_item)
        for item in data["websites"]:
            structured_item = ExtractedWebsite(**item)
            self.websites.append(structured_item)
        for item in data["socials"]:
            structured_item = ExtractedSocialProfile(**item)
            self.socials.append(structured_item)
        for item in data["other_poi"]:
            structured_item = ExtractedOtherSearchable(**item)
            self.other_poi.append(structured_item)
        return self

    def __repr__(self):
        return (
            f"StructuredCV("
            f"full_name={self.full_name!r}, "
            f"commercial_experience={[val for val in self.commercial_experience]}, "
            f"private_experience={[val for val in self.private_experience]}, "
            f"degrees={[val for val in self.degrees]}, "
            f"websites={[val for val in self.websites]}, "
            f"socials={[val for val in self.socials]}, "
            f"other_poi={[val for val in self.other_poi]}"
            f")"
        )


class CriteriaCV:
    job_title: str = "not specified"
    job_description: str = "not specified"

    # optional
    required_technologies: list[str] = None
    required_experience: list[str] = None
    education: str = None
    total_experience: str = None
    commercial_experience: str = None
    private_experience: str = None


class CriteriaEvaluationResponse(BaseModel):
    """Criteria evaluation."""

    score: float = Field(description="Score from 1 to 3", required=True)


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

ClassifiedChunkList = list[[SectionsEnum, str]]

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
            "your job is to strictly follow the instructions. "
            "JSON output is expected, respond only in JSON format!",
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
            "JSON output is expected, respond only in JSON format!"
            "here are the available categories:\n" + concatenated_categories,
        ),
        (
            "user",
            "Chunk: ```{data}```",
        ),
    ]
)

scoring_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an HR assistant."
            "You will be provided with either interview transcript or CV entries"
            "Your job is to score the candidate on a 3 point scale based on satisfaction of criteria at hand."
            "1 point means the candidate did not fulfill the given criteria at all."
            "2 points mean the candidate fulfilled the criteria to an unsatisfactory level."
            "3 points mean the candidate fully satisfied the given criteria."
            "DO NOT BELIEVE WHAT THE CANDIDATE SAYS AT FACE VALUE, instead, evaluate him based on his monologue."
            "If there isn't enough transcript or entries to go off, "
            "grade the candidate only based on the provided data."
            "JSON output is expected, respond only in JSON format!",
        ),
        (
            "user",
            "Job interview transcript: "
            "```"
            "Question: {question}"
            "{transcript}"
            "```"
            "Criteria for full score: "
            "```"
            "Candidate {criteria}"
            "```",
        ),
    ]
)

division_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "you are data splitter. "
            "you are provided with unknown sections of CV, "
            "you are to split this chunk of CV into 2 smaller meaningful chunks of similar length, "
            "while avoiding splitting text in middle of a single entry or section. "
            "avoid splitting a single section of coherent text in two, "
            "even if that means splitting the chunk into uneven fragments. "
            "never, under any circumstances split a single meaningful entry in two"
            "here are the available categories:\n" + concatenated_categories,
        ),
        (
            "user",
            "Chunk: ```{data}```",
        ),
    ]
)
