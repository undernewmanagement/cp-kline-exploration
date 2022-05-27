# Acquiring historic klines (Candle Data)

This repo explores some ideas how we might acquire data from various exchanges.

NOTE: I did not use the famous `ccxt` library (trying to keep it simple)

My hope is to expand this conversation and see how this can meet the needs of the task.


# Requirements

  * Python 3.x (prefer a later version)
  * Timescale DB instance (see @sam for the credentials)

# Getting started

  1. Clone this repo
  2. create a virtual environment
  3. run `pip install -r requirements.txt`
  4. in the `coinbase/models.py` file date the `PASS` variable with the password. (I know, i'm lazy here)
  5. done

# Using the crawler
I used Typer, a popular python package for making nice command line tools.

Simply tun `python crawler.py` and you will see the options available to you.

There are two commands: acquire all trading pairs and acquire full kline data for a given pair.

## Acquiring all token pairs

`python crawler.py coinbase all-pairs` and you should see the script kick off. It 
pulls the pairs from the coinbase API and the validates it against the database. Changes in the
status are flagged and updated. No changes are simply ignored.

## Acquiring all kline data
`python coinbase.py fetch-all-klines BTC-USD` will being the process of querying the api and
inserting klines into the database. Duplicate entires are ignored. It will continue to paginate
backwards in time until no more pairs are read.

# Other notes
There is a `schema.sql` auto-generated, but it is untested if you can import it.
Pycharm is a bit funky with DDL generation.

