import logging
import telegram
from os import environ


class TelegramHandler(logging.Handler):
    def __init__(self, telegram_bot_token, telegram_chat_id, message_thread_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id
        self.message_thread_id = message_thread_id

    def emit(self, record):
        log_entry = self.format(record)
        # bot = telegram.Bot(token=self.telegram_bot_token)
        # bot.send_message(chat_id=self.telegram_chat_id, text=log_entry, message_thread_id=self.message_thread_id)
        print(log_entry)

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
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'telegram_info': {
            'level': 'INFO',
            'class': 'core.settings.logging.TelegramHandler',
            'telegram_bot_token': environ.get('TELEGRAM_BOT_TOKEN', ''),
            'telegram_chat_id': environ.get('TELEGRAM_GROUP_ID', ''),
            'message_thread_id': environ.get('INFO_LOG_TOPIC_ID', ''),
            'formatter': 'verbose',
        },
        'telegram_error': {
            'level': 'ERROR',
            'class': 'core.settings.logging.TelegramHandler',
            'telegram_bot_token': environ.get('TELEGRAM_BOT_TOKEN', ''),
            'telegram_chat_id': environ.get('TELEGRAM_GROUP_ID', ''),
            'message_thread_id': environ.get('ERROR_LOG_TOPIC_ID', ''),
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
