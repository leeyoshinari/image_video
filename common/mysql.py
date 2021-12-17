#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import pymysql
from common.config import getServer
from common.scheduler import Schedule
from common.simhash import hamming_distance, cal_percentage
from common.logger import logger


sch = Schedule()

def get_answer(answer_id, page):
    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'), port=int(getServer('db_port')),
                          password=getServer('db_pwd'), database=getServer('db_name'))
    cursor = con.cursor()
    sql = f'select question_id, answer_id, name, content, create_time, update_time from simple_answer where answer_id={answer_id} order by update_time desc limit 15 offset {page};'
    count = f'select count(1) from simple_answer where answer_id={answer_id};'
    try:
        cursor.execute(count)
        total_page = cursor.fetchall()
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception as err:
        logger.info(err)
        del cursor, con
        return None, 0
    del cursor, con
    return results, total_page[0][0]


def get_comment(user_id, page):
    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'), port=int(getServer('db_port')),
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
    except Exception as err:
        logger.info(err)
        del cursor, con
        return None, 0
    del cursor, con
    return results, total_page[0][0]


def get_key_word(venture, key_word, page):
    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'), port=int(getServer('db_port')),
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
    except Exception as err:
        logger.info(err)
        del cursor, con
        return None, 0
    del cursor, con
    return results, total_page[0][0]


def get_similarity(answer_id, page, is_init = False):
    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'), port=int(getServer('db_port')),
                          password=getServer('db_pwd'), database=getServer('db_name'))
    cursor = con.cursor()

    if is_init:
        sch.get_result()

    sql = f'select id, hash from simple_answer where answer_id={answer_id} order by update_time desc limit 1;'
    select_sql = 'select id, question_id, answer_id, name, content, create_time, update_time from simple_answer where id in {};'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        hash1 = results[0][1]

        res_list = []
        for r in sch.res:
            hamming = hamming_distance(int(hash1), int(r[1]))
            if hamming < 9:
                res_list.append([r[0], cal_percentage(hamming)])

        res_list.sort(key=lambda x: x[1], reverse=True)
        res_sorted = res_list[page: page + 15]
        ids = [x[0] for x in res_sorted]
        total_page = len(res_list)

        cursor.execute(select_sql.format(tuple(ids)))
        results = cursor.fetchall()
    except Exception as err:
        logger.info(err)
        del cursor, con
        return None, 0
    del cursor, con
    return merge_res(res_sorted, results), total_page


def get_forum(page, search_type = 'time', order_type = 'desc'):
    count = f"select count(1) from forum where parent_id = '';"
    time_sql = "( SELECT id, parent_id, user_id, content, create_time FROM forum WHERE parent_id = '' ORDER BY " \
          "create_time {} LIMIT 10 OFFSET {} ) UNION ALL (SELECT * FROM (SELECT b.id, b.parent_id, b.user_id, b.content, " \
          "b.create_time FROM ( SELECT id FROM forum WHERE parent_id = '' ORDER BY create_time {} LIMIT 10 OFFSET {} ) a LEFT JOIN " \
          "forum b ON a.id = b.parent_id ORDER BY b.create_time limit 99999) c where c.id IS NOT NULL);"

    hot_sql = "( SELECT c.id, c.parent_id, c.user_id, c.content, c.create_time FROM (SELECT b.parent_id FROM ( " \
              "SELECT parent_id, count( parent_id ) num FROM forum WHERE parent_id != '' GROUP BY parent_id ) b " \
              "ORDER BY b.num {} LIMIT 10 OFFSET {} ) a LEFT JOIN forum c ON a.parent_id = c.id ) UNION ALL (" \
              "SELECT c.id, c.parent_id, c.user_id, c.content, c.create_time FROM (SELECT b.parent_id FROM ( " \
              "SELECT parent_id, count( parent_id ) num FROM forum WHERE parent_id != '' GROUP BY parent_id ) " \
              "b ORDER BY b.num {} LIMIT 10 OFFSET {} ) a LEFT JOIN forum c ON a.parent_id = c.parent_id );"

    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'), port=int(getServer('db_port')),
                          password=getServer('db_pwd'), database=getServer('db_name'))
    cursor = con.cursor()
    try:
        cursor.execute(count)
        total_page = cursor.fetchall()
        if search_type == 'time':
            cursor.execute(time_sql.format(order_type, page, order_type, page))
            results = cursor.fetchall()

        if search_type == 'hot':
            cursor.execute(hot_sql.format(order_type, page, order_type, page))
            results = cursor.fetchall()
    except Exception as err:
        logger.info(err)
        del cursor, con
        return None, 0
    del cursor, con
    return deal_forum(results), total_page[0][0]


def add_comment(data):
    sql = "insert into forum (parent_id, user_id, content, create_time) values {};"
    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'), port=int(getServer('db_port')),
                          password=getServer('db_pwd'), database=getServer('db_name'))
    cursor = con.cursor()
    logger.info(sql.format(data))
    try:
        cursor.execute(sql.format(data))
        con.commit()
        del cursor, con
    except Exception as err:
        logger.error(err)
        del cursor, con
        raise Exception(err)

def add_connect(data):
    sql = "insert into message (ip, contact, content, create_time) values {};"
    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'), port=int(getServer('db_port')),
                          password=getServer('db_pwd'), database=getServer('db_name'))
    cursor = con.cursor()
    logger.info(sql.format(data))
    try:
        cursor.execute(sql.format(data))
        con.commit()
        del cursor, con
    except Exception as err:
        logger.error(err)
        del cursor, con
        raise Exception(err)


def get_contact():
    sql = "select * from message order by create_time desc;"
    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'), port=int(getServer('db_port')),
                          password=getServer('db_pwd'), database=getServer('db_name'))
    cursor = con.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception as err:
        logger.info(err)
        del cursor, con
        return None
    del cursor, con
    return results


def merge_res(res_sorted, all_res):
    result = []
    res_dict = dict(res_sorted)
    for x in all_res:
        xx = list(x)
        xx.append(res_dict[x[0]])
        result.append(xx)

    result.sort(key=lambda y: y[7], reverse=True)
    return result


def deal_forum(results):
    res = {}
    for r in results:
        if r[1]:
            res[str(r[1])]['child'].append({"id": r[0], "name": r[2], "content": r[3], "create_time": r[4]})
        else:
            res.update({str(r[0]): {"id": r[0], "name": r[2], "content": r[3], "create_time": r[4], "child": []}})
    return res
