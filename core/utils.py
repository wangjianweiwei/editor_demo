# -*- coding: utf-8 -*-
"""
@Author：wang jian wei
@date：2023/6/23 12:13
"""
from importlib import import_module

from fastapi import FastAPI
from settings import ROUTERS


def load_module(module: str):
    mod = import_module(module)

    return mod


def register_router(app: FastAPI):
    for route in ROUTERS:
        module = load_module(route)
        router = getattr(module, "router")
        if router:
            app.include_router(router)
