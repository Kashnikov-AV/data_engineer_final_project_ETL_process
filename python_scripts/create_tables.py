import os
import psycopg2
from sql_scripts.sql_ddl import *

# заполнение таблицы meta files
# get current directory
def create_tables():
    try:
        conn_edu = psycopg2.connect(database="edu",
                                    host="de-edu-db.chronosavant.ru",
                                    user="deaian",
                                    password="sarumanthewhite",
                                    port="5432")
        print("подключение к базам выполнено")
    except Exception as e:
        print(e)
        exit()
    conn_edu.autocommit = False
    cursor_edu = conn_edu.cursor()

    try:
        cursor_edu.execute(SQL_DDL)
        conn_edu.commit()
        print('Таблицы созданы')
    except Exception as e:
        print(e)

    cursor_edu.close()
    conn_edu.close()
    print('connections close')

if __name__ == "__main__":
    create_tables()