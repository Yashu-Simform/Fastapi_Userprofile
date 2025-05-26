import pytz

tz = pytz.timezone('Asia/Kolkata')

env_mapping = {
    'DEVELOPMENT': '.env',
    'TESTING': '.env.test',
    'PRODUCTION': '.env.production'
}

stage_mappeing = {
    'DEVELOPMENT': '',
    'TESTING': 'TEST',
    'PRODUCTION': 'PROD'
}