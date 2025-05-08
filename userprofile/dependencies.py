from config.db import DBConnection
from sqlalchemy.orm import Session
from sqlalchemy import Engine

def get_db_session() -> Session:
    mydb = DBConnection()
    return mydb.create_session()

def get_db_engine() -> Engine:
    mydb = DBConnection()
    return mydb.get_engine()