#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: harbor/main.py
# Author: MingshiCai i@unoiou.com
# Created Date: 2019-08-06 10:27:19
# ----
# Last Modified:
# Modified By:
# ----
# Copyright (c) 2019 MingshiCai i@unoiou.com
from harbor.constant import HEADERS
from harbor.models.attachment import Attachment
from harbor.models.base import db
from harbor.models.post import Post
from harbor.spider.main import Spider


def main():
    """Entry point
    """
    db.create_tables([Attachment, Post])
    HEADERS['Cookie'] = ''
    uid = ''
    marshaller = 'ghost'
    s = Spider(HEADERS, uid, marshaller)
    try:
        s.start()
    except Exception as e:
        print(e)
        print(s._current_page)
        s._dump()


if __name__ == "__main__":
    main()
