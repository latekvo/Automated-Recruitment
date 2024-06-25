from sqlalchemy import String, TEXT, Integer, Boolean, create_engine, select, update
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship, DeclarativeBase

class Base(DeclarativeBase):
  pass

engine = create_engine()

def init_database():
  Base.metadata.create_all(bind=engine)