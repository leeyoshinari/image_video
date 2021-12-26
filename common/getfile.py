#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import os
import time
import json
import urllib.request
from common.config import getServer


p = 'C:/Users/lee_j/Pictures'
def get_file():
    dir_list = []
    file_list = []
    #files = os.stat(getServer('filePath'))
    files = os.listdir(p)
    file = [os.path.join(p, f) for f in files]
    for f in file:
        if os.path.isdir(f):
            dir_list.append({'file_name': f,
                             'file_size': None,
                             'file_atime': access_time(f),
                             'file_mtime': update_time(f),
                             'file_ctime': create_time(f)})
        else:
            file_list.append({'file_name': f,
                             'file_size': file_size(f),
                             'file_atime': access_time(f),
                              'file_mtime': update_time(f),
                             'file_ctime': create_time(f)})

    print({'dir_list': dir_list, 'file_list': file_list})


def access_time(file):
    stat_file = os.stat(file)
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat_file.st_atime))


def create_time(file):
    stat_file = os.stat(file)
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat_file.st_ctime))


def update_time(file):
    stat_file = os.stat(file)
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat_file.st_mtime))


def file_size(file):
    stat_file = os.stat(file)
    return round(stat_file.st_size / 1048576, 2)


def download_file(name):
    url = f'https://geo.datav.aliyun.com/areas_v3/bound/{name}_full.json'
    try:
        res = urllib.request.urlopen(url)
        datas = res.read()
        with open(f'../static/map/{name}.json', 'wb') as f:
            f.write(datas)
    except Exception as err:
        print(err)

if __name__ == '__main__':
    get_file()
    download_file('all')
    all_data = json.load(open('all.json', 'r', encoding='utf-8'))
    for d in all_data:
        print(d['name'], f"https://geo.datav.aliyun.com/areas_v3/bound/{d['adcode']}_full.json")
        download_file(d['adcode'])
