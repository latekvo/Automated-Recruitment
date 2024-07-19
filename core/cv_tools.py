from __future__ import annotations

from typing import Literal

from unstructured.partition.auto import partition
from unstructured.partition.utils.constants import PartitionStrategy
from unstructured.cleaners.core import group_broken_paragraphs
from unstructured.cleaners.core import clean

from core.cv_extractors import (
    extract_education,
    extract_commercial_experience,
    extract_private_experience,
    extract_searchable_data,
    extract_social_profiles,
    extract_websites,
)
from core.cv_structures import StructuredCV, SectionsEnum


def read_cv_from_file():
    # convert cv into a well-structured text blob
    pass


def read_cv_from_path(cv_path: str) -> list[str]:
    # convert cv into a well-structured document
    elements = partition(
        filename=cv_path,
        content_type="application/pdf",
        strategy=PartitionStrategy.HI_RES,
        paragraph_grouper=group_broken_paragraphs,
    )

    clean_elements = [
        clean(
            str(e),
            extra_whitespace=True,
            dashes=True,
            bullets=True,
            trailing_punctuation=True,
            lowercase=True,
        )
        for e in elements
    ]

    return clean_elements


def detect_header() -> SectionsEnum:
    # check if chunk of text is a header or not
    pass


def verify_content_positioning() -> bool:
    # check if chunk of text belongs to the current section
    pass


def regroup_cv(
    text_chunks: list[str],
) -> list[[SectionsEnum, str]]:
    # group extracted CV slices into better-organised fragments
    # coagulate chunks until a header is encountered
    # with each coagulation, also check if the text chunk belongs to the current section
    pass


# couple different approaches for section classification are feasible
# - use AI to split into large sections: EXPERIENCE, EDUCATION ETC
#   this would allow us to split the entire document by just detecting headers
#   we would then have to split the individual entries into each section
# - use AI to sort each individual entry into appropriate section
#   simpler, but likely more lossy, as less context is being used
# I'm going with the first one, but will see where it goes in the coming commits


def process_cv(cv_path: str) -> StructuredCV:
    extracted_cv = StructuredCV(
        full_name="N/A",
        commercial_experience=[],
        private_experience=[],
        degrees=[],
        socials=[],
        websites=[],
        other_poi=[],
    )

    raw_cv_chunks = read_cv_from_path(cv_path)
    grouped_chunks = regroup_cv(raw_cv_chunks)
    for chunk in grouped_chunks:
        section, text = chunk

        if section == "work":
            extracted_cv.commercial_experience += extract_commercial_experience(text)
        if section == "project":
            extracted_cv.private_experience += extract_private_experience(text)
        if section == "education":
            extracted_cv.degrees += extract_education(text)
        if section == "socials":
            extracted_cv.socials += extract_social_profiles(text)
        if section == "websites":
            extracted_cv.websites += extract_websites(text)
        if section == "other_poi":
            extracted_cv.other_poi += extract_searchable_data(text)

    return extracted_cv
