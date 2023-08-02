# -*- coding: utf-8 -*-
"""
@Author：wang jian wei
@date：2023/6/24 22:19
"""
import time
from typing import Union

from delta import Delta
from pymongo.errors import DuplicateKeyError

from ext import mongo

DEFAULT_SNAPSHOT = {"v": 0, "delta": []}


class Retry(Exception):
    pass


class History:

    def __init__(self, snapshot: "Snapshot", doc: int, sort_by: str = "v"):
        self.snapshot = snapshot
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
        try:
            await mongo["history"].insert_one(op.as_dict())
        except DuplicateKeyError:
            await self.snapshot.retry(op)


class Snapshot:

    def __init__(self, doc: int):
        self.__v: Union[int, None] = None
        self.__delta: list = []
        self.doc = int(doc)
        self.history = History(snapshot=self, doc=doc)

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

    async def refresh(self):
        await self.refresh_delta()
        await self.refresh_v()

    def as_dict(self):
        return {"v": self.__v, "delta": self.__delta}

    async def compose(self, op: "Op"):
        v = await self.v
        if v == op.v:
            print("v == op.v")
            delta = await self.delta
            snapshot = Delta(delta)
            self.__delta = snapshot.compose(Delta(op.op)).ops
            self.__v += 1
            await self.history.append(op)
            await self.commit()

        elif v > op.v:
            print("v > op.v", v, op.v)
            async for n in self.history({"v": {"$gte": op.v, "$lt": v}}):
                conflict_op = Op(**n)
                if conflict_op.src == op.src and conflict_op.seq == op.seq:
                    print("已经提交过了")
                    return
                else:
                    op.transform(conflict_op)
                    op.v += 1

            await self.history.append(op)
            await self.commit()

        else:
            print("else")
            pass

    async def retry(self, op: "Op"):
        op.retries += 1
        if op.retries > 10:
            raise ValueError("超出最大重试次数")

        await self.compose(op)

    async def commit(self):
        await mongo["snapshot"].update_one({"_id": self.doc, "v": self.__v - 1}, {"$set": self.as_dict()})


class Op:

    def __init__(self, doc: str, v: int, op: list, src: str, seq: int, retries: int = 0, _id=None, **kwargs):
        if _id:
            self._id = _id
        else:
            self._id = f"{doc}_{v}"
        self.doc = doc
        self.v = v
        self.op = op
        self.src = src
        self.seq = seq
        self.retries = retries
        self.t = time.time()

    def transform(self, other: "Op"):
        """

        :param other:
        :return:
        """
        self.op = Delta(other.op).transform(Delta(self.op), priority="left").ops

    def as_dict(self):
        return self.__dict__


class Session:

    def __init__(self, doc: int):
        self.doc = doc


if __name__ == '__main__':
    o = Op(doc="8", **{'op': [{'retain': 45}, {'insert': '3'}], 'v': 183, 'src': 'be7R2fmIgV6V3GWzAAAT', 'seq': 0})
    b = Op(doc="8", **{'op': [{'retain': 44}, {'insert': '266'}], 'v': 183, 'src': 'CMJM0E2W03l93IwHAAAV', 'seq': 0})
    o.transform(b)
    print(o.op)
