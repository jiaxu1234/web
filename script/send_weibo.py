# -*- coding: utf-8 -*-
# @project : web
# @file   : login_weibo.py
# @time   : 2019-12-31

from __future__ import absolute_import, division, print_function, unicode_literals

import re
import json
import time
import base64
import binascii
import datetime
import rsa
import requests
import logging
logging.basicConfig(level=logging.DEBUG)

import sys
sys.path.append("/var/config")
import config

WBCLIENT = 'ssologin.js(v1.4.5)'
user_agent = (
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) '
    'Chrome/20.0.1132.57 Safari/536.11'
)
session = requests.session()
session.headers['User-Agent'] = user_agent


def encrypt_passwd(passwd, pubkey, servertime, nonce):
    key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(passwd)
    passwd = rsa.encrypt(message.encode('utf-8'), key)
    return binascii.b2a_hex(passwd)


def wblogin(username, password):
    resp = session.get(
        'http://login.sina.com.cn/sso/prelogin.php?'
        'entry=sso&callback=sinaSSOController.preloginCallBack&'
        'su=%s&rsakt=mod&client=%s' %
        (base64.b64encode(username.encode('utf-8')), WBCLIENT)
    )

    pre_login_str = re.match(r'[^{]+({.+?})', resp.text).group(1)
    pre_login = json.loads(pre_login_str)

    pre_login = json.loads(pre_login_str)
    data = {
        'entry': 'weibo',
        'gateway': 1,
        'from': '',
        'savestate': 7,
        'userticket': 1,
        'ssosimplelogin': 1,
        'su': base64.b64encode(requests.utils.quote(username).encode('utf-8')),
        'service': 'miniblog',
        'servertime': pre_login['servertime'],
        'nonce': pre_login['nonce'],
        'vsnf': 1,
        'vsnval': '',
        'pwencode': 'rsa2',
        'sp': encrypt_passwd(password, pre_login['pubkey'],
                             pre_login['servertime'], pre_login['nonce']),
        'rsakv' : pre_login['rsakv'],
        'encoding': 'UTF-8',
        'prelt': '115',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.si'
               'naSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }


    resp = session.post(
        'http://login.sina.com.cn/sso/login.php?client=%s' % WBCLIENT,
        data=data
    )

    login_url = re.search('replace\\(\'([^\']+)\'\\)', resp.text).group(1)
    resp = session.get(login_url)
    login_str = re.search('\((\{.*\})\)', resp.text).group(1)
    print (login_str)
    # return json.loads(login_str)
    return session

def send_weibo(session, text):
    data = {
      'location': 'v6_content_home',
      'text': text + "\n" + str(datetime.datetime.now()),
      'appkey': '',
      'style_type': '1',
      'pic_id': '',
      'tid': '',
      'pdetail': '',
      'mid': '',
      'isReEdit': 'false',
      'rank': '0',
      'rankid': '',
      'module': 'stissue',
      'pub_source': 'main_',
      'pub_type': 'dialog',
      'isPri': '0',
      '_t': '0'
    }


    session.headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Origin': 'https://weibo.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': config.weibo_referer,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }


    response = session.post("https://www.weibo.com/aj/mblog/add?ajwvr=6&__rnd=%d"
                 % int(time.time() * 1000),
                 data=data)
    print(response.text)
    print ("success")


def get_pyq_text():
    headers = {
        'authority': 'pyq.shadiao.app',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://pyq.shadiao.app/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': 'Hm_lvt_0a17234907531e3e9a08a980e5da5f15=1575910462; Hm_lpvt_0a17234907531e3e9a08a980e5da5f15=1575910462; Hm_lvt_a2a4c0cfcbcf95285d39e12f99d7a4f3=1575910582; Hm_lpvt_a2a4c0cfcbcf95285d39e12f99d7a4f3=1575910582',
    }

    response = requests.get('https://pyq.shadiao.app/api.php', headers=headers)
    pyq_text = response.content.decode('utf8')
    print(pyq_text)
    return pyq_text

def get_chp_text():
    headers = {
        'authority': 'chp.shadiao.app',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://chp.shadiao.app/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': 'Hm_lvt_0a17234907531e3e9a08a980e5da5f15=1575910462; Hm_lpvt_0a17234907531e3e9a08a980e5da5f15=1575910462; Hm_lvt_0237bad9496c62f26747ca19a52eca1a=1575910143,1575910981; Hm_lpvt_0237bad9496c62f26747ca19a52eca1a=1575910981',
    }

    response = requests.get('https://chp.shadiao.app/api.php', headers=headers)
    chp = response.content.decode('utf8')
    print(chp)
    return chp



if __name__ == '__main__':
    # text = get_pyq_text()
    text = get_chp_text()
    session = wblogin(config.weibo_account, config.weibo_secret)
    send_weibo(session, text)