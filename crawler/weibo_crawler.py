#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import Queue
import time
from bs4 import BeautifulSoup
from lxml import etree
from GPCrawler.base_crawler import BaseCrawler
from GPCrawler.user import User

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


NUM_PATTERN = re.compile('\[(\d+)\]')
USER = re.compile('/u/\d+$')
FANS = re.compile('/fans$')
FANS_PAGE = re.compile('/fans?page=\d+$')
FOLLOW = re.compile('/follow$')
FOLLOW_PAGE = re.compile('/follow?page=\d+$')


class WeiboCrawler(BaseCrawler):

    domain = 'http://weibo.cn'
    start_url = 'http://weibo.cn'

    host = "weibo.cn"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
    cookie = "_T_WM=bd230a5604cdb56bbe4314af5958fee3; SUB=_2A257-YWHDeRxGeNO7VUU8yzFzziIHXVZBSvPrDV6PUNbvtBeLVD2kW1LHesCidiZw6DLYXAl3ixoiuuf3V16Hw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFGTX4oOj01Hw_XFxKFbxQr5JpX5KMt; SUHB=0D-1-6btaOC7ng; SSOLoginState=1459484119; gsid_CTandWM=4uz7CpOz5ic9UsTQFfVL1lgiofe"
    referer = 'http://weibo.cn'
    # referer = "http://login.sina.com.cn/sso/login.php?url=http%3A%2F%2Fweibo.cn%2F&_rand=1459153356.0121&gateway=1&service=sinawap&entry=sinawap&useticket=1&returntype=META&sudaref=&_client_version=0.6.16",

    def start(self):
        crawl_queue = Queue.Queue()
        crawled_queue = set()
        crawl_queue.put(self.start_url)
        while True:
            url = crawl_queue.get()
            response = self.get_response_from_url(url)
            if self.if_parse(url) and url not in crawled_queue:
                self.parse(response)
                crawled_queue.add(url)

            urls = self.get_links_from_html(response.text)
            for new_url in urls:
                if self.if_follow(new_url) and new_url not in crawled_queue:
                    crawl_queue.put(new_url)


    def if_parse(self, url):
        if USER.search(url):
            return True
        return False

    def if_follow(self, url):
        if FANS.search(url) or FOLLOW.search(url) or USER.search(url) or \
                FANS_PAGE.search(url) or FOLLOW_PAGE.search(url):
            return True
        return False

    def parse(self, response):
        user = User()
        selector = etree.HTML(response.content)
        user.name = selector.xpath('//title/text()')[0][:-3]
        data = selector.xpath('//div[@class="u"]/table/tr/td[2]/div/span[1]/text()')
        if len(data) != 1:
            message = data[1]
        else:
            message = data[0].split(u'\xa0')[1]
        user.sex = message.split('/')[0]
        user.place = message.split('/')[1].split(' ')[0]
        num = selector.xpath('//div[@class="tip2"]/span[@class="tc"]/text()')[0]
        user.cnum = self.get_num(num)
        follows = selector.xpath('//div[@class="tip2"]/a/text()')[0]
        user.follows = self.get_num(follows)
        fans = selector.xpath('//div[@class="tip2"]/a/text()')[1]
        user.fans = self.get_num(fans)
        user.contents = self.get_contents(response.url)
        print 'Info: crawled weibo user: {}, sex: {}, place: {}, cnum: {}, follows: {}, fans: {}'.format(
                user.name, user.sex, user.place, user.cnum, user.follows, user.fans)

    def get_contents(self, url):
        """下载用户原创微博页面"""
        contents = []
        for i in range(1, 6):
            content_url = url + '?filter=1&page=%s' % i
            response = self.get_response_from_url(content_url)
            content = self.parse_page(response)
            contents.extend(content)
        return contents

    def parse_page(self, response):
        """解析页面中的微博正文"""
        page = BeautifulSoup(response.text, 'lxml')
        divs = page.find_all('div')
        content = []
        for div in divs:
            if u'class' and u'id' in div.attrs.keys() and u'c' in div.attrs[u'class']:
                text = div.span.text
                content.append(text)
        return content

    def get_num(self, data):
        """Get num in `abc[123]`."""
        data = NUM_PATTERN.findall(data)
        if data[0]:
            return data[0]
        return ''

if __name__ == '__main__':
    crawler = WeiboCrawler()
