from core.cv_structures import ClassifiedChunkList
from core.cv_tools import read_cv_from_path, classify_cv_chunks
from core.cv_extractors import extract_commercial_experience


# read CV
raw_cv = read_cv_from_path("static/senior-software-developer.pdf")

print("\n\n".join([str(el) for el in raw_cv]))

professional_sample = """work experience _______________________________________________________________________________________________________________
senior software developer
handled 15 web applications utilized by 3m users to manage their 401(k) accounts within 45 days of employment
managed an infrastructure of 243 servers by providing services like patching, hardening, monitoring, and
backups. initiated documentation for rw's system architecture and deployment instructions; increased adoption rate by 59% among 5.5k employees. supervised a 15 man team of developers to create a navigational app that reached 10m downloads on the ﬁrst release day
polyhire, london, united kingdom nyse listed recruitment and employer branding company
12/2012 08/2015
"""

print("commercial experience:")
print(extract_commercial_experience(professional_sample))

classified_cv_chunks: ClassifiedChunkList = classify_cv_chunks(raw_cv)

for chunk in classified_cv_chunks:
    print(chunk[0], "|", chunk[1])
