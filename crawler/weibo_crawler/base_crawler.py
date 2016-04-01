# -*- coding: utf-8 -*-

# import sys
# import settings
import requests
import re
import time
import Queue
from urlparse import urljoin
from urlparse import urldefrag
from HTMLParser import HTMLParser

# sys.path.append('../')


class BaseCrawler(object):

    domain = ''
    start_url = ''

    host = ''
    user_agent = ''
    cookie = ''
    referer = ''

    def __init__(self):
        self.headers = {
            'Cookie': self.cookie,
            'Host': self.host,
            'Referer': self.referer,
            'User-Agent': self.user_agent
            }
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

    # @property
    # def crawl_urls(self):
    #     """"An alias for `get_links_from_url`"""
    #     return self.get_links_from_url(self.start_url)

    def get_response_from_url(self, url):
        print 'fetching url: %s' % url
        response = requests.get(url, headers=self.headers)
        print 'status_code: {}'.format(response.status_code)
        if response.status_code != 200:
            # logging.error
            pass
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