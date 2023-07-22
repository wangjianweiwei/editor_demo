# -*- coding: utf-8 -*-
"""
@Author：wang jian wei
@date：2023/6/21 17:55
"""

from tortoise import fields
from tortoise.models import Model
from tortoise.transactions import atomic

from apps.document.service import Snapshot


class Document(Model):
    name = fields.CharField(max_length=255)
    create_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            "id": self.pk,
            "name": self.name,
            "create_at": str(self.create_at)
        }

    @atomic()
    async def save(self, *args, **kwargs):
        await super().save(*args, **kwargs)
        await Snapshot.initialize(self.pk)
