import os

__RUNTIME_NAME__ = 'RUNTIME'
__ENVIRONMENT_NAME__ = 'ENVIRONMENT'
__DATABASE_URL_NAME__ = 'DATABASE_URL'

def is_docker():
        return os.environ.get('RUNTIME') or 'dev' == 'docker'

def is_prod():
    return os.environ.get('ENVIRONMENT') or 'dev' == 'production'

def db_url():
    if os.environ.get('ENVIRONMENT') == 'production' and os.environ.get('DATABASE_URL') is None:
        raise Exception('DATABASE_URL is not set')
    return os.environ.get('DATABASE_URL') or 'sqlite:///./sqlite.db'
