from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles

router = APIRouter(prefix='/static')

# router.mount('/templates', StaticFiles(directory='.templates/', html=True), name='templates')