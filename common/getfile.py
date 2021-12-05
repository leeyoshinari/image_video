#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import os
import time
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


if __name__ == '__main__':
    get_file()