# -*- coding: utf-8 -*-

import json


class BaseObject(object):

    table = ''
    keyMapping = ()

    def __init__(self, data=None):
        if data is not None:
            if isinstance(data, tuple):
                i = 0
                for k in self.keyMapping:
                    setattr(self, k, data[i])
                    i += 1
            elif isinstance(data.values()[0], list):
                for k in self.keyMapping:
                    if k in data:
                        setattr(self, k, data[k][0])
            else:
                for k in self.keyMapping:
                    if k in data:
                        setattr(self, k, data[k])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps(self.__dict__)
