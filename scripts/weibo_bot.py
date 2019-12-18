#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: WeiboBot\wbbot.py
# Last Edited By: MingshiCai i@unoiou.com
# Date: 2019-12-15 00:08:57
from os import getenv
from tqdm import tqdm

from actions import Actions


class WeiboBot:
    """Class for weibo bot.
    """

    def __init__(self, directory, loginname, password, headless=False):
        """Init weibo bot.

        Args:
            directory
            headless
        """
        self.acts = Actions.init(directory, headless)
        self.acts.login(loginname, password)

    def save_posts(self):
        """Get all weibo content."""
        self.acts.wait().set_user_credentials().set_cookies()
        all_weibos_count = self.acts.all_weibos_count()
        progress = tqdm(total=all_weibos_count, desc='all weibos')
        posts = []
        page_index = 1
        retry = 3
        while len(posts) < all_weibos_count and retry > 0:
            try:
                posts.extend(self.acts.get_posts_single_page(page_index))
            except Exception as e:
                print(e)
                retry -= 1
            else:
                page_index += 1
                progress.update(len(posts))
                retry = 3


def main():
    save_to_directory = './weibo_backup'

    bot = WeiboBot(
        save_to_directory,
        getenv('WEIBO_USERNAME', 'default-username'),
        getenv('WEIBO_PASSWORD', 'default-password'),
    )
    bot.save_posts()


if __name__ == "__main__":
    main()
