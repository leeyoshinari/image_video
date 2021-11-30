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
    sql = f'select answer_id, url_token, name, content, create_time, update_time from answers where answer_id={answer_id} order by update_time desc;'
    cursor.execute(sql)
    results = cursor.fetchall()
    return results
