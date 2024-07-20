from core.cv_extractors import (
    extract_education,
    extract_commercial_experience,
    extract_social_profiles,
    extract_searchable_data,
)
from core.cv_tools import read_cv_from_path

# read CV
raw_cv = read_cv_from_path("static/senior-software-developer.pdf")

print("\n\n".join([str(el) for el in raw_cv]))

skills_sample = """skills _______________________________________________________________________________________________________________
hard skills: prioritization (advanced), looker (experienced), segment, amplitude, user documentation. techniques: jira, pendo, rubicon (advanced), doubleclick, liverail, visio, javascript, html, codeigniter
"""

education_sample = """education _______________________________________________________________________________________________________________
resume worded university, new york, ny master of science — computer science
06/2005
"""

professional_sample = """work experience _______________________________________________________________________________________________________________
senior software developer
handled 15 web applications utilized by 3m users to manage their 401(k) accounts within 45 days of employment
managed an infrastructure of 243 servers by providing services like patching, hardening, monitoring, and
backups. initiated documentation for rw's system architecture and deployment instructions; increased adoption rate by 59% among 5.5k employees. supervised a 15 man team of developers to create a navigational app that reached 10m downloads on the ﬁrst release day
polyhire, london, united kingdom nyse listed recruitment and employer branding company
12/2012 08/2015
"""

details_sample = """
first last senior software developer olympia, washington • +1 234 456 789 • professionalemail@resumeworded.com • linkedin.com/in/username
"""

print("\n\n\n---\n\n\n")

# extractors unit tests
print("education:")
print(extract_education(education_sample))
print("commercial experience:")
print(extract_commercial_experience(professional_sample))
print("social accounts:")
print(extract_social_profiles(details_sample))
print("other data:")
print(extract_searchable_data(skills_sample))
