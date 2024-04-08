LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'telegram': {
            'handlers': ['telegram_handler'],
            'level': 'INFO',
            'propagate': True,
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'telegram_handler': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # todo write custom handler to send tg bot
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{filename}  {levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
}
