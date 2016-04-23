#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from GPCrawler.base_crawler import BaseCrawler

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


NUM_PATTERN = re.compile('\[(\d+)\]')
USER = re.compile('/u/\d+$')
FANS = re.compile('/fans$')
FANS_PAGE = re.compile('/fans?page=\d+$')
FOLLOW = re.compile('/follow$')
FOLLOW_PAGE = re.compile('/follow?page=\d+$')


class UrlFetcher(BaseCrawler):

    domain = 'http://weibo.cn'
    start_urls = ('http://weibo.cn',)
    deny_url = 'http://weibo.cn/pub/'

    def start(self):
        info = self.start_login()
        for url in self.start_urls:
            self.redis.lpush("weibo_crawl_queue", url)
        while True:
            url = self.redis.lpop("weibo_crawl_queue")
            response = self.get_response_from_url(url, info['headers'])
            if response is None:
                self.update_account_status(info['aid'], 2)
                info = self.start_login()
                continue
            urls = self.get_links_from_html(response.text)
            for new_url in urls:
                if self.if_follow(new_url) and not self.redis.sismember('weibo_crawled_queue', new_url):
                    self.redis.lpush("weibo_crawl_queue", new_url)

    def if_follow(self, url):
        if FANS.search(url) or USER.search(url) or FANS_PAGE.search(url):
            return True
        return False

if __name__ == '__main__':
    crawler = UrlFetcher()
