import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, TimeoutError

from recognizer.orm import Base, Project, Server, PhoneCall

# Connect to logger
logger = logging.getLogger(__name__)


# Connection implement as context manager which return session
class DatabaseController(object):
    def __init__(self, connection_string):
        # Skip SQLAlchemy warnings
        import warnings
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        self.connection_string = connection_string

        logger.debug(f"Try connect to DB with this parameters: {self.connection_string}")

        try:
            self.engine = create_engine(self.connection_string)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
        except TimeoutError as exc:
            logger.exception(f"Timeout error while connect to DB", exc_info=exc)
            raise exc
        except SQLAlchemyError as exc:
            logger.exception(f"Error while connect to DB", exc_info=exc)
            raise exc

    def __enter__(self):
        session = self.Session(bind=self.engine)
        return session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.Session.close_all()

    # Used for tests
    def __clear_db__(self):
        Base.metadata.drop_all(bind=self.engine)


# Specified for Postgres DB controller
class PostgresDatabaseController(DatabaseController):
    def __init__(self, host, port, database, user, password):
        connection_string = f'postgres://{user}:{password}@{host}:{port}/{database}'
        super().__init__(connection_string)


# Procedure of insert new phone call or updating existed
def update_or_insert_phone_call(session, date_time, stage_number, answer, phone_number, duration, transcription,
                                project_name, server_name, server_ip):
    # Try get existed instance of Phone_call by date-time and phone number
    # (Because one phone can accept only one call at moment)
    logger.debug(f"Try find in DB PhoneCall with this parameters: date={date_time.date()}, time={date_time.time()}, "
                 f"phone_number={phone_number}")
    phone_call = session.query(PhoneCall).filter_by(date=date_time.date(), time=date_time.time(),
                                                    phone_number=phone_number).first()
    if phone_call:
        # Phone call already exist, change his stage and save
        logger.debug("Phone call found in DB, update stage.")
        phone_call.set_stage(stage_number, answer)
        session.add(phone_call)
        session.commit()
    else:
        # Phone call not exist in DB
        logger.debug("Phone call not with this parameters not exist. Record will be created")
        phone_call = PhoneCall(date_time, stage_number, answer, phone_number, duration, transcription)

    # Set phone_call relations
    project = session.query(Project).filter_by(name=project_name).first()
    if project is None:
        logging.debug(f"Project with name:{project_name} not exist. Record will be created")
        project = Project(name=project_name)
        session.add(project)
        session.commit()

    server = session.query(Server).filter_by(name=server_name, ip_address=server_ip).first()
    if server is None:
        logger.debug(f"Server with name:{server_name} and ip_address: {server_ip} not exist. "
                     "Record will be created")

        server = Server(name=server_name, ip_address=server_ip)
        session.add(server)
        session.commit()

    # Append call to project and server children
    logger.debug(f"Add phone call to project ({project_name})")
    project.phone_calls.append(phone_call)
    logger.debug(f"Add phone call to server ({server_name}, <{server_ip}>)")
    server.phone_calls.append(phone_call)

    # Commit project and server changes too
    session.add(phone_call)
    session.commit()
