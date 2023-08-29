import sqlite3
from threading import Lock
lock = Lock()


def exec_querry(sql):
    try:
        lock.acquire()
        sqliteConn = sqlite3.connect('devices.db')
        cursor = sqliteConn.cursor()
        cursor.execute(sql)
        sqliteConn.commit()
    except sqlite3.Error as error:
        print(error)
    finally:
        if sqliteConn:
            sqliteConn.close()
            lock.release()


def lista_db(sql):
    try:
        lock.acquire()
        sqliteConn = sqlite3.connect('devices.db')
        cursor = sqliteConn.cursor()
        cursor.execute(sql)
        sqliteConn.commit()
        return cursor.fetchall()
    except sqlite3.Error as error:
        print(error)
    finally:
        if sqliteConn:
            sqliteConn.close()
            lock.release()
