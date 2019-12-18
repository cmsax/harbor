#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: WeiboBot\actions.py
# Author: MingshiCai i@unoiou.com
# Date: 2019-12-18 00:59:34
import json
import os
import re
import shutil

from os import getenv
from requests import get, Session
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

from marshaller import Marshaller


class Actions:
    """Class for weibo actions.

    Note that you must call `init` and `login` first.
    """
    driver = None  # set default driver to get intelisense

    base_url = 'https://m.weibo.com'
    weibo_api = (
        "https://m.weibo.cn/api/container/getIndex?containerid={}"
        "-_WEIBO_SECOND_PROFILE_WEIBO{}"
    )  # &page_type=03&page={}
    comment_api = (
        "https://m.weibo.cn/comments/hotflow"
        "?id={}&mid={}&max_id_type=0"  # mid from card
    )
    user_info_api = (
        "https://m.weibo.cn/profile/info?uid={}"
    )
    likes_api = (
        "https://m.weibo.cn/api/attitudes/show?id={}&page=1"  # mid
    )
    repost_api = (
        "https://m.weibo.cn/api/statuses/repostTimeline?id={}&page=1"  # mid
    )

    container_id = ''
    uid = ''

    driver_path = getenv('CHROMEDRIVER_PATH', './chromedriver.exe')
    all_weibos_count = 0
    session = Session()

    @classmethod
    def find_css(cls, selector, single=True):
        """Find element by css selector.

        Args:
            selector: (str) css selector
            single: (boolean) whether select single or multiple elements

        Returns:
            (Element or [Element, ])
        """
        if single:
            return cls.driver.find_element_by_css_selector(selector)
        return cls.driver.find_elements_by_css_selector(selector)

    @classmethod
    def find_xpath(cls, xpath, single=True):
        """Find element by xpath.

        Args:
            xpath: (str) xpath
            single: (boolean) whether select single or multiple elements

        Returns:
            (Element or [Element, ])
        """
        if single:
            return cls.driver.find_element_by_xpath(xpath)
        return cls.driver.find_element_by_xpath(xpath)

    @classmethod
    def wait(cls, seconds=1):
        sleep(seconds)
        return cls

    @classmethod
    def init(cls, directory, headless=False):
        """Init weibo bot.

        Args:
            directory: (str) driver default directory
            headless: (boolean) whether run selenium in headless mode
        """
        cls.directory = directory

        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option(
            "prefs", {
                "download.default_directory": cls.directory,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True, "safebrowsing.enabled": True
            })
        if headless:
            chromeOptions.add_argument("headless")
            chromeOptions.add_argument('window-size=1200x800')
        cls.driver = webdriver.Chrome(
            cls.driver_path, chrome_options=chromeOptions
        )
        return cls

    @classmethod
    def login(cls, loginname, password):
        """Login and set request session cookies.

        Args:
            loginname: (str)
            password: (str)
        """
        cls.driver.get(cls.base_url)
        sleep(2)
        cls.find_xpath("//a[contains(text(),'登录/注册')]").click()
        sleep(2)
        cls.find_xpath("//a[contains(text(),'用帐号密码登录')]").click()
        sleep(2)
        cls.find_xpath("//input[@id='loginName']").clear()
        cls.find_xpath("//input[@id='loginName']").send_keys(loginname)
        cls.find_xpath('//*[@id="loginPassword"]').clear()
        cls.find_xpath('//*[@id="loginPassword"]').send_keys(password)
        cls.find_xpath("//a[@id='loginAction']").click()
        sleep(2)

        return cls

    @classmethod
    def set_user_credentials(cls):
        """Set container id and uid."""
        cls.click_btn_profile().wait()
        cls.uid = re.findall(r'\d+', cls.driver.current_url)[0]
        cls.scroll_to_bottom().click_btn_view_all().wait(2)
        cls.container_id = re.findall(r'\d+_', cls.driver.current_url)[0]
        cls.weibo_api = cls.weibo_api.format(cls.container_id, '{}')
        return cls

    @classmethod
    def set_cookies(cls):
        """Set session cookies with webdriver's current cookies."""
        cls.session.cookies.clear()
        for cookie in cls.driver.get_cookies():
            cls.session.cookies.set(cookie['name'], cookie['value'])
        return cls

    @classmethod
    def patch_post_extra_info(cls, post_item):
        """Patch reposts, likes and comments data to post item.

        Args:
            post_item: (dict)

        Returns:
            (dict or None)
        """
        if not post_item:
            return None
        mid = post_item['id']
        for key, api, extra_mid in [
            ['comments', cls.comment_api, True],
            ['likes', cls.likes_api, False],
            ['reposts', cls.repost_api, False]
        ]:
            url = api.format(*(mid, mid) if extra_mid else mid)
            post_item[key] = cls.session.get(url).json()
        return post_item

    @classmethod
    def download_original_image(cls, urls, mid):
        """Download and save image by weibo id.

        Args:
            urls: ([str, ]) image urls list
            mid: (str) weibo mid
        """
        pic_dir = './download/users/{}/images/{}'.format(cls.uid, mid)
        if not os.path.exists(pic_dir):
            os.makedirs(pic_dir)
        for pic_index, url in enumerate(urls):
            res = cls.session.get(url, stream=True)
            pic_suffix = url.split('.')[-1]
            with open(
                '{}/{}.{}'.format(pic_dir, pic_index, pic_suffix), 'wb'
            ) as pic_file:
                res.raw.decode_content = True
                shutil.copyfileobj(res.raw, pic_file)

    @classmethod
    def get_posts_single_page(cls, page_index=None):
        """Get posts in single page.

        Args:
            page_index: (int) page index

        Returns:
            [dict, ]
        """
        suffix = '&page_type=03&page={}'.format(
            page_index) if page_index else ''
        res = cls.session.get(cls.weibo_api.format(suffix))
        cards = res.json()['data']['cards']
        posts = []
        for card in cards:
            post = cls.patch_post_extra_info(Marshaller.mobile_card(card))
            if post:
                if post['pic_num'] > 0:
                    pic_urls = [item['large']['url'] for item in post['pics']]
                    cls.download_original_image(pic_urls, post['id'])
                posts.append(post)
        cls.cache_posts(posts, page_index)
        cls.wait(10)
        return posts

    @classmethod
    def cache_posts(cls, posts, page_index):
        """Save posts locally.

        Args:
            posts: ([dict, ]) list of posts
            page_index: (int)
        """
        with open(
            './download/users/{}/posts/{}.json'.format(cls.uid, page_index),
            'w+', encoding='UTF8'
        ) as json_file:
            json.dump(posts, json_file, ensure_ascii=False)

    @classmethod
    def click_btn_profile(cls):
        """Click the nav btn to go to homepage.
        """
        cls.find_css('.nav-left').click()
        return cls

    @classmethod
    def all_weibos_count(cls):
        """Get current user's all weibos count"""
        return int(cls.session.get(
            cls.user_info_api.format(cls.uid)
        ).json()['data']['user']['statuses_count'])

    @classmethod
    def click_btn_view_all(cls):
        """Go to all weibos page.
        """
        cls.find_css('.lite-btn-more').click()
        return cls

    @classmethod
    def scroll_to_bottom(cls):
        cls.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight)"
        )
        return cls
