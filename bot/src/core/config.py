import os
from dotenv import load_dotenv
import pytz

load_dotenv()

config = {
    'BOT_TOKEN' : os.getenv('BOT_TOKEN'),

    'DATABASE_USER' : os.getenv('DATABASE_USER'),
    'DATABASE_PASSWORD' : os.getenv('DATABASE_PASSWORD'),
    'DATABASE_HOST' : os.getenv('DATABASE_HOST'),
    'DATABASE_PORT' : os.getenv('DATABASE_PORT'),
    'DATABASE_NAME' : os.getenv('DATABASE_NAME'),

    'TIMEZONE' : pytz.timezone(os.getenv('TZ')),

    'REDIS' : {
        'HOST': os.getenv('REDIS_HOST'),
        'PORT': os.getenv('REDIS_PORT'),
        'DB': os.getenv('REDIS_DB'),
    },

    'SCHEDULER_LOCK_KEY' : os.getenv('SCHEDULER_LOCK_KEY'),

    'REDIS_STREAM_KEY' : os.getenv('REDIS_STREAM_KEY'),

    'DEV_MODE' : os.getenv('DEV_MODE') == 'TRUE',

    'SHOP_SECRET_KEY' : os.getenv('SHOP_SECRET_KEY'),
    'SHOP_ID': os.getenv('SHOP_ID'),

    'DEFAULT_SMART_WALLET_PRICE': float(os.getenv('DEFAULT_SMART_WALLET_PRICE')),
}

TORTOISE_ORM = {
    'connections': {
            'default': f"asyncpg://{config['DATABASE_USER']}:{config['DATABASE_PASSWORD']}@{config['DATABASE_HOST']}:{config['DATABASE_PORT']}/{config['DATABASE_NAME']}"
        },
        'apps': {
            'models': {
                'models': ['src.models'],
                'default_connection': 'default',
            }
        }
}

