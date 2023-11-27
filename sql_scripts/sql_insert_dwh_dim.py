SQL_INSERT_DWH_DIM_TERMINALS = """
insert into deaian.kshn_dwh_dim_terminals ( terminal_id, terminal_type, terminal_city, terminal_address, create_dt, update_dt, processed_dt )
select
	stg.terminal_id, 
	stg.terminal_type, 
	stg.terminal_city,
	stg.terminal_address,
	now(),
	null, 
	now() 
from deaian.kshn_stg_terminals stg
left join deaian.kshn_dwh_dim_terminals dwh
on stg.terminal_id = dwh.terminal_id
where dwh.terminal_id is null;
"""
SQL_INSERT_DWH_DIM_CARDS = """
insert into deaian.kshn_dwh_dim_cards ( card_num, account_num, create_dt, update_dt, processed_dt )
select
	stg.card_num, 
	stg.account_num, 
	now(),
	stg.update_dt,
	now()
from deaian.kshn_stg_cards stg
left join deaian.kshn_dwh_dim_cards dwh
on stg.card_num = dwh.card_num
where dwh.card_num is null;
"""
SQL_INSERT_DWH_DIM_ACCOUNTS = """
insert into deaian.kshn_dwh_dim_accounts ( account_num, valid_to, client, create_dt, update_dt, processed_dt )
select
	stg.account_num, 
	stg.valid_to, 
	stg.client,
	now(),
	stg.update_dt,
	now()
from deaian.kshn_stg_accounts stg
left join deaian.kshn_dwh_dim_accounts dwh
on stg.account_num = dwh.account_num
where dwh.account_num is null;
"""
SQL_INSERT_DWH_DIM_CLIENTS = """
insert into deaian.kshn_dwh_dim_clients ( client_id, last_name, first_name, patronymic, date_of_birth, passport_num, passport_valid_to, phone, create_dt, update_dt, processed_dt )
select
	stg.client_id,
    stg.last_name,
    stg.first_name,
    stg.patronymic,
    stg.date_of_birth,
    stg.passport_num,
    stg.passport_valid_to,
    stg.phone,
    now(),
    stg.update_dt,
	now()
from deaian.kshn_stg_clients stg
left join deaian.kshn_dwh_dim_clients dwh
on stg.client_id = dwh.client_id
where dwh.client_id is null;
"""