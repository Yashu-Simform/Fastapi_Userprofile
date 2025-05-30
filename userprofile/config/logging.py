from logging import Logger
from .env_init import env_config

logger = Logger('userprofile', level=int(env_config.get_envvar('DEV_LOG_LEVEL')))