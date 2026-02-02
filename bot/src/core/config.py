import os
from dotenv import load_dotenv
from datetime import timezone

load_dotenv()

config = {
    'BOT_TOKEN' : os.getenv('BOT_TOKEN'),

    'DATABASE_USER' : os.getenv('DATABASE_USER'),
    'DATABASE_PASSWORD' : os.getenv('DATABASE_PASSWORD'),
    'DATABASE_HOST' : os.getenv('DATABASE_HOST'),
    'DATABASE_PORT' : os.getenv('DATABASE_PORT'),
    'DATABASE_NAME' : os.getenv('DATABASE_NAME'),

    'TIMEZONE' : timezone.utc,

    'REDIS' : {
        'HOST': os.getenv('REDIS_HOST'),
        'PORT': os.getenv('REDIS_PORT'),
        'DB': os.getenv('REDIS_DB'),
    },

    'TEST_PRIVATE_GROUP_ID' : -1003804979475
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

