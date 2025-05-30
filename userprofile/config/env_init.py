from decouple import Config, RepositoryEnv
from .constants import env_mapping, stage_mappeing
import os

class EnvConfig:
    
    def __init__(self):
        default_config = Config(RepositoryEnv('.env'))
        self.stage = default_config('STAGE', default='DEVELOPMENT')
        self.env_config = Config(RepositoryEnv(env_mapping.get(self.stage, '.env')))

    def get_env(self):
        return self.env_config
    
    def get_envvar(self, key: str, default=None):
        prefix = stage_mappeing.get(self.stage, 'DEV')
        value = self.env_config.get(f'{prefix}_{key}', default)
        return value
    
env_config = EnvConfig()