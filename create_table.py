import sqlite3
import __exec_sql

def create_db():
    __exec_sql.exec_querry(f"CREATE TABLE IF NOT EXISTS device_list (devices varchar(40), status varchar(15), user varchar(40), lock varchar(2), type varchar(15))")
    __exec_sql.exec_querry(f"CREATE TABLE IF NOT EXISTS last_update (time varchar(16))")
    __exec_sql.exec_querry(f"DELETE FROM last_update")
    __exec_sql.exec_querry(f"INSERT INTO last_update(time) VALUES ('None')")
