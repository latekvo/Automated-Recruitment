from sqlalchemy import (
    ForeignKey,
    String,
    TEXT,
    Integer,
    Boolean,
    create_engine,
    select,
    update,
)
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship, DeclarativeBase


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

    transcription: Mapped[str] = mapped_column(TEXT())


engine = create_engine("sqlite://")
Base.metadata.create_all(bind=engine)
