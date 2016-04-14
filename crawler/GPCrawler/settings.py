# -*- coding: utf-8 -*-

LOGIN_URL = 'http://login.sina.com.cn/signup/signin.php?entry=sso'

HOST = "weibo.cn"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
COOKIE = "_T_WM=bd230a5604cdb56bbe4314af5958fee3; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFGTX4oOj01Hw_XFxKFbxQr5JpX5o2p; gsid_CTandWM=4uf4CpOz5nQ9LdCuk2c8Rlgiofe; SUB=_2A256Ah5wDeRxGeNO7VUU8yzFzziIHXVZDKI4rDV6PUJbrdBeLWbYkW1LHes9q7e4PKufC1d9osQ-f45s0gvFVQ..; SUHB=0Yhhtf-bog1tWl; SSOLoginState=1460039200; M_WEIBOCN_PARAMS=luicode%3D20000174"
REFERER = 'http://weibo.cn'
# REFERER = "http://login.sina.com.cn/sso/login.php?url=http%3A%2F%2Fweibo.cn%2F&_rand=1459153356.0121&gateway=1&service=sinawap&entry=sinawap&useticket=1&returntype=META&sudaref=&_client_version=0.6.16",

CR5428441557AWL_PAGE = 10
DOWNLOAD_DELAY = [0.5, 1, 2, 3]
REDIS_QUEUE = True

# mysql config
MYSQL_HOST = 'localhost'
MYSQL_DATABASE_NAME = 'weibo'
MYSQL_USER_NAME = 'root'
MYSQL_PASS_WORD = 'ssdut'

# mongo config
MONGO_HOST = 'localhost'
MONGO_PORT = 27017

# redis config
REDIS_ADDRESS = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_PASSWD = 'ssdut'
REDIS_INDEX = 1
