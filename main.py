#!/bin/python3
import os
from datetime import date
import psycopg2
import pandas as pd
from pprint import pprint
from sql_scripts.sql_insert_stg import *
from sql_scripts.sql_insert_dwh_dim import *
from sql_scripts.sql_report import *

# подключение к базам данных
try:
    conn_edu = psycopg2.connect(database="edu",
                                host="de-edu-db.chronosavant.ru",
                                user="deaian",
                                password="sarumanthewhite",
                                port="5432")
    
    conn_bank = psycopg2.connect(database = "bank",
                                host="de-edu-db.chronosavant.ru",
                                user="bank_etl",
                                password="bank_etl_password",
                                port="5432")
    print("подключение к базам выполнено")
except Exception as e:
    print(e)
    exit()
# Отключение автокоммита
conn_edu.autocommit = False
conn_bank.autocommit = False

# Создание курсора
cursor_edu = conn_edu.cursor()
cursor_bank = conn_bank.cursor()

# достаем дату для файлов из meta
cursor_edu.execute(
"""
select LPAD(file, 8, '0')
from deaian.kshn_meta_files
order by file
limit 1;
"""
)
str_dt = cursor_edu.fetchone()
str_dt = str_dt[0]
cursor_edu.execute(
"""
delete from deaian.kshn_meta_files 
where file = (
	select file 
	from deaian.kshn_meta_files
	order by file
	limit 1
)
"""
)
conn_edu.commit()
#---------------------------------------------
# формируем имена загружаемых файлов
password_black_list = f'passport_blacklist_{ str_dt }.xlsx'
terminals = f'terminals_{ str_dt }.xlsx'
transactions = f'transactions_{ str_dt }.txt'

# формируем полный путь до файлов
path_password_black_list = os.path.abspath(password_black_list)
path_terminals = os.path.abspath(terminals)
path_transactions = os.path.abspath(transactions)

# создаем датафреймы pandas для каждой таблицы
df_password_black_list = pd.read_excel(path_password_black_list)
df_terminals = pd.read_excel(path_terminals)
df_transactions = pd.read_csv(path_transactions, sep=";", decimal=',')
df_transactions['transaction_id'] = df_transactions['transaction_id'].astype('str')
#df clients
cursor_bank.execute( "select * from info.clients" )
records = cursor_bank.fetchall()
names = [ x[0] for x in cursor_bank.description ]
df_clients = pd.DataFrame( records, columns=names )
#df cards
cursor_bank.execute( "select * from info.cards" )
records = cursor_bank.fetchall()
names = [ x[0] for x in cursor_bank.description ]
df_cards = pd.DataFrame( records, columns=names )
#df accounts
cursor_bank.execute( "select * from info.accounts" )
records = cursor_bank.fetchall()
names = [ x[0] for x in cursor_bank.description ]
df_accounts = pd.DataFrame( records, columns=names )

#данные для работы с stg
df_list = [
    (df_transactions, SQL_INSERT_STG_TRANSACTIONS, 'kshn_stg_transactions', 'edu'),
    (df_terminals, SQL_INSERT_STG_TERMINALS, 'kshn_stg_terminals', 'edu'),
    (df_password_black_list, SQL_INSERT_STG_BLACK_LIST, 'kshn_stg_blacklist', 'edu'),
    (df_clients, SQL_INSERT_STG_CLIENTS, 'kshn_stg_clients', 'bank'),
    (df_accounts, SQL_INSERT_STG_ACCOUNTS, 'kshn_stg_accounts', 'bank'),
    (df_cards, SQL_INSERT_STG_CARDS, 'kshn_stg_cards', 'bank'),
    ] 



# Очистка stg
cursor_edu.execute("""delete from deaian.kshn_stg_transactions;""")
cursor_edu.execute("""delete from deaian.kshn_stg_terminals;""")
cursor_edu.execute("""delete from deaian.kshn_stg_blacklist;""")
cursor_edu.execute("""delete from deaian.kshn_stg_cards;""")
cursor_edu.execute("""delete from deaian.kshn_stg_accounts;""")
cursor_edu.execute("""delete from deaian.kshn_stg_clients;""")
print('stg delete done')

# загрузка данных по 1000 записей в stg
step = 1000
iter_list = None    
for df in df_list:
    pprint(df[0].head())
    if df[0].shape[0] > step:
        iter_list  = list(range(0, df[0].shape[0], step))
        if df[0].shape[0] % step != 0:
            last_item = iter_list[-1::][0] + df[0].shape[0] % step
            iter_list.append(last_item)
    else:
        iter_list = [0, df[0].shape[0]]
        
    for i, chunk in enumerate(iter_list[0:-1]):
        try:
            cursor_edu.executemany(df[1], df[0].values.tolist()[iter_list[i]:iter_list[i+1]])
            if df[3] == 'edu':
                conn_edu.commit()
            if df[3] == 'bank':
                conn_bank.commit()
            print(f"insert to {df[2]} completed, chunk {iter_list[i+1]}")
        except Exception as e:
            print(e)

# Загрузка данных в фактовые таблицы
cursor_edu.execute("""
INSERT INTO deaian.kshn_dwh_fact_transactions
SELECT * FROM deaian.kshn_stg_transactions""")
cursor_edu.execute("""
insert into deaian.kshn_dwh_fact_passport_blacklist (passport_num, entry_dt )
select
	stg.passport_num, 
	stg.entry_dt
from deaian.kshn_stg_blacklist stg
left join deaian.kshn_dwh_fact_passport_blacklist dwh
on stg.passport_num = dwh.passport_num
where dwh.passport_num is null;
""")
print('таблицы фактов заполнены')
# загрузка данных в таблицы измерений
cursor_edu.execute(SQL_INSERT_DWH_DIM_TERMINALS)
cursor_edu.execute(SQL_INSERT_DWH_DIM_CARDS)
cursor_edu.execute(SQL_INSERT_DWH_DIM_ACCOUNTS)
cursor_edu.execute(SQL_INSERT_DWH_DIM_CLIENTS)
print('таблицы измерений заполнены')

#файлы складываем в архив
os.rename(path_password_black_list, f'archive/{password_black_list}.backup')
os.rename(path_terminals, f'archive/{terminals}.backup')
os.rename(path_transactions, f'archive/{transactions}.backup')
print('файлы отправлены в архив')

# построение отчета
cursor_edu.execute(SQL_REPORT_1)
cursor_edu.execute(SQL_REPORT_2)

conn_edu.commit()
conn_bank.commit()
print('commits done')

cursor_edu.close() 
cursor_bank.close()

conn_edu.close()
conn_bank.close()
print('connections close')




