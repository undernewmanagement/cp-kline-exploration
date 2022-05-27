from datetime import datetime
from typing import Optional
from enum import Enum

import typer
import requests
from .models import TradingPair, CandleData
from peewee import DoesNotExist, fn


app = typer.Typer()


class Granularity(str, Enum):
    one_minute = 60
    five_minute = 300
    fifteen_minute = 900
    sixty_minute = 3600
    six_hour = 21600
    one_day = 86400


def upsert_trading_pair(item):
    """
    Insert or update a trading pair. Send out a log / warning when the status of a pair changes.
    Also notice when a new pair is found.

    :param payload:
    :return:
    """
    try:
        pair = TradingPair.get(token_id=item['id'])

    except DoesNotExist as e:
        typer.echo(f"{item['id']} not found. Creating...")
        pair = TradingPair.create(
            token_id=item['id'],
            base_currency=item['base_currency'],
            quote_currency=item['quote_currency'],
            display_name=item['display_name'],
            status=item['status'],
            status_message=item['status_message']
        )

    if pair.status.casefold() != item['status'].casefold():
        pair.status = item['status']
        pair.status_message = item['status_message']
        pair.save()
        typer.echo(f"Token status changed! New status={pair.status}")
    else:
        typer.echo(f"Token found. No changes")


@app.command()
def all_pairs():
    """
    Fetch all trading pairs for Coinbase
    :return:
    """
    typer.echo(f"Getting all pairs")
    r = requests.get('https://api.exchange.coinbase.com/products', headers={"Accept": "application/json"})
    results = r.json()

    for item in results:
        typer.echo(item)
        upsert_trading_pair(item)


@app.command()
def kline(pair: str,
          granularity: Granularity = Granularity.one_day,
          start: Optional[int] = typer.Option(None),
          end: Optional[int] = typer.Option(None)):
    """
    Fetch kline data for a pair and start/end date range

    :param pair:
    :param granularity:
    :param start:
    :param end:
    :return:
    """
    # todo: validate end date > start date
    # todo: validate end date not in future
    if end is None:
        end = datetime.utcnow().strftime('%s')

    try:
        product_id = TradingPair.get(token_id=pair)

    except DoesNotExist as e:
        typer.echo(f"That trading pair is not in the database")
        exit(1)

    params = {
        'end': end,
        'granularity': granularity
    }

    r = requests.get(f'https://api.exchange.coinbase.com/products/{pair}/candles',
                     headers={"Accept": "application/json"},
                     params=params)

    results = r.json()

    typer.echo(r.content)

    bob=[]
    for i in results:
        ts = datetime.utcfromtimestamp(i[0])
        bob.append({
            'tick_time': ts,
            'low_price': i[1],
            'high_price': i[2],
            'open_price': i[3],
            'close_price': i[4],
            'volume': i[5],
            'trading_pair_id': product_id
        })

    CandleData.insert_many(bob).on_conflict_ignore().execute()

    typer.echo(f"Processed {len(bob)} items")


@app.command()
def fetch_all_klines(pair:str):
    """
    Fetch the full historic klines (candle data) for the given pair

    Refereces: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproductcandles

    :param pair: A known Coinbase trading pair
    :return:
    """


    try:
        tp = TradingPair.get(token_id=pair)

    except DoesNotExist as e:
        typer.echo(f"That trading pair is not in the database")
        exit(1)

    get_more = True
    params = {
        'start': None,
        'end': None,
        'granularity': 60,
    }

    while get_more:
        ts = CandleData\
                    .select(fn.Min(CandleData.tick_time).alias('hi_tick_time'))\
                    .where(CandleData.trading_pair_id==tp.id)\
                    .get()

        if ts.hi_tick_time:
            hi_ts = int(ts.hi_tick_time.strftime('%s'))
        else:
            hi_ts = int(datetime.utcnow().strftime('%s'))

        lo_ts = hi_ts - 18000

        typer.echo(f"Hi: {hi_ts}  Lo: {lo_ts}")

        params['start'] = lo_ts
        params['end'] = hi_ts

        r = requests.get(f'https://api.exchange.coinbase.com/products/{pair}/candles',
                         headers={"Accept": "application/json"},
                         params=params)

        typer.echo(r.url)
        results = r.json()

        if len(results) > 0:
            bob = []
            for i in results:

                ts = datetime.utcfromtimestamp(i[0])

                typer.echo(f"{i[0]}: {ts.strftime('%c')}")

                bob.append({
                    'tick_time': ts,
                    'low_price': i[1],
                    'high_price': i[2],
                    'open_price': i[3],
                    'close_price': i[4],
                    'volume': i[5],
                    'trading_pair_id': tp.id
                })
            CandleData.insert_many(bob).on_conflict_ignore().execute()
            typer.echo(f"Processed {len(bob)} items")
        else:
            typer.echo('No more results')
            get_more = False

    typer.echo('DONE')


if __name__ == "__main__":
    app()