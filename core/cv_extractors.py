from core.cv_structures import (
    ExtractedProject,
    ExtractedDegree,
    ExtractedRole,
    ExtractedWebsite,
    ExtractedSocialProfile,
    ExtractedOtherSearchable,
)


# Either:
# - ai regroups chunks of text into structured list jsons
# or
# - ai extracts single entries
#
# the former will be much easier to implement, as no need for entry splitting will be necessary

# in all of the following cases, text is guaranteed to provide the extraction goal


def extract_education(text: str) -> list[ExtractedDegree]:
    pass


def extract_commercial_experience(text: str) -> list[ExtractedRole]:
    pass


def extract_private_experience(text: str) -> list[ExtractedProject]:
    pass


def extract_websites(text: str) -> list[ExtractedWebsite]:
    pass


def extract_social_profiles(text: str) -> list[ExtractedSocialProfile]:
    pass


def extract_searchable_data(text: str) -> list[ExtractedOtherSearchable]:
    pass
