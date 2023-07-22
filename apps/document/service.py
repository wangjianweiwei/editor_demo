# -*- coding: utf-8 -*-
"""
@Author：wang jian wei
@date：2023/6/24 22:19
"""
import time
from typing import Union

from delta import Delta

from ext import mongo

DEFAULT_SNAPSHOT = {"v": 0, "delta": []}


class History:

    def __init__(self, doc: int, sort_by: str = "v"):
        self.doc = doc
        self.sort_by = sort_by
        self.conditions = dict()

    def __aiter__(self):
        return mongo["history"].find({"doc": self.doc, **self.conditions}).sort(self.sort_by)

    def __call__(self, conditions=None):
        if conditions:
            self.conditions = conditions

        return self

    async def append(self, op: "Op"):
        await mongo["history"].insert_one({"doc": self.doc, **op.as_dict()})


class Snapshot:

    def __init__(self, doc: int):
        self.__v: Union[int, None] = None
        self.__delta: list = []
        self.doc = int(doc)
        self.history = History(doc=doc)

    @classmethod
    async def initialize(cls, doc: int) -> "Snapshot":
        await mongo["snapshot"].insert_one({"_id": doc, **DEFAULT_SNAPSHOT})

        return cls(doc)

    @property
    async def v(self):
        if self.__v is None:
            await self.refresh_v()

        return self.__v

    @property
    async def delta(self):
        if not self.__delta:
            await self.refresh_delta()

        return self.__delta

    async def refresh_v(self):
        data = await mongo["snapshot"].find_one({"_id": self.doc}, {"v": 1})
        self.__v = data["v"]

    async def refresh_delta(self):
        data = await mongo["snapshot"].find_one({"_id": self.doc}, {"delta": 1})
        self.__delta = data["delta"]

    async def as_dict(self):
        return {"v": await self.v, "delta": await self.delta}

    async def compose(self, op: "Op"):
        v = await self.v
        if v == op.v:
            delta = await self.delta
            snapshot = Delta(delta)
            self.__delta = snapshot.compose(Delta(op.op)).ops
            self.__v += 1
            await self.commit()
            await self.history.append(op)
        elif v > op.v:
            pass
        else:
            pass

    async def commit(self):
        await mongo["snapshot"].update_one({"_id": self.doc, "v": self.__v - 1},
                                           {"$set": {"v": self.__v, "delta": self.__delta}})


class Op:

    def __init__(self, v: int, op: list, src: str, seq: int, retries: int = 0):
        self.v = v
        self.op = op
        self.src = src
        self.seq = seq
        self.retries = retries
        self.t = time.time()

    def as_dict(self):
        return self.__dict__


class Session:

    def __init__(self, doc: int):
        self.doc = doc
