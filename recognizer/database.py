import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from recognizer.orm import Base, Project, Server, PhoneCall


# TODO Check work
# import recognizer.logger

# TODO Make standalone function, rewrite controller with as context manager (__enter__, __exit__)
class DatabaseController:
    def __init__(self, host, port, database, user, password):
        # Skip SQLAlchemy warnings
        import warnings
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # Module logger
        logging.getLogger(__name__)

        connection_string = f'postgres://{user}:{password}@{host}:{port}/{database}'
        logging.debug(f"Try connect to DB with this parameters: {connection_string}")
        try:
            self.engine = create_engine(connection_string)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
        except SQLAlchemyError as exc:
            logging.exception(f"Error while connect to DB", exc_info=exc)
            # TODO check is raised after log?
            # raise exc

        self.cur_session = self.Session()

    def _save_to_db_(self, instance):
        self.cur_session.add(instance)
        self.cur_session.commit()

    def update_or_insert_phone_call(self, date_time, stage_number, answer, phone_number, duration, transcription,
                                    project_id: int, server_id: int, ):
        # Try get existed instance of Phone_call by date-time and phone number
        # (Because one phone can accept only one call at moment)
        existed_instance = self.cur_session.query(PhoneCall).filter_by(date=date_time.date(), time=date_time.time(),
                                                                       phone_number=phone_number).first()
        if existed_instance:
            # Phone call already exist, change his stage and save
            existed_instance.set_stage(stage_number, answer)
            self._save_to_db_(existed_instance)
            return

        # Phone call not exist in DB
        phone_call = PhoneCall(date_time, stage_number, answer, phone_number, duration, transcription)
        # Set phone_call relations
        project = self.cur_session.query(Project).get(project_id)
        if project is None:
            logging.exception(f"Project with ID:{project_id} not exist!")

            project = Project(name="TestProject")
            self._save_to_db_(project)

            # raise Exception()
        server = self.cur_session.query(Server).get(server_id)
        if server is None:
            logging.exception(f"Server with ID:{project_id} not exist!")

            server = Server(name="TestServer", ip_address="8.8.8.8")
            self._save_to_db_(server)

            # raise Exception()

        # Append call to project and server children
        project.phone_calls.append(phone_call)
        server.phone_calls.append(phone_call)

        # Commit project and server changes too
        self._save_to_db_(phone_call)

    def __clear_db__(self):
        Base.metadata.drop_all(bind=self.engine)

    def __del__(self):
        self.Session.close_all()
