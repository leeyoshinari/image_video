#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import pymysql
from common.config import getServer


con = pymysql.connect(host=getServer('db_host'),
                      user=getServer('db_user'),
                      password=getServer('db_pwd'),
                      database=getServer('db_name'))
cursor = con.cursor()

def get_answer(answer_id):
    sql = f'select answer_id, answer_id, name, content, create_time, update_time from answers where answer_id={answer_id} order by update_time desc;'
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def get_comment(user_id):
    if '-' in user_id or len(user_id) < 22:
        sql = f'select commenter_id, answer_id, name, content, parent_id, create_time from comments where url_token="{user_id}" order by create_time desc;'
    else:
        sql = f'select commenter_id, answer_id, name, content, parent_id, create_time from comments where commenter_id="{user_id}" order by create_time desc;'

    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def get_key_word(question_id, key_word):
    sql = f'select answer_id, answer_id, name, content, create_time, update_time from answers where answer_id="{question_id}" and content like "%{key_word}%";'
    cursor.execute(sql)
    results = cursor.fetchall()
    return results
