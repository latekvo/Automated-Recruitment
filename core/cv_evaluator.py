from dataclasses import dataclass
from unstructured.partition.auto import partition
from unstructured.partition.utils.constants import PartitionStrategy


# Data of each candidate:
#     - most the details are on the CV
#     - related technologies and their relation to them
#     - experience level in multiple areas
#     - work, project and school history
#     - other logistic data
# fill in as many blanks as possible
# save to the existing applicant data database


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


def back_propagate_project(cv: StructuredCV, project: ExtractedProject):
    # extract data from private projects to fill additional cv data fields
    pass


def back_propagate_degree(cv: StructuredCV, institution: ExtractedInstitution, degree: ExtractedDegree):
    # extract data from educational institution to fill additional cv data fields
    pass


def back_propagate_role(cv: StructuredCV, workplace: ExtractedWorkplace, role: ExtractedRole):
    # extract data from professional experience to fill additional cv data fields
    pass


def back_propagate_social_profile(cv: StructuredCV, social_profile: ExtractedWebsite):
    # extract data from socials to fill additional cv data fields
    pass


def back_propagate_website(cv: StructuredCV, website: ExtractedWebsite):
    # extract data from website to fill additional cv data fields
    pass


def back_propagate_other_searchable(cv: StructuredCV, website: ExtractedWebsite):
    # extract data from other POIs to fill additional cv data fields
    pass


def read_cv_from_file():
    # convert cv into a well-structured text blob
    pass


def read_cv_from_path(cv_path):
    # convert cv into a well-structured document
    elements = partition(filename=cv_path, content_type="application/pdf", strategy=PartitionStrategy.OCR_ONLY)
    print("\n\n".join([str(el) for el in elements]))


def split_cv():
    # extract all the covered points of interest and store them in a single blob
    pass


def section_classifier():
    # classify what kind of section the provided chunk of text is
    # input can be either education, project, experience etc
    pass


def evaluate_cv():
    # rate cv relevance to job description
    pass


def evaluate_cv_by_application_uuid(application_uuid: str):
    # rate cv relevance to job description - using application uuid
    pass
