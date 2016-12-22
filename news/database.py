# -*- coding: utf-8 -*-

import psycopg2
from private_settings import POSTGRESQL_CONFIG


class Database(object):
    """
    """

    conn = psycopg2.connect(host=POSTGRESQL_CONFIG["host"], port=POSTGRESQL_CONFIG["port"], user=POSTGRESQL_CONFIG["user"],
                            password=POSTGRESQL_CONFIG["password"], database=POSTGRESQL_CONFIG["database"])

    def __init__(self):
        pass

    @staticmethod
    def find_dup(href):
        with Database.conn:
            with Database.conn.cursor() as cur:
                sql = "SELECT href FROM news_source WHERE href = %s"
                cur.execute(sql, (href, ))
                row = cur.fetchone()
                if row:
                    return True
        return False

    @staticmethod
    def insert(item):
        with Database.conn:
            with Database.conn.cursor() as cur:
                sql = "INSERT INTO news_source (title, pubtime, htmlcontent, keywords, source, images, href) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                args = (item["title"], item["pubtime"], item["htmlcontent"], item["keywords"], item["source"], item["images"], item["href"])
                cur.execute(sql, args)
