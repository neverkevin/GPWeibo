#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""利用crontab每天重置一次cookie失效的帐号的状态"""
from GPCrawler.dal import MySQLDal


db = MySQLDal()
db.update(
        'account',
        dict(status=3),
        where=dict(status=2)
    )
