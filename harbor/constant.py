#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: harbor/constant.py
# Author: MingshiCai i@unoiou.com
# Created Date: 2019-08-06 10:28:15
# ----
# Last Modified:
# Modified By:
# ----
# Copyright (c) 2019 MingshiCai i@unoiou.com
import re

FILTER_PATTERNS = [
    re.compile(r'反动')
]
DIRTY_PATTERN = re.compile(r'(\\n)|(\s+)')

URL_TPL = 'https://weibo.cn/{}/profile?page={}'
HEADER_PATH_TPL = '/{}/profile?page={}'
REFERER_URL_TPL = 'https://weibo.cn/{}/profile?page={}'

LIKE_NUM_PATTERN = re.compile(r'赞\[(\d+)\]')
COMMENT_NUM_PATTERN = re.compile(r'评论\[(\d+)\]')
REPO_NUM_PATTERN = re.compile(r'转发\[(\d+)\]')
REPO_TEST_PATTERN = re.compile(r'(转发了)|(Repost)')
TIME_PATTERN = re.compile(
    r'(\d+月\d+日 [\d\:]+)|(\d{4}\-\d{2}\-\d{2} [\d\:]+)')
SOURCE_DEVICE_PATTERN = re.compile(r'(来自.+)')
VISIBILITY_PATTERN = re.compile(r'\[([仅自].+)\]')

DATE_FMTS = (
    'YYYY年MM月DD日 HH:mm', 'YYYY-MM-DD HH:mm:ss'
)

HEADERS = {
    'authority': 'weibo.cn',
    'method': 'GET',
    'scheme': 'https',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Cookie': None  # set to your own cookie
}
