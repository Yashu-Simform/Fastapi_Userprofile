from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

templates = Jinja2Templates(directory='userprofile/templates/')

router = APIRouter(prefix='/templates', tags=['Templates'])

@router.get('/welcome-page')
def img_gallery(req: Request):
    return templates.TemplateResponse(req, 'template1.html')