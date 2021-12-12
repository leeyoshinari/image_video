#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import re
import math
import jieba
import numpy as np


def content_vector(contents):
    # contents = re.sub('[^\w]+', '', contents)
    keywords = jieba.lcut(contents)
    ret_list = []
    for word in keywords:
        word_hash = string_hash(word)
        tmp_list = []
        for feature in word_hash:
            if feature == '1':
                tmp_list.append(1)
            else:
                tmp_list.append(-1)
        ret_list.append(tmp_list)

    sum_list = np.sum(np.array(ret_list), axis=0)
    res_str = ''
    for i in sum_list:
        if i > 0:
            res_str += '1'
        else:
            res_str += '0'
    return int(('0b' + res_str), 2)


def string_hash(s):
    x = ord(s[0]) << 7
    # mask = 2 ** 128 -1
    for c in s:
        x = ((x * 1000003) ^ ord(c)) & 340282366920938463463374607431768211455

    x ^= len(s)
    if x == -1:
        x = -2

    h = bin(x).replace('0b','').zfill(64)[-64:]
    return h


def hamming_distance(hash1, hash2):
    num = (hash1 ^ hash2) & ((1 << 64) - 1)
    ans = 0
    while num:
        ans += 1
        num &= num - 1
    return ans


def cal_percentage(x):
    # a = 1 / (2 * math.pi * 0.16) ** 0.5
    # b = 2 * 0.0459 ** 2
    y = 0.9973557010035817 * math.exp((0.0065 * x) ** 2 / 0.00421362 * -1)
    return round(y * 100)


if __name__ == '__main__':
    h = hamming_distance(2784020025728, 2305845793233719680)
    print(h)