#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import base64
import logging
import settings

PWSSWD_WRONG = u'\u767b\u5f55\u540d\u6216\u5bc6\u7801\u9519\u8bef'


def login(username, password):
    """Return headers with cookies."""
    login_url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)"
    su = base64.b64encode(username)
    postdata = {
            "entry": "sso",
            "gateway": "1",
            "from": "null",
            "savestate": "30",
            "useticket": "0",
            "pagereger": "",
            "vsnf": "1",
            "su": su,
            "sp": password,
            "sr": "1280*1024",
            "encoding": "UTF-8",
            "cdult": "3",
            "domain": "sina.com.cn",
            "prelt": "0",
            "returntype": "TEXT"
        }
    session = requests.Session()
    res = session.post(login_url, data=postdata)
    res_content = json.loads(res.content)
    if res_content['retcode'] != '0':
        logging.warning('login error, reason: %s', res_content['reason'])
        return None
    logging.info('login success! %s' % username)
    cookies = session.cookies.get_dict()
    cookies = [key + "=" + value for key, value in cookies.items()]
    cookies = ";".join(cookies)
    headers = {}
    headers["Cookie"] = cookies
    headers["Host"] = settings.HOST
    headers["Referer"] = settings.REFERER
    headers["User-Agent"] = settings.USER_AGENT
    return headers
