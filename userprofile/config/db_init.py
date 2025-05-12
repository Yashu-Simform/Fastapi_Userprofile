from ..models.models import Base
from sqlalchemy import Engine

def create_db_tables(engine: Engine):
    Base.metadata.create_all(bind=engine)