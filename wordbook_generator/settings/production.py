from .base import *
import environ


env = environ.Env()
env.read_env('.env')

DEBUG = False

DATABASES = {
    'default': env.db()
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s] %(message)s プロセス=%(process)d スレッド=%(thread)d %(pathname)s:%(lineno)d'
        },
    },
    'handlers': {
        'production': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/wordbookge/app.log',
            'formatter': 'default'
        }
    },
    'loggers': {
        '': {
            'handlers': ['production'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['production'],
            'level': 'INFO',
            'propagate': False
        }
    }
}