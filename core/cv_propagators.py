from core.cv_structures import (
    StructuredCV,
    ExtractedProject,
    ExtractedInstitution,
    ExtractedDegree,
    ExtractedWorkplace,
    ExtractedRole,
    ExtractedWebsite,
    ExtractedSocialProfile,
    ExtractedOtherSearchable,
)


def back_propagate_project(cv: StructuredCV, project: ExtractedProject):
    # extract data from private projects to fill additional cv data fields
    pass


def back_propagate_degree(
    cv: StructuredCV, institution: ExtractedInstitution, degree: ExtractedDegree
):
    # extract data from educational institution to fill additional cv data fields
    pass


def back_propagate_role(
    cv: StructuredCV, workplace: ExtractedWorkplace, role: ExtractedRole
):
    # extract data from professional experience to fill additional cv data fields
    pass


def back_propagate_social_profile(
    cv: StructuredCV, social_profile: ExtractedSocialProfile
):
    # extract data from socials to fill additional cv data fields
    pass


def back_propagate_website(cv: StructuredCV, website: ExtractedWebsite):
    # extract data from website to fill additional cv data fields
    pass


def back_propagate_other_searchable(
    cv: StructuredCV, searchable: ExtractedOtherSearchable
):
    # extract data from other POIs to fill additional cv data fields
    pass
