from core.cv_tools import read_cv_from_path

# read CV
raw_cv = read_cv_from_path("static/senior-software-developer.pdf")

print("\n\nNEXT SECTION\n\n".join([str(el) for el in raw_cv]))
