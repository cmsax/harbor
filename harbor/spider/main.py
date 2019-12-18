#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: spider/main.py
# Author: MingshiCai i@unoiou.com
# Created Date: 2019-08-06 10:36:40
# ----
# Last Modified:
# Modified By:
# ----
# Copyright (c) 2019 MingshiCai i@unoiou.com
import logging
import json
import re

from arrow import get as ar
from bs4 import BeautifulSoup as BS
from requests import get
from tqdm import tqdm
from time import sleep

from harbor.constant import (
    URL_TPL, HEADER_PATH_TPL, REFERER_URL_TPL, LIKE_NUM_PATTERN,
    COMMENT_NUM_PATTERN, REPO_NUM_PATTERN, REPO_TEST_PATTERN, TIME_PATTERN,
    DATE_FMTS, SOURCE_DEVICE_PATTERN, VISIBILITY_PATTERN
)
from harbor.marshallers.factory import Marshaller
from harbor.models.attachment import Attachment
from harbor.models.post import Post

LOGGER = logging.getLogger(__name__)


class Spider:
    """A spider that does everything.

    Not an abstract factory.
    """

    def __init__(self, headers, uid, marshaller_name):
        if not headers['Cookie']:
            raise KeyError("Empty cookie.")
        self._all_page_num = None
        self._all_post_num = 0
        self._current_year = ar().year
        self._current_page = 0
        self._current_html = None
        self._post_item = None
        self._attachment_item = None
        self._uid = uid
        self._headers = headers
        self._marshaller = Marshaller(marshaller_name)

    @property
    def url(self):
        """Dynamically get url and `_current_page` auto increment.
        """
        self._current_page += 1
        return URL_TPL.format(self._uid, self._current_page)

    @property
    def headers(self):
        """Dynamically get `:path` and `referer` header.
        """
        self._headers['path'] = HEADER_PATH_TPL.format(
            self._uid, self._current_page)
        self._headers['referer'] = REFERER_URL_TPL.format(
            self._uid, self._current_page - 1
        )
        return self._headers

    @property
    def has_post(self):
        return True if self._current_page < self._all_page_num else False

    def _set_all_page_num(self):
        """Initialize all page num.
        """
        res = get(self.url, headers=self.headers)
        post_num = re.findall(r'微博\[(\d+)\]', res.text)[0]
        page_num = re.findall(r'\/(\d+)页', res.text)[0]
        self._current_page -= 1
        self._all_page_num = int(page_num)
        self._all_post_num = int(post_num)

    def _get_html(self):
        url = self.url
        res = None
        while True:
            res = get(url, headers=self.headers)
            if res.status_code == 200:
                break
            sleep(4)
        self._current_html = res.text

    def _parse(self):
        """Extract info from HTML content.
        TODO: refractor
        """
        soup = BS(self._current_html, 'lxml')
        for item in soup.select('div.c'):
            temp = {}
            # main content
            ctt = item.select('span.ctt')
            if not ctt:
                continue
            weibo_body = item.select('div')
            if len(weibo_body) > 1:
                temp['content'] = weibo_body[0].text
                btn_group = weibo_body[1].text
            else:
                temp['content'] = weibo_body[0].select('span.ctt')[0].text
                btn_group = weibo_body[0].text
            temp['is_repost'] = True if REPO_TEST_PATTERN.match(
                temp['content']) else False
            try:
                temp['like_num'] = LIKE_NUM_PATTERN.findall(btn_group)[0]
                temp['cmt_num'] = COMMENT_NUM_PATTERN.findall(btn_group)[0]
                temp['repo_num'] = REPO_NUM_PATTERN.findall(btn_group)[0]
            except Exception:
                pass
            cmt = item.select('.cmt')
            # visibility
            if cmt:
                try:
                    temp['visibility'] = VISIBILITY_PATTERN.findall(
                        cmt[0].text)[0]
                except Exception:
                    pass

            # img in main content
            img = item.select('div a img')
            img_src = img[0].attrs['src'] if img else None
            temp['img_src'] = img_src
            LOGGER.debug('img_src: {}'.format(img_src))
            # time & source device
            ct = item.select('span.ct')
            if ct:
                ct = ct[0]
                text = ct.text
                reg_result = TIME_PATTERN.findall(text)[0]

                temp['time'] = ar(
                    '{}年{}'.format(self._current_year, reg_result[0]),
                    DATE_FMTS[0]
                ).naive if reg_result[0] else ar(
                    reg_result[1], DATE_FMTS[1]
                ).naive
                temp['source'] = SOURCE_DEVICE_PATTERN.findall(text)[0]
            self._post_item = Post(**temp)
            self._attachment_item = Attachment(
                uri=img_src, post=self._post_item)
            self._store()

    def _store(self):
        """Commit to SQL database.
        Can be async.
        """
        self._post_item.save()
        self._attachment_item.save()
        self._marshaller.marshall(self._post_item)

    def _dump(self):
        """Dump JSON object to document database.
        """
        with open('weibo_dumps.json', 'w+', encoding='utf-8') as f:
            json.dump(self._marshaller.result, f, ensure_ascii=False)

    def start(self):
        """Start spider. Auto exit when no more post.
        """
        if not self._all_page_num:
            self._set_all_page_num()
            LOGGER.debug('overall pages: {}'.format(self._all_page_num))
        with tqdm(total=self._all_page_num) as progress_bar:
            while self.has_post:
                self._get_html()
                self._parse()
                # 10 post each page.
                progress_bar.update(1)
                progress_bar.set_description(
                    'Page #{}'.format(self._current_page))
                sleep(4)
            self._dump()


def main():
    from harbor.models.base import db
    from harbor.models.post import Post
    from harbor.models.attachment import Attachment
    from harbor.constant import HEADERS
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
        LOGGER.debug(e)
        LOGGER.debug(s._current_page)
        s._dump()


if __name__ == "__main__":
    main()
