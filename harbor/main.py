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
import logging

from os import getenv

from harbor.spider.mobile_bot import WeiboBot

LOGGER = logging(__name__)


def main():
    save_to_directory = './weibo_backup'
    LOGGER.info('start mobile weibo bot')
    bot = WeiboBot(
        save_to_directory,
        getenv('WEIBO_USERNAME', 'default-username'),
        getenv('WEIBO_PASSWORD', 'default-password'),
    )
    bot.save_posts()
    LOGGER.info('exit normally')


if __name__ == "__main__":
    main()
