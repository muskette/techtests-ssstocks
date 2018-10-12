from fixtures import STATIC_STOCK_DATA
from trading import MOST_RECENT_TRADE_PRICE, get_recent_trades, derive_price_from_trades


class Stock:
    def __init__(self, symbol, type, last_dividend, par_value, fixed_dividend=None):
        self.symbol = symbol
        self.s_type = type
        self.last_dividend = last_dividend
        self.par_value = par_value
        self.fixed_dividend = fixed_dividend

    @property
    def dividend_yield(self):
        stock_price = self.recent_price
        if stock_price:
            if self.fixed_dividend:
                return (self.fixed_dividend * self.par_value) / stock_price
            return self.last_dividend / stock_price

    @property
    def pe_ratio(self):
        if self.last_dividend:
            stock_price = self.recent_price
            return stock_price / self.last_dividend

    def derive_initial_price(self):
        # IPO data not within scope of the tech test, so let's just use face value for now
        return self.par_value

    @property
    def recent_price(self):
        """
        We want to be able to look at the average price of a trade over the last 15 minutes.
        Our ideal route is to look at all the trades for a stock in the time period and that as an average

        There are two failure cases with this: 1. There have never been any trades OR 2. There have been no trades recently.
        The challenge with this is determining which case we're in.

        In a real world scenario, determining our fallback process for these failure cases would
        require further discussion and updates on the requirements specification.
        For this context, I'll just make up my own fallback processes.

        For case 1, we will provide the initial price for the stock.
        For case 2, we will give the most recent price indicator, which would be the price of the most recent trade.
        Determining either of this values is a responsibility we're passing on to another function.
        """
        trades = get_recent_trades(self.symbol)
        if trades:
            price = derive_price_from_trades(trades)
        else:
            most_recent_trade = self.get_most_recent_trade()
            if most_recent_trade:
                price = most_recent_trade
            else:
                price = self.derive_initial_price()
        return price

    def get_most_recent_trade(self):
        """
        If we end up in case 2 regularly, we're going to want to avoid hitting the database multiple times.
        Considering the nature of stock markets, this case is probably quite rare but lets assume it is an issue.
        Instead of hitting the database, we're going to use cache with key based invalidation.
        In this test, it'll be represented by a dictionary rather than full caching software.
        """
        return MOST_RECENT_TRADE_PRICE.get(self.symbol)

    def __str__(self):
        return self.symbol


STOCKS = {
    "TEA": Stock(
        symbol=STATIC_STOCK_DATA["TEA"]['Symbol'],
        type=STATIC_STOCK_DATA["TEA"]['Type'],
        last_dividend=STATIC_STOCK_DATA["TEA"]['Last Dividend'],
        par_value=STATIC_STOCK_DATA["TEA"]['Par Value'],
        fixed_dividend=STATIC_STOCK_DATA["TEA"].get('Fixed Dividend')
    ),
    "POP": Stock(
        symbol=STATIC_STOCK_DATA["POP"]['Symbol'],
        type=STATIC_STOCK_DATA["POP"]['Type'],
        last_dividend=STATIC_STOCK_DATA["POP"]['Last Dividend'],
        par_value=STATIC_STOCK_DATA["POP"]['Par Value'],
        fixed_dividend=STATIC_STOCK_DATA["POP"].get('Fixed Dividend')
    ),
    "ALE": Stock(
        symbol=STATIC_STOCK_DATA["ALE"]['Symbol'],
        type=STATIC_STOCK_DATA["ALE"]['Type'],
        last_dividend=STATIC_STOCK_DATA["ALE"]['Last Dividend'],
        par_value=STATIC_STOCK_DATA["ALE"]['Par Value'],
        fixed_dividend=STATIC_STOCK_DATA["ALE"].get('Fixed Dividend')
    ),
    "GIN": Stock(
        symbol=STATIC_STOCK_DATA["GIN"]['Symbol'],
        type=STATIC_STOCK_DATA["GIN"]['Type'],
        last_dividend=STATIC_STOCK_DATA["GIN"]['Last Dividend'],
        par_value=STATIC_STOCK_DATA["GIN"]['Par Value'],
        fixed_dividend=STATIC_STOCK_DATA["GIN"].get('Fixed Dividend')
    ),
    "JOE": Stock(
        symbol=STATIC_STOCK_DATA["JOE"]['Symbol'],
        type=STATIC_STOCK_DATA["JOE"]['Type'],
        last_dividend=STATIC_STOCK_DATA["JOE"]['Last Dividend'],
        par_value=STATIC_STOCK_DATA["JOE"]['Par Value'],
        fixed_dividend=STATIC_STOCK_DATA["JOE"].get('Fixed Dividend')
    ),
}