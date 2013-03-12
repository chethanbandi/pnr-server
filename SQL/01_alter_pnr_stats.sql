alter table PNR_STATS
   add column status_code       int,
   add column status_message    varchar(50), 
   add column user_agent        varchar(250),
   add column remote_addr       varchar(20);
