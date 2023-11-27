import os
from datetime import date
import psycopg2
import pandas as pd

#заполнение таблицы meta files
# get current directory
def create_meta_files():
    path = os.getcwd() 
    file_list = []
    for file in os.listdir(os.path.abspath(os.path.join(path, os.pardir))):
        if file.find('transact') != -1:
            file_list.append(file[13:21])
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
        for row in file_list:
            print(row)
            cursor_edu.execute(f"insert into deaian.kshn_meta_files( file ) values ({'0' + row});")
            conn_edu.commit()
        print('данные загружены')
    except Exception as e:
        print(e)

    cursor_edu.close()
    conn_edu.close()
    print('connections close')

if __name__ == "__main__":
    create_meta_files()
