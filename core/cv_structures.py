from dataclasses import dataclass


@dataclass
class ExtractedProject:
    # scan for originality, technologies and scope of project
    title: str
    code_links: list[str]
    social_links: list[str]
    technologies: list[str]
    people: list[str]


@dataclass
class ExtractedInstitution:
    # scan for technologies and broad quality
    # asking the latest flagship models directly with no further research
    # will yield good enough results for most recognized facilities
    name: str
    fields: list[str]
    note: str


@dataclass
class ExtractedDegree:
    title: str
    field: str
    seniority: str


@dataclass
class ExtractedWorkplace:
    # scan for technologies and area operand
    # asking the latest flagship models directly with no further research
    # will yield good enough results for most recognized employers
    name: str
    sector: str
    size: int  # estimated


@dataclass
class ExtractedRole:
    title: str
    field: str
    seniority: str


@dataclass
class ExtractedSocialProfile:
    # use to gather details
    full_url: str
    root_url: str


@dataclass
class ExtractedWebsite:
    # scan for technologies and originality
    full_url: str
    root_url: str
    is_owner: bool


@dataclass
class ExtractedOtherSearchable:
    # document other points of interest not yet covered by the algo
    title: str
    data: list[str]


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
