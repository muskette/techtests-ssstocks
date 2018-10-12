#!/usr/bin/python3.6
from models import STOCKS
from trading import register_trade, all_share_index, MOST_RECENT_TRADE_PRICE

if __name__ == '__main__':
    print("Registering Trades")
    register_trade('JOE', 10, 1598, 'sell')
    register_trade('JOE', 10, 1698, 'sell')
    register_trade('JOE', 10, 2398, 'sell')
    register_trade('POP', 10, 868, 'sell')
    register_trade('POP', 10, 668, 'sell')
    register_trade('POP', 100, 6811, 'sell')
    register_trade('ALE', 1, 21, 'sell')
    register_trade('ALE', 1, 25, 'sell')
    register_trade('ALE', 1, 28, 'sell')
    register_trade('ALE', 1, 28, 'sell')
    print("10 Sample trades registered")
    print("\n")
    print("Printing All Share Index")
    all_share_index()

    print("\n----------------------\n")
    print("Attempting invalid trades\n")
    input("Press enter to continue\n")

    register_trade('JOE', 0, 1560, 'sell')
    print("\n")
    register_trade('JO', 10, 1698, 'sell')
    print("\n")
    register_trade('JOE', 10, 2398, 'sellaaa')
    print("\n")

    print("\n----------------------\n")
    print("Printing derived Stock Properties")
    input("Press enter to continue\n")

    for k,stock in STOCKS.items():
        print(f"Stock: {stock}")
        print(f"Dividend Yield: {stock.dividend_yield}")
        print(f"P/E Ratio: {stock.pe_ratio}")
        print(f"Latest Average Price: {stock.recent_price}")
        print("\n-----------------------------------------------\n")


    print("Checking Latest Price Cache")
    input("Press enter to continue\n")

    print(f"{MOST_RECENT_TRADE_PRICE}")

    print("\n ========== Done")