#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import configparser
import json
import datetime

cfg = configparser.ConfigParser()
cfg.read('config.ini', encoding = 'utf-8')

def getServer(key):
    return cfg.get('server', key, fallback = None)


def user_name(ip):
    num = ip.replace('.', '').encode('utf-8')
    res = []
    for s in num:
        res.append(s^1)
    return bytes(res).decode()


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    code = '0058409243'
    print(user_name(code))
