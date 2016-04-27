#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import getpass
import settings
from dal import MySQLDal


db = MySQLDal()
while True:
    username = raw_input('请输入帐号: ')
    password = getpass.getpass('请输入密码: ')
    info = dict(
            username=username,
            password=password,
            status=3
        )
    print info
    aid = db.insert(settings.ACCOUNT_TABLE, info)
    print "插入结果: %s" % aid
    quit = raw_input("是否继续添加(请输入y/n): ")
    if quit == 'n':
        sys.exit()
