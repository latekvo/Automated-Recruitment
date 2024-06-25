# introduce both shallow and deep evaluation,
# automatically distaptch additional stages in case of large candidate pool
#
# with enough data, we could use a RAG system to do initial evaluation
# as it is done in the medical field to convert symptoms into disease classification

import __future__

from database import engine, Evaluation
from sqlalchemy import (
    insert,
    select,
    update,
)
from sqlalchemy.orm import Session
import utils


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


def evaluate_submission(uuid: str):
    pass


def evaluate_application(uuid: str):
    pass
