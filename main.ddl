--ddl tables
create table if not exists deaian.kshn_stg_transactions(
	trans_id varchar(30),
	trans_date timestamp(0),
	card_num bpchar(20),
	oper_type varchar(30),
	amt decimal(18,2),
	oper_result varchar(30),
	terminal varchar(30)
);
create table if not exists deaian.kshn_stg_terminals(
	terminal_id varchar(30),
	terminal_type varchar(20),
	terminal_city varchar(50),
	terminal_address varchar(100)
);
create table if not exists deaian.kshn_stg_blacklist(
	passport_num varchar(15),
	entry_dt date
);
create table if not exists deaian.kshn_stg_cards(
	card_num bpchar(20) NULL,
	account_num bpchar(20) NULL,
	create_dt timestamp(0) NULL,
	update_dt timestamp(0) NULL
);
create table if not exists deaian.kshn_stg_accounts(
	account_num bpchar(20) NULL,
	valid_to date NULL,
	client varchar(10) NULL,
	create_dt timestamp(0) NULL,
	update_dt timestamp(0) NULL
);
create table if not exists deaian.kshn_stg_clients(
	client_id varchar(10) NULL,
	last_name varchar(20) NULL,
	first_name varchar(20) NULL,
	patronymic varchar(20) NULL,
	date_of_birth date NULL,
	passport_num varchar(15) NULL,
	passport_valid_to date NULL,
	phone bpchar(16) NULL,
	create_dt timestamp(0) NULL,
	update_dt timestamp(0) NULL
);
--Таблицы фактов, загруженных в хранилище. В качестве фактов выступают сами 
--транзакции и «черный список» паспортов.
create table if not exists deaian.kshn_dwh_fact_transactions(
	trans_id varchar(30),
	trans_date timestamp(0),
	card_num bpchar(20),
	oper_type varchar(30),
	amt decimal(18,2),
	oper_result varchar(30),
	terminal varchar(30)
);
create table if not exists deaian.kshn_dwh_fact_passport_blacklist(
	passport_num varchar(15),
	entry_dt date
);
--Таблицы измерений, хранящиеся в формате SCD1.
create table if not exists deaian.kshn_dwh_dim_terminals(
	terminal_id varchar(30),
	terminal_type varchar(20),
	terminal_city varchar(50),
	terminal_address varchar(100),
	create_dt timestamp(0),
	update_dt timestamp(0),
	processed_dt timestamp(0)
);
create table if not exists deaian.kshn_dwh_dim_cards(
	card_num bpchar(20),
	account_num bpchar(20),
	create_dt timestamp(0),
	update_dt timestamp(0),
	processed_dt timestamp(0)
);
create table if not exists deaian.kshn_dwh_dim_accounts(
	account_num bpchar(20),
	valid_to date,
	client varchar(10),
	create_dt timestamp(0),
	update_dt timestamp(0),
	processed_dt timestamp(0)
);
create table if not exists deaian.kshn_dwh_dim_clients(
	client_id varchar(10),
	last_name varchar(20),
	first_name varchar(20),
	patronymic varchar(20),
	date_of_birth date,
	passport_num varchar(15),
	passport_valid_to date,
	phone varchar(16),
	create_dt timestamp(0),
	update_dt timestamp(0),
	processed_dt timestamp(0)
);
--Таблица с отчетом.
create table if not exists deaian.kshn_rep_fraud(
	event_dt timestamp(0), --?
	passport varchar(15), --deaian.kshn_dwh_dim_clients
	fio varchar(150), --deaian.kshn_dwh_dim_clients
	phone varchar(16), --deaian.kshn_dwh_dim_clients
	event_type int, --1,2,3,4
	report_dt date --now()
);
--Таблицы для хранения метаданных.
create table if not exists deaian.chrn_meta(
    schema_name varchar(30),
    table_name varchar(30),
    max_update_dt timestamp(0)
);
create table if not exists deaian.kshn_rep_fraud_tmp(
	event_dt timestamp(0), --fact transactions?
	passport varchar(15), --deaian.kshn_dwh_dim_clients
	fio varchar(150), --deaian.kshn_dwh_dim_clients
	phone varchar(16), --deaian.kshn_dwh_dim_clients
	event_type int, --1,2,3,4
	report_dt date --now()
);
create table if not exists deaian.kshn_meta_files(
	file char(8)
);