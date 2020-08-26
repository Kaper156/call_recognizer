from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from recognizer.orm import Base, Project, Server, PhoneCall, Stage


class DatabaseController:
    def __init__(self, host, port, database, user, password):
        # Skip SQLAlchemy warnings
        import warnings
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        self.engine = create_engine(f'postgres://{user}:{password}@{host}:{port}/{database}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.cur_session = self.Session()

    def get_or_create(self, model, field_with_values):
        # Try find instance by all fields in table
        inst = self.cur_session.query(model).filter_by(**field_with_values).first()
        if not inst:
            # Instance not exist, insert it
            inst = model(**field_with_values)
            self.cur_session.add(inst)
        return inst

    def save_call_data(self, date_time,
                       stage, result,
                       phone_number,
                       duration, transcription,
                       project_name="Тестовое",
                       server_name="Тестовый сервер", server_ip="127.0.0.1"):

        _project = self.get_or_create(Project, {
            'name': project_name
        })
        _server = self.get_or_create(Server, {
            'name': server_name,
            'ip_address': server_ip,
        })

        # Save project and server
        self.cur_session.commit()

        # Insert or get phone call
        _phone_call = self.get_or_create(PhoneCall, {
            'date_time': date_time,
            'phone_number': phone_number,
            'duration': duration,
            'transcription': transcription,
        })

        # Add fk to it and save
        _project.phone_calls.append(_phone_call)
        _server.phone_calls.append(_phone_call)
        self.cur_session.commit()

        #
        _stage = self.get_or_create(Stage, {
            'phone_call_id': _phone_call.id,
            'step_number': stage,
            'answer': bool(result)
        })

        self.cur_session.commit()

    def __clear_db__(self):
        Base.metadata.drop_all(bind=self.engine)

    def __del__(self):
        self.Session.close_all()
