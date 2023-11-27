SQL_INSERT_STG_TRANSACTIONS = """
INSERT INTO deaian.kshn_stg_transactions(
    trans_id,
    trans_date,
    amt,
    card_num,
    oper_type,
    oper_result,
    terminal
 )
VALUES(%s, %s, %s, %s, %s, %s, %s)"""
                            
SQL_INSERT_STG_TERMINALS = """
INSERT INTO deaian.kshn_stg_terminals(
    terminal_id,
    terminal_type,
    terminal_city,
    terminal_address
)
VALUES(%s, %s, %s, %s)"""
                        
SQL_INSERT_STG_BLACK_LIST = """
INSERT INTO deaian.kshn_stg_blacklist(
    entry_dt,
    passport_num
)
VALUES(%s, %s)"""

SQL_INSERT_STG_CLIENTS = """
INSERT INTO deaian.kshn_stg_clients(
    client_id,
	last_name,
	first_name,
	patronymic,
	date_of_birth,
	passport_num,
	passport_valid_to,
	phone,
	create_dt,
	update_dt
)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

SQL_INSERT_STG_CARDS = """INSERT INTO deaian.kshn_stg_cards(
	card_num,
	account_num,
	create_dt,
	update_dt
)
VALUES(%s, %s, %s, %s)"""

SQL_INSERT_STG_ACCOUNTS = """INSERT INTO deaian.kshn_stg_accounts(
	account_num,
	valid_to,
	client,
	create_dt,
	update_dt
)
VALUES(%s, %s, %s, %s, %s)"""