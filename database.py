from sqlalchemy import (
    ForeignKey,
    String,
    TEXT,
    Integer,
    Boolean,
    create_engine,
    insert,
    select,
    update,
)
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship, DeclarativeBase
import utils
from transcriber import get_text


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


class Application(Base):
    # applicant's work results
    __tablename__ = "application"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    recruitment_uuid: Mapped[str] = mapped_column(ForeignKey("recruitment.uuid"))


class Evaluation(Base):
    # applicant's work results
    __tablename__ = "evaluation"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    recruitment_uuid: Mapped[str] = mapped_column(ForeignKey("dynamic_task.uuid"))

    # there a couple of possible approaches
    # a. checklist score system [not flexible]
    # b. relative score system [very slow]
    # c. pivot point score [improvement over b]
    # I think it's the best if we use the following system:
    # 1: siftoff with #1
    # 2: deeper check by #1 with thought process
    # 3: b for last candidates
    general_summary: Mapped[str] = mapped_column(TEXT())
    knowledge_summary: Mapped[str] = mapped_column(TEXT(), default="N/A")
    experience_summary: Mapped[str] = mapped_column(TEXT(), default="N/A")
    # scores better defined in evaluator.py prompts
    general_score: Mapped[int] = mapped_column(Integer(), default=0)


class PersonalData(Base):
    # CV, and required extracted data
    __tablename__ = "personal_data"

    uuid: Mapped[str] = mapped_column(primary_key=True)
    application_uuid: Mapped[str] = mapped_column(ForeignKey("application.uuid"))

    full_name: Mapped[str] = mapped_column(String())
    # find a way to store CV blobs efficiently
    # we want to store them before and after the analysis


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


engine = create_engine("sqlite://")
Base.metadata.create_all(bind=engine)


def add_recruitment(title, company="N/A"):
    new_uuid = utils.gen_uuid()
    with Session(engine) as session:
        insert(Task).values(uuid=new_uuid, title=title, company=company)
        session.commit()
    return new_uuid


def add_task(recruitment_uuid, question):
    new_uuid = utils.gen_uuid()
    with Session(engine) as session:
        insert(Task).values(
            uuid=new_uuid, recruitment_uuid=recruitment_uuid, question=question
        )
        session.commit()
    return new_uuid


def add_application(recruitment_uuid: str):
    new_uuid = utils.gen_uuid()
    with Session(engine) as session:
        insert(Application).values(uuid=new_uuid, recruitment_uuid=recruitment_uuid)
        session.commit()
    return new_uuid


def add_submission(
    application_uuid: str, task_uuid: str, filename: str = "./static/test.mov"
):
    new_uuid = utils.gen_uuid()
    with Session(engine) as session:
        insert(Submission).values(
            uuid=new_uuid,
            application_uuid=application_uuid,
            task_uuid=task_uuid,
            # todo: make into a worker transcribtion queue
            transcription=get_text(filename),
        )
        session.commit()
    return new_uuid
