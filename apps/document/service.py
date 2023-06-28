# -*- coding: utf-8 -*-
"""
@Author：wang jian wei
@date：2023/6/24 22:19
"""
import time
from typing import Union

from delta import Delta

from ext import mongo


class History:

    def __init__(self, doc: str, reverse: bool = False):
        self.doc = doc
        self.reverse = reverse

    async def __aiter__(self):
        return self

    async def __anext__(self):
        async for n in mongo["snapshot"].find({"_id": "64970a215901772fd2bd40aa"}):
            yield n


class Snapshot:

    def __init__(self, doc: str):
        self.__v: Union[int, None] = None
        self.doc = doc
        self.history = History(doc=doc)

    @property
    async def v(self):
        if self.__v is None:
            await self.refresh_v()

        return self.__v

    async def refresh_v(self):
        data = await mongo["snapshot"].find_one({"_id": self.doc}, {"v": 1})
        self.__v = data["v"]

    def compose(self, op: "Op"):
        pass


class Op:

    def __init__(self, v: int, op: list, src: str, seq: int, user: int, retries: int = 0):
        self.v = v
        self.op = op
        self.src = src
        self.seq = seq
        self.user = user
        self.retries = retries
        self.t = time.time()
