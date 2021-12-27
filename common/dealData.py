#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari

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
        elif 'MI' in s:
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
        elif 'Redmi' in s or 'M2012K11' in s or "RKQ" in s or 'M2007J17' in s:
            mobile = '红米'
        else:
            mobile = None
    else:
        mobile = None

    return mobile


if __name__ == '__main__':
    pass
