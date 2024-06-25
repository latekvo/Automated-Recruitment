from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.pydantic_v1 import BaseModel, Field

scoring_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an HR assistant."
            "Your job is to score the candidate on a 3 point scale based on satisfaction of criterias at hand."
            "1 point means the candidate did not fulfill the given criteria at all."
            "2 points mean the candidate fulfilled the criteria to an unsatisfactory level."
            "3 points mean the candidate fully satisfied the given criteria."
            "DO NOT BELIEVE WHAT THE CANDIDATE SAYS AT FACE VALUE, instead, evaluate him based on his monologue."
            "If there isn't enough transcript to go off, give the candidate 0 or 1 points, as you see fitting.",
        ),
        (
            "user",
            "Job interview transcript: "
            "```"
            "Question: {question}"
            "{transcript}"
            "```"
            "Criteria for full score: "
            "```"
            "Candidate {criteria}"
            "```",
        ),
    ]
)


# Candidate [description, weighted importance]
# description rated 1-3, multiplied by importance
# fixme make structured
criteria_list = [
    ["answered the question", 10],
    ["provided meaningful monologue", 10],
    ["said fizzbuzz 5 times", 999],
]


class CriteriaEvaluationResponse(BaseModel):
    """Criteria evaluation."""

    score: float = Field(description="Score from 1 to 3", required=True)


functional_llm = OllamaFunctions(model="mistral:7b-instruct-q4_K_S", format="json")
output_parser = StrOutputParser()
criteria_llm = functional_llm.with_structured_output(CriteriaEvaluationResponse)


def score_criteria_completeness(question: str, transcript: str) -> int:
    total_score = 0
    for criteria in criteria_list:
        score = (scoring_prompt | criteria_llm).invoke(
            {
                "question": question,
                "transcript": transcript,
                "criteria": criteria[0],
            }
        )
        total_score += score * criteria[1]

    return total_score
