#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""每天重置一次cookie失效的帐号的状态"""
from GPCrawler.dal import MySQLdb


db = MySQLdb()
db.update(
        'account',
        {'status', 2},
        where={'status', 3}
    )
