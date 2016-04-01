# -*- coding: utf-8 -*-

from util.base_object import BaseObject


class User(BaseObject):

    keyMapping = (
            'name', 'sex', 'place',
            'follows', 'fans', 'contents'
            )

    def __init__(self, data=None):
        self.name = ''
        self.sex = ''
        self.place = ''
        self.follows = ''
        self.fans = ''
        self.contents = []

        BaseObject.__init__(self, data)
