# -*- coding: utf-8 -*-

from base_object import BaseObject


class User(BaseObject):

    table = 'user'
    keyMapping = (
            'name', 'sex', 'area', 'cnum',
            'follows', 'fans',
        )

    def __init__(self, data=None):
        self.name = ''
        self.sex = ''
        self.area = ''
        self.cnum = ''
        self.follows = ''
        self.fans = ''
        self.wid = ''

        BaseObject.__init__(self, data)
