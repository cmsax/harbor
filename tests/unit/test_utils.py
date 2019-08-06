#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: unit/test_utils.py
# Author: MingshiCai i@unoiou.com
# Created Date: 2019-08-06 11:21:36
# ----
# Last Modified:
# Modified By:
# ----
# Copyright (c) 2019 MingshiCai i@unoiou.com
from nose.tools import assert_equals

from harbor import utils


def test_http_to_https():
    """Check if `utils.https_and_large` works
    """
    fake = 'http://abc.com'
    expect = 'https://abc.com'
    assert_equals(utils.https_and_large(fake), expect)
