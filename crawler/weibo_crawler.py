#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import datetime
import logging
from lxml import etree
from bs4 import BeautifulSoup
from GPCrawler.types.user import User
from GPCrawler.types.contents import Contents
from GPCrawler import settings
from GPCrawler.base_crawler import BaseCrawler

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

NUM_PATTERN = re.compile('\[(\d+)\]')
WID = re.compile('\d+')
USER = re.compile('/u/\d+$')
FANS = re.compile('/fans$')
FANS_PAGE = re.compile('/fans?page=\d+$')
FOLLOW = re.compile('/follow$')
FOLLOW_PAGE = re.compile('/follow?page=\d+$')


class WeiboCrawler(BaseCrawler):

    domain = 'http://weibo.cn'
    start_urls = ('http://weibo.cn', )
    deny_url = 'http://weibo.cn/pub/'

    def start(self):
        info = self.start_login()
        for url in self.start_urls:
            self.redis.lpush("weibo_crawl_queue", url)
        try:
            while True:
                url = self.redis.lpop("weibo_crawl_queue")
                response = self.get_response_from_url(url, info['headers'])
                if response is None:
                    self.update_account_status(info['aid'], 2)
                    info = self.start_login()
                    continue
                if self.if_parse(url) and not self.redis.sismember('weibo_crawled_queue', url):
                    self.redis.sadd('weibo_crawled_queue', url)
                    self.parse(response, info)

                urls = self.get_links_from_html(response.text)
                urls = list(set(urls))
                for new_url in urls:
                    if self.if_follow(new_url) and not self.redis.sismember('weibo_crawled_queue', new_url):
                        self.redis.lpush("weibo_crawl_queue", new_url)
        except:
            logging.exception('crawler run error')

    def if_parse(self, url):
        if USER.search(url):
            return True
        return False

    def if_follow(self, url):
        if FANS.search(url) or USER.search(url) or FANS_PAGE.search(url):
            return True
        return False

    def parse(self, response, info):
        selector = etree.HTML(response.content)
        logging.info('response url %s', response.url)
        user = User()
        user.wid = int(WID.findall(response.url)[0])
        user.name = selector.xpath('//title/text()')[0][:-3]
        user_data = selector.xpath('//div[@class="u"]/table/tr/td[2]/div/span[1]/text()')
        if len(user_data) > 1:
            message = user_data[1]
        else:
            message = user_data[0].split(u'\xa0')[1]
        sex_message = message.split('/')[0].replace(u'\xa0', '')
        user.sex = sex_message
        user.area = message.split('/')[1].split(' ')[0]
        cnum = selector.xpath('//div[@class="tip2"]/span[@class="tc"]/text()')[0]
        user.cnum = self.get_num(cnum)
        follows = selector.xpath('//div[@class="tip2"]/a/text()')[0]
        user.follows = self.get_num(follows)
        fans = selector.xpath('//div[@class="tip2"]/a/text()')[1]
        user.fans = self.get_num(fans)
        total_page = selector.xpath('//input[@name="mp"]/@value')
        total_page = total_page[0] if total_page else 1
        self.mongo.insert_one(user.table, user.collection, user.__dict__)
        logging.info(
                'crawled weibo user: %s, wid: %s, sex: %s, area %s, cnum %s, follows %s, fans %s',
                user.name, user.wid, user.sex, user.area, user.cnum, user.follows, user.fans,
            )
        self.get_contents(response.url, int(total_page), info, user.wid)

    def get_contents(self, url, total_page, info, wid):
        """下载用户原创微博页面"""
        page = min(settings.CRAWL_PAGE, total_page) + 1
        for i in range(1, page):
            content_url = url + '?filter=1&page=%s' % i
            response = self.get_response_from_url(content_url, info['headers'])
            if response is None:
                self.update_account_status(info['aid'], 2)
                info = self.start_login()
                continue
            self.parse_page(response, wid)

    def parse_page(self, response, wid):
        """解析页面中的微博正文"""
        page = BeautifulSoup(response.text, 'lxml')
        divs = page.find_all('div')
        for div in divs:
            if u'class' and u'id' in div.attrs.keys() and u'c' in div.attrs[u'class']:
                content = Contents()
                content.wid = wid
                content.content = div.span.text
                ct = div.find_all('span')[-1].text.split(' ')
                if len(ct) < 2:
                    continue
                content.ct_date = self.get_date(ct[0])
                content.ct_time = ct[1][:5]
                a_info = div.find_all('a')
                for a in a_info:
                    a_text = a.text
                    if '赞' in a_text:
                        content.attitude = self.get_num(a_text)
                    elif '转发' in a_text:
                        content.repost = self.get_num(a_text)
                    elif '评论' in a_text:
                        content.comment = self.get_num(a_text)
                self.mongo.insert_one(content.table, content.collection, content.__dict__)

    def get_date(self, date):
        """统一'今天'，'4月6日'格式化为'2016-1-1'."""
        t = datetime.datetime.now()
        to_year = t.year
        to_month = t.month
        to_day = t.day
        if date == u'今天':
            return '%s-%s-%s' % (to_year, to_month, to_day)
        elif u'月' in date:
            nu = re.findall('\d+', date)
            return '%s-%s-%s' % (to_year, nu[0], nu[1])
        else:
            return date

    def get_num(self, data):
        """Get num in `abc[123]`."""
        data = NUM_PATTERN.findall(data)
        if data:
            return int(data[0])
        return 0


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='crawler.log',
        filemode='w'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    crawler = WeiboCrawler()
    crawler.start()
