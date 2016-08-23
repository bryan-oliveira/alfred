from config import engine
from sqlalchemy.orm import sessionmaker
from db.alfred_db import Base
from sqlalchemy.orm import scoped_session

Base.metadata.bind = engine
session_factory = sessionmaker(bind=engine)


def get_session():
    return scoped_session(session_factory)
