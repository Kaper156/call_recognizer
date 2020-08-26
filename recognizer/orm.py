from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, BigInteger, Float, SmallInteger, Boolean, String, Text
from sqlalchemy.dialects.postgresql import INET, TIMESTAMP

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String(256))
    description = Column(Text)


class Server(Base):
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String(256))
    ip_address = Column(INET)
    description = Column(Text)


class PhoneCall(Base):
    __tablename__ = 'phone_call'
    id = Column(Integer, primary_key=True, autoincrement='auto')
    date_time = Column(TIMESTAMP)
    phone_number = Column(BigInteger)
    duration = Column(Float)
    transcription = Column(Text)

    project_id = Column(Integer, ForeignKey("project.id"))
    project = relationship("Project", backref=backref('phone_calls'))

    server_id = Column(Integer, ForeignKey("server.id"))
    server = relationship("Server", backref=backref('phone_calls'))


class Stage(Base):
    __tablename__ = 'stage'
    id = Column(Integer, primary_key=True, autoincrement='auto')
    step_number = Column(SmallInteger)
    answer = Column(Boolean)

    phone_call_id = Column(Integer, ForeignKey("phone_call.id"))
    phone_call = relationship("PhoneCall", backref=backref('stages'))
