from core.cv_extractors import extract_cv_entries, extracted_to_structured_cv
from core.cv_tools import read_cv_from_path


# read CV
raw_cv = read_cv_from_path("static/senior-software-developer.pdf")

extracted_entries = extract_cv_entries(raw_cv)
print("--- EXTRACTED ENTRIES ---")
print(extracted_entries)

structured_entries = extracted_to_structured_cv(extracted_entries)
print("--- STRUCTURED ENTRIES ---")
print(structured_entries)
