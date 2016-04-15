#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import MySQLdb
from pymongo import MongoClient
import settings


"""
def get_select_sql(tabel, keys):
    sql = 'select %s from %s' % (
        ','.join(keys), table
        )

def get_insert_sql(table, keys):
    sql = 'INSERT INTO %s (%s) VALUES (%s)' % (
        table, ', '.join(keys), ', '.join(['%s'] * len(keys))
        )
    return sql


class MySQLDal(object):

    def __init__(self):
        self.mysql_db = MySQLdb.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DATABASE_NAME,
            user=settings.MYSQL_USER_NAME,
            passwd=settings.MYSQL_PASS_WORD,
            charset="utf8"
            )

    def insert(self, table, info):
        cursor = self.mysql_db.cursor()
        sql = get_insert_sql(table, info.keys())
        cursor.execute(sql, info.values())
        uid = cursor.lastrowid
        return int(uid)

    def get(self, table, info):
        cursor = self.mysql_db.cursor()
        sql = get_select_sql(table, info.keys)
        cursor.execute(sql, info.values())
"""


class MongoDal(object):

    def __init__(self):
        self.mongo_db = MongoClient(
            settings.MONGO_HOST,
            settings.MONGO_PORT
            )

    def insert(self, info):
        db = self.mongo_db.weibo
        collections = db.weibo
        collections.insert(info)
