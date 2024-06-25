from database import Base

class Submission(Base):
  # single sent answer to Task or TechnicalTask
  pass

class PersonalData(Base):
  # CV, and required extracted data
  pass

class Application(Base):
  # applicant's work results
  pass

class Task(Base):
  # question which may be given to a candidate
  pass

class TechnicalTask(Base):
  # question with a coding task
  pass

class Recruitment(Base):
  # single position to which you might recruit someone
  pass

class Platform(Base):
  # platform details on which a batch was deployed
  pass

class RecruitmentBatch(Base):
  pass
