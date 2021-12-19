#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import time
import queue
import threading
import pymysql
from common.config import getServer
from common.logger import logger


insert_sql = "insert into access (ip, traffic, access_time) values ('{}', {}, '{}');"
select_sql = "select ip, traffic from access where ip = '{}';"
update_sql = "update access set traffic = {}, access_time = '{}' where ip = '{}';"

user_agent_insert_sql = "insert into user_agent (ip, user_agent, traffic) values ('{}', '{}', {});"
user_agent_select_sql = "select id, ip, traffic from user_agent where ip = '{}' and user_agent = '{}';"
user_agent_update_sql = "update user_agent set traffic = {} where id = {};"

class IPQueue:
    def __init__(self):
        self.q = queue.Queue()

        self.con = None
        self.cursor = None

        self.task()

    def put_queue(self, value):
        self.q.put(value)

    def connect_sql(self):
        self.con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'), port=int(getServer('db_port')),
                              password=getServer('db_pwd'), database=getServer('db_name'))
        self.cursor = self.con.cursor()

    def task(self):
        t = threading.Thread(target=self.write_sql_task)
        t.setDaemon(True)
        t.start()

    def write_sql_task(self):
        while True:
            if self.q.qsize() > 20:
                self.connect_sql()
                while True:
                    if not self.q.empty():
                        param = self.q.get()
                        if len(param) == 2:
                            self.write_sql(param)
                        else:
                            self.write_agent_sql(param)
                    else:
                        break
                del self.cursor, self.con
            else:
                logger.info(f'The current size of queue is {self.q.qsize()}.')
                time.sleep(6)

    def write_sql(self, value):
        res = self.execute(select_sql.format(value[0]))
        if res:
            num = res[0][1]
            self.execute(update_sql.format(num + 1, value[1], value[0]), is_commit=True)
        else:
            self.execute(insert_sql.format(value[0], 1, value[1]), is_commit=True)

    def execute(self, sql, is_commit = False):
        self.cursor.execute(sql)
        if is_commit:
            self.con.commit()
            return None
        else:
            return self.cursor.fetchall()

    def write_agent_sql(self, value):
        res = self.execute(user_agent_select_sql.format(value[0], value[1]))
        if res:
            num = res[0][2]
            self.execute(user_agent_update_sql.format(num + 1, res[0][0]), is_commit=True)
        else:
            self.execute(user_agent_insert_sql.format(value[0], value[1], 1), is_commit=True)
