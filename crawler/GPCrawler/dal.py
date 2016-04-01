#!/usr/bin/env python
# -*- coding: utf-8 -*-

import torndb
import settings


class DAL(object):

    def __init__(self):
        self.mysql_db = torndb.Connection(
            settings.MYSQL_HOST,
            settings.MYSQL_DATABASE_NAME,
            settings.MYSQL_USER_NAME,
            settings.MYSQL_PASS_WORD
            )

    def insert(self, user):
        sql = "INSERT INTO usre (name, sex, place, cnum, follows, fans) \
                values (%s, %s, %s, %s, %s, %s)"
        result = self.mysql_db.insert(
            sql, user.name, user.sex, user.place, user.cnum, user.follows, user.fans
            )
        return result
