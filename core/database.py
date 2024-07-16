from dataclasses import dataclass
from sqlalchemy import (
    ForeignKey,
    String,
    TEXT,
    Integer,
    Boolean,
    create_engine,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship, DeclarativeBase
import core.utils as utils
from core.transcriber import get_text


class Base(DeclarativeBase):
    pass


class Recruitment(Base):
    # single position to which you might recruit someone
    __tablename__ = "recruitment"

    uuid: Mapped[str] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String())
    company: Mapped[str] = mapped_column(String())


class Platform(Base):
    # platform details on which a batch was deployed
    __tablename__ = "platform"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    recruitment_uuid: Mapped[str] = mapped_column(ForeignKey("recruitment.uuid"))

    name: Mapped[str] = mapped_column(String())
    url: Mapped[str] = mapped_column(String())


class TechnicalTask(Base):
    # question with a coding task
    __tablename__ = "technical_task"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    recruitment_uuid: Mapped[str] = mapped_column(ForeignKey("recruitment.uuid"))

    highlighting: Mapped[str] = mapped_column(String())
    question: Mapped[str] = mapped_column(String())
    template: Mapped[str] = mapped_column(String())  # use relation


class DynamicTask(Base):
    # given a theme, this task will create a new question based on the contents of applicants CV, and or prior answers
    # at least as many regular tasks as dynamic tasks as a fallback
    __tablename__ = "dynamic_task"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    recruitment_uuid: Mapped[str] = mapped_column(ForeignKey("recruitment.uuid"))

    theme: Mapped[str] = mapped_column(String())


class Task(Base):
    # question which may be given to a candidate
    __tablename__ = "task"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    recruitment_uuid: Mapped[str] = mapped_column(ForeignKey("recruitment.uuid"))

    question: Mapped[str] = mapped_column(String())


class PersonalData(Base):
    # CV, and required extracted data
    __tablename__ = "personal_data"

    uuid: Mapped[str] = mapped_column(primary_key=True)

    full_name: Mapped[str] = mapped_column(String())
    # find a way to store CV blobs efficiently
    # we want to store them before and after the analysis


class Application(Base):
    # applicant's work results
    __tablename__ = "application"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    recruitment_uuid: Mapped[str] = mapped_column(ForeignKey("recruitment.uuid"))
    personal_data_uuid: Mapped[str] = mapped_column(ForeignKey("personal_data.uuid"))
    personal_data = relationship("PersonalData")


class Evaluation(Base):
    # applicant's work results
    __tablename__ = "evaluation"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    recruitment_uuid: Mapped[str] = mapped_column(ForeignKey("recruitment.uuid"))
    application_uuid: Mapped[str] = mapped_column(ForeignKey("application.uuid"))
    application = relationship("Application")

    # there a couple of possible approaches
    # a. checklist score system [not flexible]
    # b. relative score system [very slow]
    # c. pivot point score [improvement over b]
    # I think it's the best if we use the following system:
    # 1: siftoff with #a
    # 2: deeper check by #a with thought process
    # 3: b for last candidates
    # Current system:
    # 1: score a weighted checklist and rank scores
    general_summary: Mapped[str] = mapped_column(TEXT(), default="N/A")
    general_score: Mapped[int] = mapped_column(Integer(), default=0)


class SubmissionDynamicTask(Base):
    # response to DynamicTask, generated individually
    __tablename__ = "submission_dynamic_task"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    application_uuid: Mapped[str] = mapped_column(ForeignKey("application.uuid"))
    task_uuid: Mapped[str] = mapped_column(ForeignKey("task.uuid"))

    question: Mapped[str] = mapped_column(String(), default="N/A")
    generated: Mapped[bool] = mapped_column(Boolean(), default=False)


class Submission(Base):
    # single sent answer to Task or TechnicalTask
    __tablename__ = "submission"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    application_uuid: Mapped[str] = mapped_column(ForeignKey("application.uuid"))
    task_uuid: Mapped[str] = mapped_column(ForeignKey("task.uuid"))
    task = relationship("Task")

    transcription: Mapped[str] = mapped_column(TEXT())


engine = create_engine("sqlite:///database.db")


def init_db():
    Base.metadata.create_all(bind=engine)


def add_recruitment(title, company="N/A"):
    new_uuid = utils.gen_uuid()
    with Session(engine) as session:
        new_recruitment = Recruitment(uuid=new_uuid, title=title, company=company)
        session.add(new_recruitment)
        session.commit()
    return new_uuid


def add_task(recruitment_uuid, question):
    new_uuid = utils.gen_uuid()
    with Session(engine) as session:
        new_task = Task(
            uuid=new_uuid, recruitment_uuid=recruitment_uuid, question=question
        )
        session.add(new_task)
        session.commit()
    return new_uuid


def add_application(recruitment_uuid: str, personal_data_uuid: str):
    new_uuid = utils.gen_uuid()
    with Session(engine) as session:
        new_application = Application(
            uuid=new_uuid,
            recruitment_uuid=recruitment_uuid,
            personal_data_uuid=personal_data_uuid,
        )
        session.add(new_application)
        session.commit()
    return new_uuid


def add_submission(
    application_uuid: str, task_uuid: str, filename: str = "./static/test.mov"
):
    new_uuid = utils.gen_uuid()
    with Session(engine) as session:
        new_submission = Submission(
            uuid=new_uuid,
            application_uuid=application_uuid,
            task_uuid=task_uuid,
            # todo: make into a worker transcribtion queue
            transcription=get_text(filename),
        )
        session.add(new_submission)
        session.commit()
    return new_uuid


def add_personal_data(full_name: str):
    new_uuid = utils.gen_uuid()
    with Session(engine) as session:
        newPersonalData = PersonalData(uuid=new_uuid, full_name=full_name)
        session.add(newPersonalData)
        session.commit()
    return new_uuid


@dataclass
class ApplicantPosition:
    score: float
    summary: str
    full_name: str
    application_uuid: str
    evaluation_uuid: str


def get_best_applicants(recruitment_uuid: str) -> list[ApplicantPosition]:
    with Session(engine) as session:
        session.expire_on_commit = False
        query = (
            select(Evaluation)
            .join(Evaluation.application)
            .where(Application.recruitment_uuid == recruitment_uuid)
            .order_by(Evaluation.general_score.desc())
            .limit(100)
        )

        top_evaluations = list(session.scalars(query).all())
        applicant_positions = []
        for evaluation in top_evaluations:
            applicant_positions.append(
                ApplicantPosition(
                    evaluation_uuid=evaluation.uuid,
                    application_uuid=evaluation.application_uuid,
                    full_name=evaluation.application.personal_data.full_name,
                    score=evaluation.general_score,
                    summary=evaluation.general_summary,
                )
            )

        session.expunge_all()

        return applicant_positions


def get_evaluation_by_uuid(application_uuid: str):
    with Session(engine) as session:
        session.expire_on_commit = False

        query = (
            select(Evaluation)
            .join(Evaluation.application)
            .where(Application.uuid == application_uuid)
        )

        result = session.scalars(query).one_or_none()

        session.expunge_all()

        return result

