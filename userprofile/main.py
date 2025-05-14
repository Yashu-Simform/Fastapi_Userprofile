from fastapi import FastAPI
from .config.db import DBConnection
from contextlib import asynccontextmanager
from .config.db_init import create_db_tables
from .routes import user_profile_routes, admin_routes

mydb = DBConnection()

@asynccontextmanager
async def lifespan(p_app: FastAPI):
    # Before the application starts
    create_db_tables(mydb.get_engine())
    yield

    # After the application ends 

app = FastAPI(
    title='User Profile Application',
    lifespan=lifespan
)

app.include_router(admin_routes.router)
app.include_router(user_profile_routes.router)