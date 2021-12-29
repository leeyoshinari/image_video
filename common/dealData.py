#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import re
import requests


only_city = ['北京', '天津', '上海', '重庆']


def get_system(s):
    if 'HarmonyOS' in s:
        system = 'Harmony'
    elif 'Android' in s:
        system = 'Android'
    elif 'iPhone' in s:
        system = 'iPhone'
    elif 'Macintosh' in s:
        system = 'Macintosh'
    elif 'Linux' in s:
        system = 'Linux'
    elif 'Windows' in s:
        system = 'Windows'
    else:
        system = None
    return system

def get_browser(s):
    if 'ZhihuHybrid' in s:
        browser = 'ZhihuHybrid'
    elif 'Firefox' in s:
        browser = 'Firefox'
    elif 'Edg' in s:
        browser = 'Edge'
    elif 'MetaSr' in s:
        browser = 'MetaSr'
    elif 'QQBrowser' in s:
        browser = 'QQBrowser'
    elif 'MicroMessenger' in s:
        browser = 'MicroMessenger'
    elif 'MiuiBrowser' in s:
        browser = 'MiuiBrowser'
    elif 'Baidu' in s:
        browser = 'Baidu'
    elif 'Trident' in s:
        browser = 'IE'
    elif 'HuaweiBrowser' in s:
        browser = 'HuaweiBrowser'
    elif 'Safari' in s and 'Chrome' not in s:
        browser = 'Safari'
    elif 'Chrome' in s:
        browser = 'Chrome'
    else:
        browser = None
    return browser


def get_mobile(s):
    if 'Mobile' in s:
        if 'iPhone' in s:
            mobile = '苹果'
        elif 'HUAWEI' in s or 'ANE-AL' in s:
            mobile = '华为'
        elif 'MI' in s or 'Mi' in s:
            mobile = '小米'
        elif 'HONOR' in s:
            mobile = '荣耀'
        elif 'vivo' in s or 'V1986A' in s or 'V1838' in s or 'V2049A' in s:
            mobile = 'vivo'
        elif 'PEDM0' in s or 'PCLM1' in s:
            mobile = 'oppo'
        elif 'SM-G' in s:
            mobile = '三星'
        elif 'meizu' in s or '16s Pro' in s:
            mobile = '魅族'
        elif 'Coolpad' in s:
            mobile = '酷派'
        elif 'Redmi' in s or 'M2012K11' in s or "RKQ" in s or 'M2007J17' in s or 'M2004J7' in s:
            mobile = '红米'
        else:
            mobile = None
    else:
        mobile = None

    return mobile

def get_address(host):
    try:
        p = 'Whwtdhalf w45-0 lh24 tl ml70">([\s\S]*)col-gray ml10 ip138'
        pp = '<p>(.*?)</p>'
        res = requests.get('https://ip.tool.chinaz.com/{}'.format(host))
        r = re.findall(p, res.text)[0]
        result = r.strip()
        rr = re.findall(pp, result)[0]
        datas = rr.split(' ')
        if len(datas) == 5:
            if datas[1] in only_city:
                province = f"'{datas[1] + '市'}'"
                city = f"'{datas[2]}'" if datas[2] else 'null'
            else:
                province = f"'{datas[1] + '省'}'"
                city = f"'{datas[2] + '市'}'" if datas[2] else 'null'

            district = f"'{datas[3]}'" if datas[3] else 'null'
            net = f"'{datas[4]}'" if datas[4] else 'null'
        else:
            return ['null', 'null', 'null', 'null']
        return [province, city, district, net]
    except:
        return ['null', 'null', 'null', 'null']


if __name__ == '__main__':
    pass
