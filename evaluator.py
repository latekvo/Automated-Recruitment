# introduce both shallow and deep evaluation,
# automatically distaptch additional stages in case of large candidate pool
#
# with enough data, we could use a RAG system to do initial evaluation
# as it is done in the medical field to convert symptoms into disease classification

import __future__
from typing import Tuple

from database import engine, Evaluation, Submission
from sqlalchemy import (
    insert,
    select,
    update,
)
from sqlalchemy.orm import Session
import utils
from dataclasses import dataclass
import evaluator_criteria
import evaluator_general


def add_shallow_evaluation_to_db(submission_uuid: str, summary: str, score: int) -> str:
    new_uuid = utils.gen_uuid()
    with Session(engine) as session:
        insert(Evaluation).values(
            uuid=new_uuid,
            submission_uuid=submission_uuid,
            general_summary=summary,
            general_score=score,
        )
        session.commit()
        return new_uuid


@dataclass
class SubmissionDetails:
    transcription: str
    question: str


def get_submission_details_by_uuid(uuid: str) -> SubmissionDetails:
    with Session(engine) as session:
        query = select(Submission).where(Submission.uuid == uuid)
        submission = session.scalar(query)
        return SubmissionDetails(
            transcription=submission.transcription, question=submission.task.question
        )


def evaluate_submission(uuid: str) -> Tuple[str, float]:
    # evaluate individual submission
    submission_details = get_submission_details_by_uuid(uuid)
    submission_summary = evaluator_general.generate_general_summary(
        submission_details.question, submission_details.transcription
    )
    submission_score = evaluator_criteria.score_criteria_completeness(
        submission_details.question, submission_details.transcription
    )
    return submission_summary, submission_score


def evaluate_application(uuid: str):
    # evaluate each submission individually
    pass