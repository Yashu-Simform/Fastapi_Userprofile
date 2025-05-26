from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from .test_main import get_client
from ..config.db import DBConnection
from ..config.env_init import EnvConfig
import pytest


# Env config test
def test_env_config():
    envconfig = EnvConfig()
    assert envconfig.stage in ['DEVELOPMENT', 'TESTING', 'PRODUCTION']
    assert envconfig.get_env() is not None
    assert envconfig.stage == envconfig.get_envvar('STAGE')
    assert envconfig.stage == 'TESTING'

@pytest.fixture
def db_instance():
    return DBConnection()

@pytest.fixture
def db_session(db_instance):
    """Creates and yields a mock database session."""
    session = db_instance.create_session()
    yield session
    session.close()  # Ensure proper cleanup

def test_db_instance_singleton():
    inst1 = DBConnection()
    inst2 = DBConnection()

    assert inst1 is inst2

def test_db_connection_url():
    mydb = DBConnection()
    dburl = str(mydb.get_db_connection_url())
    assert dburl.startswith('postgresql+psycopg2://')

def test_db_engine(db_instance):
    inst1 = db_instance.get_engine()
    inst2 = db_instance.get_engine()
    
    assert inst1 is inst2   # Engine instances must be a single resource. 
    assert inst1 is not None    #Engine should not be None

def test_session_creation(db_session):
    assert isinstance(db_session, Session)
    assert db_session.is_active