# -*- coding: utf-8 -*-

from base_object import BaseObject


class Account(BaseObject):

    table = 'account'
    keyMapping = (
           'aid', 'username', 'password', 'satatus'
        )

    def __init__(self, data=None):
        self.aid = 0
        self.username = ''
        self.password = ''
        self.status = -1

        BaseObject.__init__(self, data)
