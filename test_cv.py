from core.cv_extractors import extract_cv_entries, extracted_to_structured_cv
from core.cv_tools import (
    read_cv_from_path,
    save_structured_cv_to_path,
    read_structured_cv_from_path,
)

evaluated_cv_name = "senior-software-developer.pdf"

structured_cv = read_structured_cv_from_path(evaluated_cv_name)

if structured_cv is None:
    # read CV
    raw_cv = read_cv_from_path(evaluated_cv_name)
    raw_text = "\n".join(raw_cv)

    extracted_entries = extract_cv_entries(raw_text)
    print("--- EXTRACTED ENTRIES ---")
    print(extracted_entries)

    structured_cv = extracted_to_structured_cv(extracted_entries)

    save_structured_cv_to_path(evaluated_cv_name, structured_cv)

print("--- STRUCTURED ENTRIES ---")
print(structured_cv)
