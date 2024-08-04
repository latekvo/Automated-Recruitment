from langchain_core.output_parsers import StrOutputParser

from core.cv_structures import CriteriaEvaluationResponse, scoring_prompt
from core.llm_loader import get_llm


# Candidate [description, weighted importance]
# description rated 1-3, multiplied by importance
# fixme make structured
criteria_list = [
    ["answered the question", 10],
    ["provided meaningful monologue", 10],
    ["has high communication skills", 8],
    ["talked in depth about the question", 5],
    ["presented real life examples for this quesiton", 5],
]


functional_llm = get_llm()
output_parser = StrOutputParser()
criteria_llm = functional_llm.with_structured_output(CriteriaEvaluationResponse)


def normalize_score(score, min_ai_range=1, max_ai_range=3):
    # criteria_weights * ai_scoring_extremes -> 0 to 1 float range
    total_weights = 0
    for criteria in criteria_list:
        total_weights += criteria[1]

    adjusted_min_range = min_ai_range * total_weights
    adjusted_max_range = max_ai_range * total_weights

    return (score - adjusted_min_range) / adjusted_max_range


def score_interview_by_criteria(question, transcript, criteria):
    try:
        return (scoring_prompt | criteria_llm).invoke(
            {
                "question": question,
                "transcript": transcript,
                "criteria": criteria[0],
            }
        )
    except Exception:  # OutputParserException | ValueError
        # retry on error
        return score_interview_by_criteria(question, transcript, criteria)


def score_interview_criteria_completeness(question: str, transcript: str) -> float:
    total_score = 0
    for criteria in criteria_list:
        response = score_interview_by_criteria(question, transcript, criteria)
        total_score += response.score * criteria[1]

    return normalize_score(total_score)
