from core.cv_structures import (
    StructuredCV,
    CriteriaCV,
    EligibilityEvaluationResponse,
    eligibility_prompt,
    VerboseEligibilityEvaluationResponse,
)
from core.llm_loader import get_llm
from core.utils import ensure_workflow_output

functional_llm = get_llm()


def score_cv_eligibility(
    evaluated_cv: StructuredCV, criteria: CriteriaCV
) -> EligibilityEvaluationResponse:
    # used for initial filtering, a lot faster than the multi-shot scoring function
    cv_text = repr(evaluated_cv)
    criteria_text = criteria.get_text_representation()

    structured_llm = functional_llm.with_structured_output(
        EligibilityEvaluationResponse
    )
    workflow = eligibility_prompt | structured_llm

    return ensure_workflow_output(
        workflow, {"candidate": cv_text, "criteria": criteria_text}
    )


def score_cv_eligibility_verbose(
    evaluated_cv: StructuredCV, criteria: CriteriaCV
) -> VerboseEligibilityEvaluationResponse:
    # used for initial filtering, a lot faster than the multi-shot scoring function
    cv_text = repr(evaluated_cv)
    criteria_text = criteria.get_text_representation()

    structured_llm = functional_llm.with_structured_output(
        VerboseEligibilityEvaluationResponse
    )
    workflow = eligibility_prompt | structured_llm

    return ensure_workflow_output(
        workflow, {"candidate": cv_text, "criteria": criteria_text}
    )


def score_cv_by_criteria(evaluated_cv: StructuredCV, criteria: CriteriaCV) -> float:
    pass
