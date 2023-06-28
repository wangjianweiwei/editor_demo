# -*- coding: utf-8 -*-
"""
@Author：wang jian wei
@date：2023/6/21 17:55
"""
from tortoise.models import Model
from tortoise import fields


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
