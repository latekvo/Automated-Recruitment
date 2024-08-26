from __future__ import annotations

import json

from core.cv_extractors import extract_cv_entries, extracted_to_structured_cv
from core.cv_structures import StructuredCV
from core.cv_tools import (
    read_cv_from_path,
    save_structured_cv_to_path,
    structure_extension,
    cache_path,
)


def create_structured_cv_from_path(cv_path: str) -> StructuredCV | None:
    try:
        try:
            with open(cache_path + cv_path + structure_extension, "r") as file:
                # load cached
                deserialized_cv = json.loads(file.read())
                loaded_cv = StructuredCV().load(deserialized_cv)
        except FileNotFoundError:
            loaded_cv = None

        if loaded_cv is not None:
            return loaded_cv

        # calculate CV
        raw_cv = read_cv_from_path(cv_path)
        raw_text = "\n".join(raw_cv)

        extracted_entries = extract_cv_entries(raw_text)
        print("--- EXTRACTED ENTRIES ---")
        print(extracted_entries)

        structured_cv = extracted_to_structured_cv(extracted_entries)

        save_structured_cv_to_path(cv_path, structured_cv)
    except Exception:
        return None
