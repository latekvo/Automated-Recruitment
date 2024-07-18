from __future__ import annotations

from typing import Literal

from unstructured.partition.auto import partition
from unstructured.partition.utils.constants import PartitionStrategy
from unstructured.cleaners.core import group_broken_paragraphs
from unstructured.cleaners.core import clean

from core.cv_structures import StructuredCV


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


def detect_header() -> None | Literal["work", "education", "project"]:
    # check if chunk of text is a header or not
    pass


def verify_content_positioning() -> bool:
    # check if chunk of text belongs to the current section
    pass


def regroup_cv(text_chunks: list[str]) -> list[str]:
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
    raw_cv_chunks = read_cv_from_path(cv_path)
    grouped_chunks = regroup_cv(raw_cv_chunks)

    pass
