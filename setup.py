#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: harbor/setup.py
# Author: MingshiCai i@unoiou.com
# Created Date: 2019-08-06 10:05:34
# ----
# Last Modified:
# Modified By:
# ----
# Copyright (c) 2019 MingshiCai i@unoiou.com
"""Set up modules
"""
from setuptools import setup, find_packages

setup(
    name='Harbor',
    version='0.1.0',
    description='A package to crawl, backup and export weibo content.',
    author='MingshiCai i@unoiou.com',

    packages=find_packages(),

    install_requires=[
        'arrow',
        'peewee',
        'requests',
        'BeautifulSoup4',
        'tqdm',
        'nose'
    ],

    entry_points={
        'console_scripts': ['harbor = harbor.main:main']
    }
)
