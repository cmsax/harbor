#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: models/post.py
# Author: MingshiCai i@unoiou.com
# Created Date: 2019-08-06 10:33:20
# ----
# Last Modified:
# Modified By:
# ----
# Copyright (c) 2019 MingshiCai i@unoiou.com
from peewee import CharField, IntegerField, TextField, DateTimeField, BooleanField

from harbor.models.base import BaseModel


class Post(BaseModel):
    content = TextField()
    time = DateTimeField()
    like_num = IntegerField(null=True)
    comment_num = IntegerField(null=True)
    repost_num = IntegerField(null=True)
    source = CharField(max_length=20)
    visibility = CharField(max_length=10, null=True)
    img_src = CharField(max_length=100, null=True)
    is_repost = BooleanField(null=True)
