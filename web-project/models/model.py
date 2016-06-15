#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import hashlib
from tornado import gen
sys.path.append('../')
from crawler.GPCrawler.dal import MongoDal


mongo = MongoDal()


def md5(data):
    md5 = hashlib.md5()
    data = data + 'secret'
    md5.update(data)
    return md5.hexdigest()


@gen.coroutine
def get_count():
    user_count = mongo.count('weibo', 'user')
    contents_count = mongo.count('weibo', 'contents')
    return user_count, contents_count


@gen.coroutine
def get_users():
    return mongo.find('weibo', 'user')


@gen.coroutine
def get_user_contents(info):
    return mongo.find('weibo', 'contents', info)


@gen.coroutine
def query_sights(filter):
    return mongo.aggregate('weibo', 'sight_tendency', filter)
