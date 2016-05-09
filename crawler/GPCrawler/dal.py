#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from pymongo import MongoClient
import settings


def get_where_op(k, v=''):
    where_map = dict(
            ne='!=',
            lt='<',
            lte='<',
            gt='>',
            gte='>=',
            isnull='isnull',
        )
    parts = k.rsplit('__', 1)
    if len(parts) == 2:
        k, op = parts
        op = where_map[op]
    else:
        k = parts[0]
        op = 'in' if isinstance(v, (list, tuple)) else '='
    if op == 'isnull':
        return '%s is %s' % (k, 'null' if v else 'not null')
    else:
        return '%s %s %%s' % (k, op)


def get_where_sql(where):
    if isinstance(where, (list, tuple)):
        where_keys = where
        where = {x: '' for x in where}
    else:
        where_keys = where.keys()
    return ' and '.join(get_where_op(k, where[k]) for k in where_keys)


def get_select_sql(table, keys, where=None, order_by=None, limit=None):
    sql = 'select %s from %s' % (
        ','.join(keys), table
        )
    if where:
        sql += ' where ' + get_where_sql(where)
    if order_by:
        sql += ' order by ' + order_by
    if limit:
        sql += ' limit % ' % limit
    return sql


def get_insert_sql(table, keys, where=None):
    sql = 'INSERT INTO %s (%s) VALUES (%s)' % (
        table, ', '.join(keys), ', '.join(['%s'] * len(keys))
        )
    return sql


def get_update_sql(table, update_keys, where):
    sql = 'update %s set %s where %s' % (
            table,
            ', '.join(x + '=%s' for x in update_keys),
            get_where_sql(where),
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
        cursor.execute(sql, args=info.values())
        uid = cursor.lastrowid
        self.mysql_db.commit()
        return int(uid)

    def update(self, table, info, where=None):
        cursor = self.mysql_db.cursor()
        # where option '__isnull' doesn't contain `%s`
        where_values = [
                v for k, v in where.iteritems() if not k.endswith('__isnull')
            ]
        sql = get_update_sql(table, info.keys(), where)
        cursor.execute(sql, args=(info.values() + where_values))

    def get(self, table, keys, where=None, order_by=None, limit=None):
        cursor = self.mysql_db.cursor()
        sql = get_select_sql(
                table, keys, where=where, order_by=order_by, limit=limit
            )
        # where option '__isnull' doesn't contain `%s`
        where_values = [
                v for k, v in where.iteritems() if not k.endswith('__isnull')
            ]
        cursor.execute(sql, args=where_values)
        return cursor.fetchall()

    def get_one(self, table, keys, where=None, order_by=None, limit=None):
        cursor = self.mysql_db.cursor()
        sql = get_select_sql(
                table, keys, where=where, order_by=order_by, limit=limit
            )
        # where option '__isnull' doesn't contain `%s`
        where_values = [
                v for k, v in where.iteritems() if not k.endswith('__isnull')
            ]
        cursor.execute(sql, args=where_values)
        return cursor.fetchone()


class MongoDal(object):

    def __init__(self):
        self.mongo_db = MongoClient(
                settings.MONGO_HOST,
                settings.MONGO_PORT
            )
        self.auth()

    def auth(self):
        db = self.mongo_db.admin
        db.authenticate(settings.MONGO_USER, settings.MONGO_PASSWD)

    def insert_one(self, table, collection, info):
        collection = self.get_collection(table, collection)
        collection.insert_one(info)

    def count(self, table, collection):
        collection = self.get_collection(table, collection)
        return collection.count()

    def find(self, table, collection, info=None, *arg):
        collection = self.get_collection(table, collection)
        if info is None:
            return collection.find()
        return collection.find(info, *arg)

    def find_one(self, table, collection, info=None, *arg):
        collection = self.get_collection(table, collection)
        if info is None:
            return collection.find_one()
        return collection.find_one(info, *arg)

    def aggregate(self, table, collection, info):
        collection = self.get_collection(table, collection)
        return collection.aggregate(info)

    def distinct(self, table, collection, key, filter=None):
        collection = self.get_collection(table, collection)
        return collection.distinct(key, filter)

    def get_collection(self, table, collection):
        db = self.mongo_db[table]
        return db[collection]
