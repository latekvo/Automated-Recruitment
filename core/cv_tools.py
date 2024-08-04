from __future__ import annotations

import os

from unstructured.partition.auto import partition
from unstructured.partition.utils.constants import PartitionStrategy
from unstructured.cleaners.core import group_broken_paragraphs
from unstructured.cleaners.core import clean

import jsonpickle

from core.cv_structures import StructuredCV

static_path = "static/"
cache_path = "cache/"


def read_cv_from_path(cv_path: str) -> list[str]:
    # convert cv into raw chunks of text
    elements = partition(
        filename=static_path + cv_path,
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


def read_structured_cv_from_path(cv_path: str) -> StructuredCV | None:
    try:
        file = open(cache_path + cv_path, "r")
        return jsonpickle.decode(file.read())
    except Exception:
        return None


def save_structured_cv_to_path(cv_path: str, structured_cv: StructuredCV):
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)

    serialized_cv = jsonpickle.encode(structured_cv)

    with open(cache_path + cv_path, "w") as text_file:
        print(serialized_cv, file=text_file)
