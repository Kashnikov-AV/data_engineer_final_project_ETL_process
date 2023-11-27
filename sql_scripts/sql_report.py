SQL_REPORT_2 = """
with t_dim as (
	select
		ac.account_num,
		ac.client,
		ac.valid_to,
		cl.last_name,
		cl.first_name,
		cl.patronymic,
		cl.passport_num,
		cl.phone,
		ca.card_num 
	from deaian.kshn_dwh_dim_cards ca
	left join deaian.kshn_dwh_dim_accounts ac
	on ca.account_num  = ac.account_num 
	left join deaian.kshn_dwh_dim_clients cl
	on cl.client_id  = ac.client  
),
t_res as (
select 
	t_dim.*,
	tr.trans_id, 
	tr.card_num,
	tr.trans_date::date
from deaian.kshn_dwh_fact_transactions tr
left join t_dim
on t_dim.card_num = tr.card_num 
where tr.trans_date::date > t_dim.valid_to
)

insert into deaian.kshn_rep_fraud_tmp 
select
	trans_date event_dt,
	passport_num passport,
	first_name || ' ' || last_name || ' ' || patronymic fio,
	phone,
	2 event_type,
	now()::date report_dt 
from t_res;

insert into deaian.kshn_rep_fraud ( event_dt, passport, fio, phone, event_type, report_dt )
select 
	tmp.event_dt, 
	tmp.passport, 
	tmp.fio, 
	tmp.phone, 
	tmp.event_type, 
	tmp.report_dt
from deaian.kshn_rep_fraud_tmp tmp
left join deaian.kshn_rep_fraud fr
on tmp.passport = fr.passport and tmp.event_dt = fr.event_dt
where fr.passport is null;

delete from deaian.kshn_rep_fraud_tmp;
"""
SQL_REPORT_1 = """
with t_dim as (
	select
		ac.account_num,
		ac.client,
		ac.valid_to,
		cl.last_name,
		cl.first_name,
		cl.patronymic,
		cl.passport_num pn,
		cl.passport_valid_to,
		cl.phone,
		ca.card_num 
	from deaian.kshn_dwh_dim_cards ca
	left join deaian.kshn_dwh_dim_accounts ac
	on ca.account_num  = ac.account_num 
	left join deaian.kshn_dwh_dim_clients cl
	on cl.client_id  = ac.client  
),
t_full as (
select 
	t_dim.*,
	tr.trans_id, 
	tr.card_num,
	tr.trans_date
from deaian.kshn_dwh_fact_transactions tr
left join t_dim
on t_dim.card_num = tr.card_num 
),
t_res as (
select 
*
from t_full
left join kshn_dwh_fact_passport_blacklist pbl
on t_full.pn = pbl.passport_num
where pbl.passport_num is not null or t_full.trans_date > t_full.passport_valid_to
)
insert into deaian.kshn_rep_fraud_tmp 
select
	trans_date event_dt,
	pn passport,
	first_name || ' ' || last_name || ' ' || patronymic fio,
	phone,
	1 event_type,
	now()::date report_dt 
from t_res;

insert into deaian.kshn_rep_fraud ( event_dt, passport, fio, phone, event_type, report_dt )
select 
	tmp.event_dt, 
	tmp.passport, 
	tmp.fio, 
	tmp.phone, 
	tmp.event_type, 
	tmp.report_dt
from deaian.kshn_rep_fraud_tmp tmp
left join deaian.kshn_rep_fraud fr
on tmp.passport = fr.passport and tmp.event_dt = fr.event_dt
where fr.passport is null;

delete from deaian.kshn_rep_fraud_tmp;
"""