# -*- coding: utf-8 -*-
import pymysql
import config.config as conf


def connect_db():
    cfg = conf.config_parser()
    return pymysql.connect(
        cfg.get("database", "database.ip"),
        cfg.get("database", "database.user"),
        cfg.get("database", "database.password"),
        cfg.get("database", "database.name")
    )


def insert_batch(sql, params):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.executemany(sql, params)
        conn.commit()
    except:
        conn.rollback()
    conn.close()


def update(sql):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    conn.close()


def select(sql):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.close()
    return data


if __name__ == '__main__':
    data = select("select count(1) from book_crawler")
    print(data)

