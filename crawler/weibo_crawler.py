#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from lxml import etree
from bs4 import BeautifulSoup
from GPCrawler.types.user import User
from GPCrawler import settings
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


class WeiboCrawler(BaseCrawler):

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
            if self.if_parse(url) and not self.redis.sismember('weibo_crawled_queue', url):
                self.parse(response, info)
                self.redis.sadd('weibo_crawled_queue', url)

            urls = self.get_links_from_html(response.text)
            for new_url in urls:
                if self.if_follow(new_url) and not self.redis.sismember('weibo_crawled_queue', new_url):
                    self.redis.lpush("weibo_crawl_queue", new_url)

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
        print 'response.url: %s' % response.url
        user = User()
        user.name = selector.xpath('//title/text()')[0][:-3]
        data = selector.xpath('//div[@class="u"]/table/tr/td[2]/div/span[1]/text()')
        if len(data) != 1:
            message = data[1]
        else:
            message = data[0].split(u'\xa0')[1]
        user.sex = message.split('/')[0]
        user.area = message.split('/')[1].split(' ')[0]
        num = selector.xpath('//div[@class="tip2"]/span[@class="tc"]/text()')[0]
        user.cnum = self.get_num(num)
        follows = selector.xpath('//div[@class="tip2"]/a/text()')[0]
        user.follows = self.get_num(follows)
        fans = selector.xpath('//div[@class="tip2"]/a/text()')[1]
        user.fans = self.get_num(fans)
        total_page = selector.xpath('//input[@name="mp"]/@value')
        total_page = total_page[0] if total_page else 1
        user.contents = self.get_contents(response.url, int(total_page), info)
        print 'Info: crawled weibo user: {}, sex: {}, area: {}, cnum: {}, follows: {}, fans: {}'.format(
                user.name, user.sex, user.area, user.cnum, user.follows, user.fans)
        self.mongo.insert(user.__dict__)

    def get_contents(self, url, total_page, info):
        """下载用户原创微博页面"""
        page = min(settings.CRAWL_PAGE, total_page) + 1
        contents = []
        for i in range(1, page):
            content_url = url + '?filter=1&page=%s' % i
            response = self.get_response_from_url(content_url, info['headers'])
            if response is None:
                self.update_account_status(info['aid'], 2)
                info = self.start_login()
                continue
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
                s_text = div.span.text
                ct = div.find_all('span')[-1].text.split(' ')
                # 十分钟前，特殊情况待处理
                ct_date = ct[0]
                ct_time = ct[1].split(u'\xa0')[0]
                ct_from = ct[1].split(u'xa0')[1]
                a_info = div.find_all('a')
                for a in a_info:
                    a_text = a.text
                    if '赞' in a_text:
                        attitude = self.get_num(a_text)
                    elif '转发' in a_text:
                        repost = self.get_num(a_text)
                    elif '评论' in a_text:
                        comment = self.get_num(a_text)
                content.append(dict(
                            s_text=s_text,
                            ct_date=ct_date,
                            ct_time=ct_time,
                            ct_from=ct_from,
                            attitude=attitude,
                            repost=repost,
                            comment=comment
                        )
                    )
        return content

    def get_num(self, data):
        """Get num in `abc[123]`."""
        data = NUM_PATTERN.findall(data)
        if data[0]:
            return data[0]
        return ''


if __name__ == '__main__':
    crawler = WeiboCrawler()
