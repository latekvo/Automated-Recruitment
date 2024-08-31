from core.cv_evaluator import score_cv_eligibility_verbose
from core.cv_interface import create_structured_cv_from_path
from core.cv_structures import CriteriaCV

evaluated_cv_name = "senior-software-developer.pdf"

structured_cv = create_structured_cv_from_path(evaluated_cv_name)

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

eligibility_output = score_cv_eligibility_verbose(structured_cv, cv_criteria)

print("--- IS ELIGIBLE ---")
print("is eligible:", eligibility_output.is_eligible)
print("reasoning:", eligibility_output.decision_explanation)
