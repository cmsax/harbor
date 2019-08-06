#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: harbor/utils.py
# Author: MingshiCai i@unoiou.com
# Created Date: 2019-08-06 10:28:04
# ----
# Last Modified:
# Modified By:
# ----
# Copyright (c) 2019 MingshiCai i@unoiou.com
import re

from arrow import get
from uuid import uuid1

from harbor.constant import DIRTY_PATTERN, FILTER_PATTERNS


def uuid():
    """Get a uuid str.
    """
    return str(uuid1())


def excerpt(given_str):
    """Generate excerpt.
    TODO:
    """
    return re.split(
        r'[\W]', given_str)[0] + '...' if len(given_str) > 4 else None


def get_milliseconds(time=None):
    """Get milliseconds. Return current timestamp by default.
    Args:
        time: `datetime.datetme`

    Return:
        an `int`
    """
    t = get(time or get())
    return t.timestamp * 1000 + int(t.format('SSS'))


def filter_words(given_str):
    """Filter illegal words.
    TODO:
    """
    return purified_string(given_str, FILTER_PATTERNS)


def https_and_large(given_url):
    """HTTP to HTTPS and large
    TODO: large pic require login/token
    """
    return given_url.replace(
        'http://', 'https://'
    ) if given_url else None


def purified_string(given_str, pattern=DIRTY_PATTERN):
    """Remove newline, spaces
    """
    return re.sub(pattern, '', given_str)
