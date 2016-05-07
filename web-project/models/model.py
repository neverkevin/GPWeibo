# -*- coding: utf-8 -*-

import hashlib


def md5(data):
    md5 = hashlib.md5()
    data = data + 'secret'
    md5.update(data)
    return md5.hexdigest()
