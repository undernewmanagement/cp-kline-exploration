create table if not exists conditions
(
    time        timestamp with time zone not null,
    location    text                     not null,
    temperature double precision
);

alter table conditions
    owner to tsdbadmin;

create index if not exists conditions_time_idx
    on conditions (time desc);

create trigger ts_insert_blocker
    before insert
    on conditions
    for each row
execute procedure ???();

create table if not exists coinbase_trading_pair
(
    id             integer default nextval('trading_pair_id_seq'::regclass) not null
        constraint trading_pair_pk
            primary key,
    token_id       varchar(20)                                              not null,
    base_currency  varchar(10),
    quote_currency varchar(10),
    display_name   varchar(20),
    status         varchar,
    status_message varchar
);

alter table coinbase_trading_pair
    owner to tsdbadmin;

create unique index if not exists trading_pair_token_id_uindex
    on coinbase_trading_pair (token_id);

create table if not exists coinbase_candle_data
(
    id              integer default nextval('candle_data_id_seq'::regclass) not null,
    tick_time       timestamp                                               not null,
    low_price       double precision,
    high_price      double precision,
    open_price      double precision,
    close_price     double precision,
    volume          integer,
    trading_pair_id integer                                                 not null
        constraint candle_data_trading_pair_id_fk
            references coinbase_trading_pair
            on delete cascade
);

alter table coinbase_candle_data
    owner to tsdbadmin;

create unique index if not exists candle_data_tick_time_trading_pair_id_uindex
    on coinbase_candle_data (tick_time, trading_pair_id);

create index if not exists candle_data_tick_time_idx
    on coinbase_candle_data (tick_time desc);

create trigger ts_insert_blocker
    before insert
    on coinbase_candle_data
    for each row
execute procedure ???();

create table if not exists kucoin_trading_pair
(
    id             serial
        constraint kucoin_trading_pair_pk
            primary key,
    symbol         varchar not null,
    name           varchar,
    base_currency  varchar,
    quote_currency varchar,
    fee_currency   varchar,
    market         varchar,
    enable_trading boolean
);

alter table kucoin_trading_pair
    owner to tsdbadmin;

create unique index if not exists kucoin_trading_pair_symbol_uindex
    on kucoin_trading_pair (symbol);

