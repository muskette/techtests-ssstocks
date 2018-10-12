import logging
from datetime import datetime, timedelta

from fixtures import db, STATIC_STOCK_DATA
from math_library import mean, geo_mean

MOST_RECENT_TRADE_PRICE = {}


def validate_trade(trade_func):
    def wrapper(symbol, quantity, price, trade_type):
        valid = validate(symbol, quantity, trade_type)
        if valid:
            return trade_func(symbol, quantity, price, trade_type)
        else:
            logging.error("Error validating trade. Transaction not executed")
            return

    def validate(symbol, quantity, trade_type):
        valid = True
        if symbol not in STATIC_STOCK_DATA.keys():
            logging.warning('Symbol not recognised')
            valid = False
        if quantity <= 0:
            logging.warning("Invalid quantity for trade")
            valid = False
        if trade_type not in ['buy', 'sell']:
            logging.warning("Invalid value for trade type")
            valid = False
        return valid

    return wrapper


@validate_trade
def register_trade(symbol, quantity, price, trade_type):
    price_per_unit = price / quantity
    statement = f"""INSERT INTO trades (symbol, timestamp, quantity, price, ppu, type) VALUES (
        '{symbol}', {datetime.utcnow().timestamp()}, {quantity}, {price}, {price_per_unit}, '{trade_type}'
    );"""
    MOST_RECENT_TRADE_PRICE[symbol] = price_per_unit
    db.execute(statement)
    db.commit()


def deserialise_trade_rows(rows):
    return [
        {
            "symbol": row[0],
            "timestamp": row[1],
            "quantity": row[2],
            "price": row[3],
            "ppu": row[4],
            "type": row[5]
        } for row in rows
    ]


def get_recent_trades(symbol):
    cutoff = (datetime.utcnow() - timedelta(minutes=15)).timestamp()
    statement = f"SELECT symbol, timestamp, quantity, price, ppu, type FROM trades WHERE symbol = '{symbol}' AND timestamp >= {cutoff};"
    results = db.execute(statement)
    return deserialise_trade_rows(results.fetchall())


def derive_price_from_trades(trades):
    return mean([x['ppu'] for x in trades])


def fetch_all_sales_prices_by_stock():
    statement = """SELECT symbol, ppu FROM trades"""
    results = db.execute(statement).fetchall()
    index = {}
    for row in results:
        index.setdefault(row[0], []).append(float(row[1]))
    return index


def all_share_index():
    index = fetch_all_sales_prices_by_stock()
    print(f"Stock \t|\t Index Price")
    print("============================")
    for key, values in index.items():
        print(f"{key} \t|\t {round(geo_mean(values))}")