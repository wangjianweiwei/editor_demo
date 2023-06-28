# -*- coding: utf-8 -*-
"""
@Author：wang jian wei
@date：2023/6/27 23:00
"""

from ext import io


@io.event
async def connect(sid, asgi):
    print("connect")
    request = asgi["wsgi.input"]


@io.event
async def hello(sid, data: dict):
    print(data)
    await io.emit("client", {"m": data["m"].upper()})


@io.event
async def disconnect(sid):
    print("disconnect")


@io.event
async def op(sid, data):
    print(sid)
    print(data)

    await io.emit("op", data, to=sid)
