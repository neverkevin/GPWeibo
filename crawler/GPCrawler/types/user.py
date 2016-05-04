# -*- coding: utf-8 -*-

from base_object import BaseObject


class User(BaseObject):

    table = 'weibo'
    collection = 'user'
    keyMapping = (
            'name', 'sex', 'area', 'cnum',
            'follows', 'fans',
        )

    def __init__(self, data=None):
        self.name = ''
        self.sex = ''
        self.area = ''
        self.cnum = 0
        self.follows = 0
        self.fans = 0
        self.wid = 0

        BaseObject.__init__(self, data)
