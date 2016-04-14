# -*- coding: utf-8 -*-

import sys
import time
import random
import redis
from urlparse import urljoin
from urlparse import urldefrag
from HTMLParser import HTMLParser
import settings
from login import login
from dal import MongoDal
# from dal import MySQLDal


class BaseCrawler(object):

    domain = ''
    start_url = ()
    deny_url = ''

    def __init__(self):
        self.headers = {
            'Cookie': settings.COOKIE,
            'Host': settings.HOST,
            'Referer': settings.REFERER,
            'User-Agent': settings.USER_AGENT
            }
        # self.mysql = MySQLDal()
        self.mongo = MongoDal()
        self.redis = redis.Redis(
            host=settings.REDIS_ADDRESS,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWD,
            db=settings.REDIS_INDEX
            )
        self.start()

    def start(self):
        """Override to start crawler."""
        pass

    def parse(self, response):
        """
            Override to get items from html,
            response is `<requests.response>`.
        """
        pass

    def get_session(self):
        username = settings.USERS.get('username')
        password = settings.USERS.get('password')
        session = login(username, password)
        return session

    def get_response_from_url(self, url):
        time.sleep(random.choice(settings.DOWNLOAD_DELAY))
        print 'fetching url: %s' % url
        session = self.get_session()
        response = session.get(url)
        print 'status_code: {}'.format(response.status_code)
        if response.status_code != 200:
            print 'status_code：%s. Cookie no longer has any effect.' \
                % response.status_code
            sys._exit(0)
        if response.url == self.deny_url:
            print 'crawled errer weibo.cn/pub/, retry...'
            time.sleep(60)
            self.get_response_from_url(url)
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
