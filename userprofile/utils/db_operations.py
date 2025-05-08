from models import Base
from sqlalchemy import Engine
from fastapi import Depends
from typing import Annotated
from ..dependencies import get_db_engine

def create_db_or_tables(engine: Annotated[Engine, Depends(get_db_engine)]):
    Base.metadata.create_all(bind=engine)