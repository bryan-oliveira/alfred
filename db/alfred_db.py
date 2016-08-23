from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config import engine

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=True)
    fullname = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    gender = Column(String(1), nullable=True)
    password = Column(String(15), nullable=False)

    allergies = relationship("Allergy", uselist=False, backref="user")


class Allergy(Base):
    __tablename__ = 'allergies'

    id = Column(Integer, primary_key=True)
    soy = Column(Boolean, nullable=False)
    milk = Column(Boolean, nullable=False)
    eggs = Column(Boolean, nullable=False)
    nuts = Column(Boolean, nullable=False)
    gluten = Column(Boolean, nullable=False)
    fish = Column(Boolean, nullable=False)
    sesame = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

# Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
Base.metadata.create_all(engine)
