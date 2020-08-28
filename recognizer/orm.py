import datetime

from sqlalchemy import Column, ForeignKey, Date, Time
from sqlalchemy import Integer, BigInteger, Float, SmallInteger, Boolean, String, Text
from sqlalchemy.dialects.postgresql import INET, TIMESTAMP

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from recognizer.helpers import set_bit, get_bit

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
    # date_time = Column(TIMESTAMP)
    date = Column(Date)
    time = Column(Time)
    phone_number = Column(BigInteger)
    duration = Column(Float)
    transcription = Column(Text)
    stages = Column(Integer)  # Used as bit-map
    count_stages = Column(SmallInteger)  # To determinate on which stages stopped this call

    project_id = Column(Integer, ForeignKey("project.id"))
    project = relationship("Project", backref=backref('phone_calls'))

    server_id = Column(Integer, ForeignKey("server.id"))
    server = relationship("Server", backref=backref('phone_calls'))

    def __init__(self, date_time: datetime.datetime, stage_number: int, answer: bool,
                 phone_number: int, duration: float, transcription: str):

        self.date = date_time.date()
        self.time = date_time.time()
        self.set_stage(stage_number, answer)

        self.phone_number = phone_number
        self.duration = duration
        self.transcription = transcription

    def set_stage(self, stage_number: int, answer: bool):
        self.stages = set_bit(self.stages or 0, stage_number-1, int(answer))
        self.count_stages = max(self.count_stages or 0, stage_number)

    def get_stage(self, stage_number: int):
        value = get_bit(self.stages, stage_number - 1)
        if stage_number == 1:
            return bool(value)
        elif stage_number == 2:
            return ["Автоответчик", "Человек"][value]
        return

