# -*- coding: utf-8 -*-
import config
import psycopg2
from datetime import datetime

def GetWordDB(word):

    conn = psycopg2.connect(
        database = config.database,
        user = config.user,
        password = config.password,
        host = config.host,
        port=config.port)
    cursor = conn.cursor()
    slowo = word
    start = len(slowo) + 1
    end = len(slowo) - 1
    cursor.execute(""" SELECT word 
                       FROM public.words
                       WHERE LENGTH(word)<= %s AND LENGTH(word)>= %s
                       ORDER BY 1;""",
                   (start, end,))
    res = cursor.fetchall()

    result = []
    j = 0
    for i in res:
        if res[j][0].lower() != word:
            result.append(res[j][0])
        j += 1
    conn.close()
    return result


def GetRating():
    conn = psycopg2.connect(
        database=config.database,
        user=config.user,
        password=config.password,
        host=config.host,
        port=config.port)
    cursor = conn.cursor()
    cursor.execute(""" 
                    SELECT glossary, valuation
                    FROM public.rating;
                    """)
    res = cursor.fetchall()
    result = []
    j = 0
    for el in res:
        a = (res[j][0]).split()[0]
        b = int(res[j][1])
        result.append([a, b])
        j += 1
    conn.close()
    return result

def CheckUpdates():
    conn = psycopg2.connect(
        database=config.database,
        user=config.user,
        password=config.password,
        host=config.host,
        port=config.port)
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT update_date 
                   FROM public.last_update;
                   """)
    res = cursor.fetchall()
    last_update = datetime.strptime(datetime.strftime(res[0][0], '%Y-%m-%d'), '%Y-%m-%d')
    now = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d'), '%Y-%m-%d')
    upd = datetime.now()
    if now != last_update:
        if int(str(now - last_update)[0:2]) >= 30:
            NullRating()
    cursor.execute(""" 
                   UPDATE public.last_update
                   SET update_date = %s;""",
                   (upd,))
    conn.close()


def NullRating():
    conn = psycopg2.connect(
        database=config.database,
        user=config.user,
        password=config.password,
        host=config.host,
        port=config.port)
    cursor = conn.cursor()
    cursor.execute(""" 
                   SELECT glossary, last_date 
                   FROM public.rating;""")
    res = cursor.fetchall()
    result = []
    j = 0
    for el in res:
        a = (res[j][0]).split()[0]
        b = str(res[j][1])
        j += 1
        result.append([a, b])

    for el in range(len(result)):
        last = datetime.strptime(result[el][1], '%Y-%m-%d')
        now = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d'), '%Y-%m-%d')
        upd = datetime.now()
        if now != last:
            if int(str(now - last)[0:2]) >= 30:
                UpdateRating(result[el][0], 7, upd)
    conn.close()

def UpdateRating(dict, val, date):
    conn = psycopg2.connect(
        database=config.database,
        user=config.user,
        password=config.password,
        host=config.host,
        port=config.port)
    cursor = conn.cursor()
    if val != 7:
        cursor.execute("""
                       UPDATE public.rating
                       SET valuation = valuation + %s, last_date = %s
                       WHERE glossary = %s;""",
                       (val, date, dict,))
    else:
        cursor.execute("""
                      UPDATE public.rating
                      SET valuation = 0, last_date = %s
                      WHERE glossary = %s;""",
                      (val, date, dict,))
    conn.commit()
    conn.close()


