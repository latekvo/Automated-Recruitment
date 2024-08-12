from core.cv_evaluator import score_cv_eligibility
from core.cv_extractors import extract_cv_entries, extracted_to_structured_cv
from core.cv_structures import CriteriaCV
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

cv_criteria = CriteriaCV()
cv_criteria.job_title = "Junior LLM Engineer."
cv_criteria.job_description = "We are seeking a Junior LLM Engineer to assist in developing and optimizing language models for various applications."
cv_criteria.required_technologies = ["Gemini API", "Python", "Langchain"]
cv_criteria.required_skills = ["Communication", "resourcefulness"]
cv_criteria.education = "min. IT or related batchelor"
cv_criteria.total_experience = "2 years of computer programming experience"
cv_criteria.commercial_experience = "none required"
cv_criteria.private_experience = "extensive project portfolio"

eligibility_output = score_cv_eligibility(structured_cv, cv_criteria)

print("--- IS ELIGIBLE ---")
print("is eligible:", eligibility_output.is_eligible)
print("reasoning:", eligibility_output.decision_explanation)
