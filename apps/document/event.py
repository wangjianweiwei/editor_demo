# -*- coding: utf-8 -*-
"""
@Author：wang jian wei
@date：2023/6/27 23:00
"""
from urllib.parse import parse_qs

from ext import io
from apps.document.service import Snapshot, Session, Op


@io.event
async def connect(sid, asgi):
    print("connect")
    request = asgi["wsgi.input"]
    params = parse_qs(asgi["QUERY_STRING"])
    # TODO: 主要做认证
    # doc_id = params.get("doc", [None])[0]
    # await io.save_session(sid, Session(doc_id))
    # params = parse_qs(asgi["QUERY_STRING"])
    # doc_id = params.get("doc", [None])[0]
    # snapshot = await Snapshot(doc_id).as_dict()
    # print(request)
    # print(dir(request))
    # await io.emit("initialize", data=snapshot, to=sid)


@io.event
async def subscribe(sid, data):
    doc_id = data["doc"]
    await io.save_session(sid, Session(doc_id))
    io.enter_room(sid, room=doc_id)
    snapshot = Snapshot(doc_id)
    async for n in snapshot.history({"v": {"$gt": 40}}):
        print(n)
    data = await snapshot.as_dict()
    await io.emit("initialize", data=data, to=sid)


@io.event
async def disconnect(sid):
    print("disconnect")


@io.event
async def compose(sid, data):
    session = await io.get_session(sid)
    snapshot = Snapshot(session.doc)
    op = Op(**data)
    await snapshot.compose(op)

    await io.emit("op", data, room=session.doc)
