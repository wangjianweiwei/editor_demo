# -*- coding: utf-8 -*-
"""
@Author：wang jian wei
@date：2023/6/21 17:55
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from apps.document import model
from ext import mongo
from apps.document.service import Snapshot
from apps.document import schemas

router = APIRouter(prefix="/document")


@router.get("/list")
async def documents():
    queryset = await model.Document.all()

    return JSONResponse({"data": [n.as_dict() for n in queryset]})


@router.post(path="/create", )
async def create(doc: schemas.Document):
    document = model.Document(name=doc.name)
    await document.save()
    # queryset = await model.Document.filter()
    # for n in queryset:
    #     print(n.name)

    # snapshot = Snapshot(doc="64970a215901772fd2bd40aa")
    # async for n in snapshot.history:
    #     print(n)

    return JSONResponse({"data": document.as_dict()})
