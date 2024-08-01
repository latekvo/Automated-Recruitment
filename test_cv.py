from core.cv_extractors import extract_cv_entries
from core.cv_tools import read_cv_from_path


# read CV
raw_cv = read_cv_from_path("static/senior-software-developer.pdf")

print(extract_cv_entries(raw_cv))
