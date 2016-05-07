# -*- coding: utf-8 -*-

import time
import random
import logging
import requests
import redis
from urlparse import urljoin
from urlparse import urldefrag
from HTMLParser import HTMLParser
import settings
from types.account import Account
from login import login
from dal import MongoDal
from dal import MySQLDal


class BaseCrawler(object):

    domain = ''
    start_url = ()
    deny_url = ''

    def __init__(self):
        self.mysql = MySQLDal()
        self.mongo = MongoDal()
        self.redis = redis.Redis(
                host=settings.REDIS_ADDRESS,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWD,
                db=settings.REDIS_INDEX
            )

    def start(self):
        """Override to start crawler."""
        pass

    def parse(self, response):
        """
            Override to get items from html,
            response is `<requests.response>`.
        """
        pass

    def start_login(self):
        while True:
            result = self.mysql.get_one(
                    settings.ACCOUNT_TABLE,
                    ['*', ],
                    where={'status': 3}
                )
            if result is None:
                time.sleep(600)
                continue
            account = Account(result)
            headers = login(account.username, account.password)
            if headers is None:
                self.update_account_status(account.aid, 1)
                continue
            info = dict(
                    aid=account.aid,
                    headers=headers
                )
            return info

    def update_account_status(self, aid, status):
        self.mysql.update(
                'account',
                {'status': status},
                where={'aid': aid}
            )

    def get_response_from_url(self, url, headers):
        time.sleep(random.choice(settings.DOWNLOAD_DELAY))
        logging.info('fetching url: %s', url)
        response = requests.get(url, headers=headers)
        # print 'status_code: {}'.format(response.status_code)
        if response.status_code != 200:
            logging.warning(
                'status_code：%s. Cookie no longer has any effect.',
                response.status_code
                )
            return None
        if response.url == self.deny_url:
            logging.warning('crawled errer weibo.cn/pub/, retry...')
            return None
        return response

    def get_links_from_html(self, html):
        urls = [urljoin(self.domain, self.remove_fragment(new_url))
                for new_url in self.get_links(html)]

        return urls

    def remove_fragment(self, url):
        """去掉链接中'#'后面的内容"""
        pure_url, frag = urldefrag(url)
        return pure_url

    def get_links(self, html):
        class URLSeeker(HTMLParser):
            def __init__(self):
                HTMLParser.__init__(self)
                self.urls = []

            def handle_starttag(self, tag, attrs):
                href = dict(attrs).get('href')
                if href and tag == 'a':
                    self.urls.append(href)

        url_seeker = URLSeeker()
        url_seeker.feed(html)

        return url_seeker.urls
