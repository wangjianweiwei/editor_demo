# -*- coding: utf-8 -*-
"""
@Author：wang jian wei
@date：2023/6/21 15:41
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index():
    return {"hello": "world"}
