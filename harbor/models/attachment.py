#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: models/attachment.py
# Author: MingshiCai i@unoiou.com
# Created Date: 2019-08-06 10:32:42
# ----
# Last Modified:
# Modified By:
# ----
# Copyright (c) 2019 MingshiCai i@unoiou.com
from peewee import CharField, ForeignKeyField

from harbor.models.base import BaseModel
from harbor.models.post import Post


class Attachment(BaseModel):
    uri = CharField(max_length=500, null=True)
    post = ForeignKeyField(Post, backref='attachments')
