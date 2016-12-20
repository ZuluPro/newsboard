DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'newsboard': {
            'formatter': 'base',
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'formatters': {
        'base': {'format': '%(message)s'},
        'simple': {'format': '%(asctime) %(levelname)s %(message)s'}
    },
    'loggers': {
        'newsboard': {
            'handlers': [
                'newsboard',
            ],
            'level': 'INFO'
        },
    }
}
