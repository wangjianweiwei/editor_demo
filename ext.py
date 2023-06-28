# -*- coding: utf-8 -*-
"""
@Author：wang jian wei
@date：2023/6/21 16:03
"""
from fastapi import FastAPI
from socketio import AsyncServer, ASGIApp
from tortoise.contrib.fastapi import register_tortoise
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from settings import TORTOISE_CONFIG, MONGO_URI

io = AsyncServer(async_mode='asgi', cors_allowed_origins="*")
mongo_client = AsyncIOMotorClient(MONGO_URI)
mongo: AsyncIOMotorDatabase = mongo_client['editor_demo']


def startup(app: FastAPI):
    register_tortoise(app, config=TORTOISE_CONFIG)
    app.mount("", ASGIApp(io, app))

    from apps.document import event