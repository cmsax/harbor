#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: models/base.py
# Author: MingshiCai i@unoiou.com
# Created Date: 2019-08-06 10:32:15
# ----
# Last Modified:
# Modified By:
# ----
# Copyright (c) 2019 MingshiCai i@unoiou.com
from peewee import SqliteDatabase, Model

db = SqliteDatabase('weibo.db')


class BaseModel(Model):
    class Meta:
        database = db
