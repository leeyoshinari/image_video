#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import configparser


cfg = configparser.ConfigParser()
cfg.read('config.ini', encoding = 'utf-8')

def getServer(key):
    return cfg.get('server', key, fallback = None)

