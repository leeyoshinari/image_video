#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import pymysql
from common.config import getServer


def get_answer(answer_id, page):
    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'),
                          password=getServer('db_pwd'), database=getServer('db_name'))
    cursor = con.cursor()
    sql = f'select question_id, answer_id, name, content, create_time, update_time from simple_answer where answer_id={answer_id} order by update_time desc limit 15 offset {page};'
    count = f'select count(1) from simple_answer where answer_id={answer_id};'
    try:
        cursor.execute(count)
        total_page = cursor.fetchall()
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        return None, None
    del cursor, con
    return results, total_page[0][0]


def get_comment(user_id, page):
    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'),
                          password=getServer('db_pwd'), database=getServer('db_name'))
    cursor = con.cursor()
    if '-' in user_id or len(user_id) < 22:
        sql = f'select b.question_id, a.answer_id, a.name, a.content, a.parent_id, a.create_time from (select ' \
              f'answer_id, name, content, parent_id, create_time from comments where url_token="{user_id}" ' \
              f'order by create_time desc limit 15 offset {page}) a left join simple_answer b on a.answer_id ' \
              f'= b.answer_id group by b.question_id, a.answer_id, a.name, a.content, a.parent_id, a.create_time;'
        count = f'select count(1) from comments where url_token="{user_id}";'
    else:
        sql = f'select b.question_id, a.answer_id, a.name, a.content, a.parent_id, a.create_time from (select ' \
              f'answer_id, name, content, parent_id, create_time from comments where commenter_id="{user_id}" ' \
              f'order by create_time desc limit 15 offset {page}) a left join simple_answer b on a.answer_id ' \
              f'= b.answer_id group by b.question_id, a.answer_id, a.name, a.content, a.parent_id, a.create_time;'
        count = f'select count(1) from comments where commenter_id="{user_id}";'

    try:
        cursor.execute(count)
        total_page = cursor.fetchall()
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        return None, None
    del cursor, con
    return results, total_page[0][0]


def get_key_word(venture, key_word, page):
    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'),
                          password=getServer('db_pwd'), database=getServer('db_name'))
    cursor = con.cursor()
    if venture == '100':
        sql = f'select question_id, answer_id, name, content, create_time, update_time from simple_answer where code in (100, 101, 102, 103, 104) and content like "%{key_word}%" order by update_time desc limit 15 offset {page};'
        count = f'select count(1) from simple_answer where code in (100, 101, 102, 103, 104) and content like "%{key_word}%";'
    else:
        sql = f'select question_id, answer_id, name, content, create_time, update_time from simple_answer where code={venture} and content like "%{key_word}%" order by update_time desc limit 15 offset {page};'
        count = f'select count(1) from simple_answer where code={venture} and content like "%{key_word}%";'
    try:
        cursor.execute(count)
        total_page = cursor.fetchall()
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        return None, None
    del cursor, con
    return results, total_page[0][0]


def get_forum(page, search_type = 'time', order_type = 'desc'):
    count = f"select count(1) from forum where parent_id = '';"
    time_sql = "( SELECT id, parent_id, user_id, content, create_time FROM forum WHERE parent_id = '' ORDER BY ' \
          'create_time {} LIMIT 10 OFFSET {} ) UNION ALL (SELECT b.id, b.parent_id, b.user_id, b.content, ' \
          'b.create_time FROM ( SELECT id FROM forum WHERE parent_id = '' ORDER BY create_time {} LIMIT 10 ' \
          'OFFSET {} ) a LEFT JOIN forum b ON a.id = b.parent_id );"

    hot_sql = "( SELECT c.id, c.parent_id, c.user_id, c.content, c.create_time FROM (SELECT b.parent_id FROM ( " \
              "SELECT parent_id, count( parent_id ) num FROM forum WHERE parent_id != '' GROUP BY parent_id ) b " \
              "ORDER BY b.num {} LIMIT 10 OFFSET {} ) a LEFT JOIN forum c ON a.parent_id = c.id ) UNION ALL (" \
              "SELECT c.id, c.parent_id, c.user_id, c.content, c.create_time FROM (SELECT b.parent_id FROM ( " \
              "SELECT parent_id, count( parent_id ) num FROM forum WHERE parent_id != '' GROUP BY parent_id ) " \
              "b ORDER BY b.num {} LIMIT 10 OFFSET {} ) a LEFT JOIN forum c ON a.parent_id = c.parent_id );"

    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'),
                          password=getServer('db_pwd'), database=getServer('db_name'))
    cursor = con.cursor()
    cursor.execute(count)
    total_page = cursor.fetchall()
    if search_type == 'time':
        cursor.execute(time_sql.format(order_type, page, order_type, page))
        results = cursor.fetchall()

    if search_type == 'hot':
        cursor.execute(hot_sql.format(order_type, page, order_type, page))
        results = cursor.fetchall()
