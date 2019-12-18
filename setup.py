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

readme = None
with open('./README_en.md', 'r+', encoding='utf8') as f:
    readme = f.read()


setup(
    name='weibo-harbor',
    version='0.1.2',
    description='A package to crawl, backup and export weibo content.',
    author='MingshiCai',
    author_email='i@unoiou.com',
    url='https://github.com/cmsax/harbor',
    long_description=readme,
    long_description_content_type='text/markdown',

    packages=find_packages(),

    install_requires=[
        'arrow',
        'peewee',
        'requests',
        'selenium',
        'BeautifulSoup4',
        'tqdm',
        'nose',
        'flake8'
    ],

    entry_points={
        'console_scripts': ['harbor = harbor.main:main']
    }
)
