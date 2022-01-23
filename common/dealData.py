#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import re
import time
import json
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

def get_address1(host):
    try:
        p = '<div id="tab0_address">(.*?)</div>'
        pp = '<p>(.*?)</p>'
        res = requests.get('https://www.ip.cn/ip/{}.html'.format(host))
        r = re.findall(p, res.text)[0]
        datas = r.split(' ')
        if len(datas) == 5:
            if datas[2] in only_city:
                province = f"'{datas[2] + '市'}'"
                city = 'null'
            else:
                province = f"'{datas[2]}'"
                city = f"'{datas[3]}'" if datas[3] else 'null'

            district = 'null'
            net = f"'{datas[4]}'" if datas[4] else 'null'
        else:
            return None
        return [province, city, district, net]
    except:
        return None


def get_address2(host):
    try:
        p = '查询IP地址([\s\S]*?)</tbody>'
        pp = '<td>([\s\S]*?)</td>'
        res = requests.get('http://www.jsons.cn/ip/{}/'.format(host))
        r = re.findall(p, res.text)[0]
        result = r.strip()
        rr = re.findall(pp, result)
        datas = [rt.strip() for rt in rr]
        if len(datas) == 8:
            if datas[3] in only_city:
                province = f"'{datas[3] + '市'}'"
                city = 'null'
            else:
                province = f"'{datas[3] + '省'}'"
                city = f"'{datas[5]}'" if datas[5] else 'null'

            district = 'null'
            net = f"'{datas[7]}'" if datas[7] else 'null'
        else:
            return None
        return [province, city, district, net]
    except:
        return None


def get_address3(host):
    try:
        res = requests.get('https://whois.pconline.com.cn/ipJson.jsp?ip={}&json=true'.format(host))
        r = json.loads(res.text)
        if r.get('pro'):
            province = f"'{r.get('pro')}'"
            city = f"'{r.get('city')}'" if r.get('city') else 'null'

            district = 'null'
            net = f"'{r.get('addr').split(' ')[-1]}'" if r.get('addr') else 'null'
        else:
            return None
        return [province, city, district, net]
    except:
        return None


def get_address4(host):
    try:
        res = requests.get('https://ip.taobao.com/outGetIpInfo?ip={}&accessKey=alibaba-inc'.format(host))
        r = json.loads(res.text).get('data')
        if r.get('region'):
            if r.get('region') in only_city:
                province = f"'{r.get('region') + '市'}'"
                city = 'null'
            else:
                province = f"'{r.get('region') + '省'}'"
                city = f"'{r.get('city') + '市'}'" if r.get('city') else 'null'

            district = 'null'
            net = f"'{r.get('isp')}'" if r.get('isp') else 'null'
        else:
            return None
        return [province, city, district, net]
    except:
        return None


def get_address(host):
    time.sleep(0.5)
    res = get_address3(host)
    if res:
        return res
    res = get_address4(host)
    if res:
        return res
    res = get_address2(host)
    if res:
        return res
    res = get_address1(host)
    if res:
        return res
    return ['null', 'null', 'null', 'null']


if __name__ == '__main__':
    print(get_address('117.136.23.197'))
    print(get_address4('117.9.23.18'))
