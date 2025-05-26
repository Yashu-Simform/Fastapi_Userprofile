from fastapi import FastAPI, Request, Body, status
from .config.db import DBConnection
from contextlib import asynccontextmanager
from .config.db_init import create_db_tables
from .routes import user_profile_routes, admin_routes, static_file_routes, template_routes
from fastapi.staticfiles import StaticFiles

mydb = DBConnection()

@asynccontextmanager
async def lifespan(p_app: FastAPI):
    # Before the application starts
    create_db_tables(mydb.get_engine())
    yield

    # After the application ends 

app = FastAPI(
    title='User Profile Application',
    lifespan=lifespan,
)

@app.get('/', status_code=status.HTTP_200_OK)
def root_path():
    return 'Server is running ...'

app.include_router(admin_routes.router)
app.include_router(user_profile_routes.router)
app.include_router(template_routes.router)