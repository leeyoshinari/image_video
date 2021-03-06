#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import traceback
import pymysql
from common.config import getServer
from common.scheduler import Schedule
from common.simhash import hamming_distance, cal_percentage
from common.logger import logger


sch = Schedule()
browser_dict = {'Chrome': 'Chrome', 'Edge': 'Edge', 'ZhihuHybrid': '知乎内置浏览器', 'MetaSr': '搜狗',
                'MiuiBrowser': '小米', 'MicroMessenger': '微信内置浏览器', 'QQBrowser': 'QQBrowser', 'IE': 'IE',
                'Firefox': 'Firefox', 'Safari': 'Safari', 'Baidu': '百度浏览器', 'HuaweiBrowser': 'HuaweiBrowser'}


def get_answer(answer_id, page):
    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'), port=int(getServer('db_port')),
                          password=getServer('db_pwd'), database=getServer('db_name'))
    cursor = con.cursor()
    sql = f'select question_id, answer_id, name, content, create_time, update_time from simple_answer where answer_id="{answer_id}" order by update_time desc limit 15 offset {page};'
    count = f'select count(1) from simple_answer where answer_id="{answer_id}";'
    try:
        cursor.execute(count)
        total_page = cursor.fetchall()
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        logger.error(traceback.format_exc())
        del cursor, con
        return None, 0
    del cursor, con
    return results, total_page[0][0]


def get_d_answer(answer_id):
    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'), port=int(getServer('db_port')),
                          password=getServer('db_pwd'), database=getServer('db_name'))
    cursor = con.cursor()
    sql = f'select question_id, answer_id, name, content, create_time, update_time from answers where answer_id="{answer_id}" order by update_time desc;'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        logger.error(traceback.format_exc())
        del cursor, con
        return None, 0
    del cursor, con
    return results


def get_comment(user_id, page):
    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'), port=int(getServer('db_port')),
                          password=getServer('db_pwd'), database=getServer('db_name'))
    cursor = con.cursor()
    if '-' in user_id or len(user_id) < 22:
        sql = f'select answer_id, name, content, comment_id, parent_id, create_time from comments where ' \
              f'url_token="{user_id}" order by create_time desc limit 15 offset {page};'
        count = f'select count(1) from comments where url_token="{user_id}";'
    else:
        sql = f'select answer_id, name, content, comment_id, parent_id, create_time from comments where ' \
              f'commenter_id="{user_id}" order by create_time desc limit 15 offset {page};'
        count = f'select count(1) from comments where commenter_id="{user_id}";'

    try:
        cursor.execute(count)
        total_page = cursor.fetchall()
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        logger.error(traceback.format_exc())
        del cursor, con
        return None, 0
    del cursor, con
    return results, total_page[0][0]


def get_d_comment(answer_id):
    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'), port=int(getServer('db_port')),
                          password=getServer('db_pwd'), database=getServer('db_name'))
    cursor = con.cursor()
    sql = f'select answer_id, name, content, comment_id, parent_id, commenter_id, create_time from comments where ' \
          f'answer_id="{answer_id}" and parent_id ="" order by create_time desc;'

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        logger.error(traceback.format_exc())
        del cursor, con
        return None, 0
    del cursor, con
    return results


def get_comment_by_id(comment_id):
    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'), port=int(getServer('db_port')),
                          password=getServer('db_pwd'), database=getServer('db_name'))
    cursor = con.cursor()
    sql = f"select name, content, create_time from comments where comment_id = '{comment_id}' or parent_id = '{comment_id}' order by create_time;"

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception as err:
        logger.error(traceback.format_exc())
        del cursor, con
        raise Exception(err)
    del cursor, con
    return results


def delete_comment_by_id(comment_id):
    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'), port=int(getServer('db_port')),
                          password=getServer('db_pwd'), database=getServer('db_name'))
    cursor = con.cursor()
    sql = f"delete from comments where comment_id = '{comment_id}';"
    sql1 = f"delete from comments where parent_id = '{comment_id}';"

    try:
        cursor.execute(sql)
        cursor.execute(sql1)
        con.commit()
    except Exception as err:
        logger.error(traceback.format_exc())
        del cursor, con
        raise Exception(err)
    del cursor, con


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
    except:
        logger.error(traceback.format_exc())
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

    sql = f'select id, hash from simple_answer where answer_id="{answer_id}" order by update_time desc limit 1;'
    select_sql = 'select id, question_id, answer_id, name, content, create_time, update_time from simple_answer where id in {};'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if not results:
            del cursor, con
            return None, 0

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
    except:
        logger.error(traceback.format_exc())
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

        if search_type == 'hotttt':
            cursor.execute(hot_sql.format(order_type, page, order_type, page))
            results = cursor.fetchall()
    except:
        logger.error(traceback.format_exc())
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
        logger.error(traceback.format_exc())
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
        logger.error(traceback.format_exc())
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
    except:
        logger.error(traceback.format_exc())
        del cursor, con
        return None
    del cursor, con
    return results


def get_pie():
    pv_sql = "select traffic from access where province is null and ip != 'None';"
    puv_sql = "select ip, user_agent, traffic from user_agent where os is null order by id desc;"
    os_sql = "select os, count(os) from user_agent where os is not null group by os;"
    browser_sql = "select browser, count(browser) from user_agent where browser is not null group by browser;"
    mobile_sql = "select mobile, count(mobile) from user_agent where mobile is not null group by mobile;"
    net_sql = "select type, count(type) from access where type is not null group by type;"
    map_sql = "select province, city, district, sum(traffic) from access where province is not null group by province, city, district;"
    con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'), port=int(getServer('db_port')),
                          password=getServer('db_pwd'), database=getServer('db_name'))
    cursor = con.cursor()
    try:
        cursor.execute(pv_sql)
        pv_results = cursor.fetchall()
        cursor.execute(puv_sql)
        puv_results = cursor.fetchall()
        cursor.execute(browser_sql)
        browser_results = cursor.fetchall()
        cursor.execute(os_sql)
        os_results = cursor.fetchall()
        cursor.execute(mobile_sql)
        mobile_results = cursor.fetchall()
        cursor.execute(net_sql)
        net_results = cursor.fetchall()
        cursor.execute(map_sql)
        map_results = cursor.fetchall()
    except:
        logger.error(traceback.format_exc())
        del cursor, con
        return None
    del cursor, con
    pv = [r[0] for r in pv_results]
    browser = [{'name': browser_dict[r[0]], 'value': r[1]} for r in browser_results]
    os = [{'name': r[0], 'value': r[1]} for r in os_results]
    mobile = [{'name': r[0], 'value': r[1]} for r in mobile_results]
    net = [{'name': r[0], 'value': r[1]} for r in net_results]
    return {'pv': pv, 'browser': browser, 'os': os, 'mobile': mobile, 'net': net,
            'puv': deal_puv(puv_results), 'map': deal_map(map_results)}


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


def deal_puv(result):
    x_line = []
    uv_line = []
    pv_line = []
    for r in result:
        x_line.append(r[0])
        if r[1] == 'pv':
            pv_line.append(r[2])
        else:
            uv_line.append(r[2])
    axis = list(set(x_line))
    axis.sort()
    pv_line.reverse()
    uv_line.reverse()
    return {'xaxis': axis, 'pv': pv_line, 'uv': uv_line}


def deal_map(result):
    res = {}
    for r in result:
        if res.get(r[0]):
            res[r[0]]['value'] = res[r[0]]['value'] + int(r[3])
        else:
            res.update({r[0]: {"name": r[0], "value": int(r[3]), "child": {}}})
        if r[1]:
            if res[r[0]]['child'].get(r[1]):
                res[r[0]]['child'][r[1]]['value'] = res[r[0]]['child'][r[1]]['value'] + int(r[3])
            else:
                res[r[0]]['child'].update({r[1]: {"name": r[1], "value": int(r[3]), "child": {}}})
        if r[2]:
            res[r[0]]['child'][r[1]]['child'].update({r[2]: {"name": r[2], "value": int(r[3])}})

    return res
