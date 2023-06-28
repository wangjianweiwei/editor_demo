# -*- coding: utf-8 -*-
"""
@Author：wang jian wei
@date：2023/6/21 15:41
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ext import startup
from core.utils import register_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

startup(app)
register_router(app)
