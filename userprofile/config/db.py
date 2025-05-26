from sqlalchemy.engine import create_engine, Engine
from pydantic_core import MultiHostUrl
from pydantic import PostgresDsn
from sqlalchemy.orm import Session
import os
from .env_init import EnvConfig
from ..core.metaclasses import SingletonMetaClass
        

class DBConnection(metaclass=SingletonMetaClass):
    def __init__(self):
        # self.db_port = int(os.getenv('DB_PORT'))
        # self.db_username = os.getenv('DB_USER')
        # self.db_password = os.getenv('DB_PASSWORD')
        # self.db_host = os.getenv('DB_HOST')
        # self.db_path = os.getenv('DB_NAME')
        env_config = EnvConfig()
        self.db_port = int(env_config.get_envvar('DB_PORT', default='5432'))
        self.db_username = env_config.get_envvar('DB_USER')
        self.db_password = env_config.get_envvar('DB_PASSWORD')
        self.db_host = env_config.get_envvar('DB_HOST')
        self.db_path = env_config.get_envvar('DB_NAME')

    def get_db_connection_url(self) -> PostgresDsn:
        print('------------curr db: ', self.db_path)
        return MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.db_username,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            path=self.db_path
        )

    def create_engine(self, p_db_url: str = None):
        if not (hasattr(self, "engine") and isinstance(self.engine, Engine)):
            if not p_db_url:
                p_db_url = str(self.get_db_connection_url())
            self.engine = create_engine(p_db_url, echo=True)
            print('Engine object is now available. Access it using "instance.engine".')
        else:
            print('Engine object is already created.')
    
    def get_engine(self) -> Engine:
        if hasattr(self, "engine") and self.engine and isinstance(self.engine, Engine):
            return self.engine
        else:
            print('Engine object was not available, so creating it ...')
            self.create_engine()
        return self.engine

    def create_session(self) -> Session:
        """
            Create a session object for the db and binds the created engine.
        """
        session = Session(bind=self.get_engine())
        return session