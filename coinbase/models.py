from peewee import *


PASS = ''
database = PostgresqlDatabase('tsdb', **{'host': 'vzdnk371jj.fox4b30j92.tsdb.cloud.timescale.com', 'port': 31426, 'user': 'tsdbadmin', 'password': PASS})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class TradingPair(BaseModel):
    base_currency = CharField(null=True)
    display_name = CharField(null=True)
    quote_currency = CharField(null=True)
    status = CharField(null=True)
    status_message = CharField(null=True)
    token_id = CharField(unique=True)

    class Meta:
        table_name = 'coinbase_trading_pair'


class CandleData(BaseModel):
    tick_time = DateTimeField()
    low_price = DoubleField(null=True)
    high_price = DoubleField(null=True)
    open_price = DoubleField(null=True)
    close_price = DoubleField(null=True)
    volume = IntegerField(null=True)
    trading_pair_id = ForeignKeyField(TradingPair, backref='candles')

    class Meta:
        table_name = 'coinbase_candle_data'
