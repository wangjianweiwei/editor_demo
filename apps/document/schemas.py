# -*- coding: utf-8 -*-
"""
@Author：wang jian wei
@date：2023/6/21 17:55
"""
from pydantic import BaseModel, Field


class Document(BaseModel):
    name: str = Field(max_length=255, min_length=1, default="未命名")
