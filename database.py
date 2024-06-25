from sqlalchemy import ForeignKey, String, TEXT, Integer, Boolean, create_engine, select, update
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship, DeclarativeBase

class Base(DeclarativeBase):
  pass

class Recruitment(Base):
  # single position to which you might recruit someone
  __tablename__ = "recruitment"

  uuid: Mapped[str] = mapped_column(primary_key=True)

class Platform(Base):
  # platform details on which a batch was deployed
  __tablename__ = "platform"

  uuid: Mapped[str] = mapped_column(primary_key=True)

  recruitment_uuid: Mapped[str] = mapped_column(ForeignKey("recruitment.uuid"))

class TechnicalTask(Base):
  # question with a coding task
  __tablename__ = "technical_task"

  uuid: Mapped[str] = mapped_column(primary_key=True)

  recruitment_uuid: Mapped[str] = mapped_column(ForeignKey("recruitment.uuid"))

class Task(Base):
  # question which may be given to a candidate
  __tablename__ = "task"

  uuid: Mapped[str] = mapped_column(primary_key=True)

  recruitment_uuid: Mapped[str] = mapped_column(ForeignKey("recruitment.uuid"))

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

class Submission(Base):
  # single sent answer to Task or TechnicalTask
  __tablename__ = "submission"

  uuid: Mapped[str] = mapped_column(primary_key=True)

  application_uuid: Mapped[str] = mapped_column(ForeignKey("application.uuid"))
  task_uuid: Mapped[str] = mapped_column(ForeignKey("task.uuid"))


engine = create_engine("sqlite://")
Base.metadata.create_all(bind=engine)
