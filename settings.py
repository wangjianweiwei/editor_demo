# -*- coding: utf-8 -*-
"""
@Author：wang jian wei
@date：2023/6/21 16:31
"""

MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = "3306"
MYSQL_USER = "knkj"
MYSQL_PASSWORD = "knkj5383"
MYSQL_DB = "editor_demo"

TORTOISE_CONFIG = {
    'connections': {
        # Dict format for connection
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': MYSQL_HOST,
                'port': MYSQL_PORT,
                'user': MYSQL_USER,
                'password': MYSQL_PASSWORD,
                'database': MYSQL_DB,
                'charset': 'utf8mb4'
            }
        },
    },
    'apps': {
        'models': {
            'models': ['apps.document.model', "aerich.models"],
            # If no default_connection specified, defaults to 'default'
            'default_connection': 'default',
        }
    },
    'timezone': 'Asia/Shanghai'
}
ROUTERS = [
    "apps.document.api"
]

MONGO_URI = "mongodb://admin:123456@localhost:27017/?authMechanism=DEFAULT"
