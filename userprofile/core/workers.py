from celery import Celery
from dotenv import load_dotenv, get_key

celery = Celery(__name__)
load_dotenv()

CELERY_BROKER_URL = get_key('.env', 'CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = get_key('.env', 'CELERY_RESULT_BACKEND')

celery.conf.broker_url = CELERY_BROKER_URL if CELERY_BROKER_URL else 'redis://127.0.0.1:6379/0'
celery.conf.result_backend = CELERY_RESULT_BACKEND if CELERY_RESULT_BACKEND else 'redis://127.0.0.1:6379/0'

@celery.task
def send_email():
    pass