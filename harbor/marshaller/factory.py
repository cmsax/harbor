#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: marshaller/factory.py
# Author: MingshiCai i@unoiou.com
# Created Date: 2019-08-06 10:34:37
# ----
# Last Modified:
# Modified By:
# ----
# Copyright (c) 2019 MingshiCai i@unoiou.com
from typing import NewType

from harbor.utils import (
    uuid, get_milliseconds, excerpt, https_and_large, purified_string
)
from harbor.models.post import Post

PostItem = NewType('Post', Post)  # this doesn't work yet.


class Marshaller:
    """Post marshaller base class.
    """

    available_marshallers = ['ghost']
    ghost_version = '2.14.0'

    def __init__(self, marshaller):
        """Init

        Args:
            marshaller: `str` marshaller name
        """
        if marshaller not in self.available_marshallers:
            raise KeyError('Given marshaller key is not available.')
        self._marshaller = marshaller
        self._post_id = 100  # to avoid duplicated entry, set with a big num.
        self._results = []
        self._posts = []
        self._json = {}

    @property
    def result(self):
        """Marshalled dict obj.

        Return:
            a dict
        """
        getattr(self, '_{}_json'.format(self._marshaller))()
        return self._json

    @property
    def posts(self):
        """
        Return:
            a list of dict
        """
        return self._posts

    def marshall(self, post_obj: PostItem):
        """Marshall post object.

        Args:
            post_obj: `models.Post`
        """
        getattr(self, '_{}'.format(self._marshaller))(post_obj)

    def _ghost_json(self):
        """JSON marshaller for ghost.
        """
        tag_id = 2
        user_id = 99
        weibo_user_name = 'Latina_XXX'  # customize

        self._json = {
            'meta': {
                'exported_on': get_milliseconds(),
                'version': self.ghost_version
            },
            'data': {
                'posts': self._posts,
                'tags': [{
                    'id': tag_id,
                    'name': '微博',
                    'slug': 'weibo',
                    'description': ''  # customize it if necessary
                }],
                'posts_tags': [
                    {'tag_id': tag_id, 'post_id': post_item['id']}
                    for post_item in self._posts
                ],
                'users': [{
                    "id": user_id,
                    "name": weibo_user_name,
                    "slug": '_'.join(weibo_user_name.split(' ')).lower(),
                    "email": "i@unoiou.com",
                    "profile_image": None,
                    "cover_image": None,
                    "bio": None,
                    "website": None,
                    "location": None,
                    "accessibility": None,
                    "meta_title": None,
                    "meta_description": None,
                    "created_at": get_milliseconds(),
                    "created_by": user_id,
                    "updated_at": get_milliseconds(),
                    "updated_by": user_id
                }],
            }
        }

    def _ghost(self, post_obj: PostItem):
        """Marshaller for Ghost blog engine.

        Args:
            post_obj: `models.Post`

        tags, post_tags, posts, users :: content, date, img_src, visibility
        """
        temp = {
            'id': self._post_id,
            'title': excerpt(post_obj.content) or '无题',
            'slug': '/weibo-{}'.format(uuid()),
            'mobiledoc': (
                "{\"version\":\"0.3.1\",\"atoms\":[],\"cards\":[],"
                "\"markups\":[],\"sections\":[[1,\"p\","
                "[[0,[],0,\"" + purified_string(post_obj.content) +
                "\"]]]]}"
            ),
            'plaintext': post_obj.content,
            'feature_image': https_and_large(post_obj.img_src),
            "page": 0,
            "featured": 0,
            "status": "published",
            "published_at": get_milliseconds(post_obj.time),
            "published_by": 1,
            "meta_title": None,
            "meta_description": None,
            "author_id": 1,
            "created_at": get_milliseconds(post_obj.time),
            "created_by": 1,
            "updated_at": get_milliseconds(post_obj.time),
            "updated_by": 1
        }
        self._posts.append(temp)
        self._post_id += 1
