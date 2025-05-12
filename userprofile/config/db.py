from sqlalchemy.engine import create_engine, Engine
from dotenv import load_dotenv, get_key
from pydantic_core import MultiHostUrl
from pydantic import PostgresDsn
from sqlalchemy.orm import Session

class DBConnectionMetaClass(type):
    """
    Meta Class: 
    An implementation of singleton class is carried out here.
    """
    _instance = {}
    def __call__(self, *args, **kwds):
        if self not in DBConnectionMetaClass._instance:
            DBConnectionMetaClass._instance[self] = super().__call__(*args, **kwds)
        
        return DBConnectionMetaClass._instance[self]
        

class DBConnection(metaclass=DBConnectionMetaClass):
    def __init__(self):
        load_dotenv()
        self.db_port = int(get_key('.env', 'DB_PORT'))
        self.db_username = get_key('.env', 'DB_USER')
        self.db_password = get_key('.env', 'DB_PASSWORD')
        self.db_host = get_key('.env', 'DB_HOST')
        self.db_path = get_key('.env', 'DB_NAME')

    def get_db_connection_url(self) -> PostgresDsn:
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