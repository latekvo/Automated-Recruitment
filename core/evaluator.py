# introduce both shallow and deep evaluation,
# automatically distaptch additional stages in case of large candidate pool
#
# with enough data, we could use a RAG system to do initial evaluation
# as it is done in the medical field to convert symptoms into disease classification

from typing import Tuple

from core import interview_summarizer, interview_evaluator
from core.database import engine, Evaluation, Submission
from sqlalchemy import (
    insert,
    select,
)
from sqlalchemy.orm import Session
import core.utils as utils
from dataclasses import dataclass


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


def evaluate_submission_by_uuid(uuid: str) -> Tuple[str, float]:
    # evaluate individual submission
    submission_details = get_submission_details_by_uuid(uuid)
    submission_summary = interview_summarizer.generate_sub_summary(
        submission_details.question, submission_details.transcription
    )
    submission_score = interview_evaluator.score_interview_criteria_completeness(
        submission_details.question, submission_details.transcription
    )
    return submission_summary, submission_score


def evaluate_submission(question: str, transcript: str):
    submission_summary = interview_summarizer.generate_sub_summary(question, transcript)
    submission_score = interview_evaluator.score_interview_criteria_completeness(
        question, transcript
    )
    return submission_summary, submission_score


def evaluate_application(
    application_uuid: str, recruitment_uuid: str, add_to_db=True
) -> Tuple[str, float]:
    # evaluate each submission individually
    with Session(engine) as session:
        query = select(Submission).where(
            Submission.application_uuid == application_uuid
        )
        applications = list(session.scalars(query).all())
        all_summaries = []
        total_score = 0
        for application in applications:
            summary, score = evaluate_submission(
                application.task.question, application.transcription
            )
            all_summaries.append(summary)
            total_score += score

        entirety_summary = interview_summarizer.summarize_list_of_sub_summaries(
            all_summaries
        )
        score_average = total_score / len(applications)

        if add_to_db:
            new_uuid = utils.gen_uuid()
            new_evaluation = Evaluation(
                uuid=new_uuid,
                recruitment_uuid=recruitment_uuid,
                application_uuid=application_uuid,
                general_summary=entirety_summary,
                general_score=score_average,
            )
            session.add(new_evaluation)
            session.commit()

        return entirety_summary, score_average
