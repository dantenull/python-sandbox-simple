import logging
import logging.config
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler


def setup_logging():
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
            'detail': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'default',
                'stream': 'ext://sys.stdout',
            },
            'detail_file': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'level': 'INFO',
                'formatter': 'detail',
                'filename': log_dir / 'app.log',
                'when': 'midnight',
                'backupCount': 30,
                'encoding': 'utf-8',
                'delay': False,
                'utc': False,
            },
        },
        'loggers': {
            '': {
                'handlers': ['console', 'detail_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'app': {
                'handlers': ['console', 'detail_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'uvicorn': {
                'handlers': ['console', 'detail_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'uvicorn.error': {
                'handlers': ['console', 'detail_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'uvicorn.access': {
                'handlers': ['console', 'detail_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    }
    logging.config.dictConfig(log_config)
