SQL_INSERT_INIT_META = """insert into deaian.kshn_meta_max_update_dt( schema_name, table_name, max_update_dt )
values
('deaian', 'kshn_dwh_dim_terminals', to_date('1900-01-01','YYYY-MM-DD')),
('deaian', 'kshn_dwh_dim_cards'    , to_date('1900-01-01','YYYY-MM-DD')),
('deaian', 'kshn_dwh_dim_accounts' , to_date('1900-01-01','YYYY-MM-DD')),
('deaian', 'kshn_dwh_dim_clients'  , to_date('1900-01-01','YYYY-MM-DD')),
('deaian', 'kshn_rep_fraud'        , to_date('1900-01-01','YYYY-MM-DD'));
"""