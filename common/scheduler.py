#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import time
import threading
import pymysql
from common.config import getServer
from common.logger import logger


class Schedule:
    def __init__(self):
        self.con = None
        self.cursor = None
        self.res = None

        self.sql = "select a.id, b.hash from (select max(id) id, answer_id from simple_answer where hash is not null " \
                   "group by answer_id) a left join simple_answer b on a.id = b.id"

    def connect(self):
        self.con = pymysql.connect(host=getServer('db_host'), user=getServer('db_user'), port=int(getServer('db_port')),
                              password=getServer('db_pwd'), database=getServer('db_name'))
        self.cursor = self.con.cursor()

    def get_result(self):
        try:
            self.connect()
            self.cursor.execute(self.sql)
            self.res = self.cursor.fetchall()
        except Exception as err:
            logger.info(err)
        del self.cursor, self.con
