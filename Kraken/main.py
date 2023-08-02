import requests
import time
import pandas as pd
import hashlib
import hmac
import base64
import urllib.parse
from datetime import datetime, timedelta

from kraken_api_acct_mgt import KrakenAPIAcctMgt, load_api_keys
from kraken_api_market_data import KrakenAPIMarketData
from kraken_api_trade import KrakenOrderManager


def main():
    """
    A function to test the methods of the KrakenOrderManager, KrakenAPIMarketData, and KrakenAPIAcctMgt classes.
    
    It creates instances of these classes and calls their methods, printing the results for each call.
    
    Note: The function requires valid API keys from the Kraken API, which should be placed in a file named 'keys.txt'.
    """
    # Create an instance of KrakenOrderManager and test its methods
    order_manager = KrakenOrderManager()
    ordertype = "limit"
    pair = "XBTUSD"
    volume_pair = 5
    price_pair = 27500

    # Place a buy order and print the result
    resp = order_manager.place_buy_order(ordertype, pair, volume_pair, price_pair)
    print("\n")
    print("Buy order:")
    print(resp)

    # Place a sell order and print the result
    resp = order_manager.place_sell_order(ordertype, pair, volume_pair, price_pair)
    print("\n")
    print("Sell order:")
    print(resp)

    # Create an instance of KrakenAPIMarketData and test its methods
    kraken_api = KrakenAPIMarketData()

    print("\nGet Asset Info")
    asset_info = kraken_api.get_asset_info()
    print(asset_info)

    print("\nGet tradable asset pairs")
    tradable_pairs = kraken_api.get_tradable_asset_pairs()
    print(tradable_pairs)

    print("\nGet historical data")
    list_pairs = ["XXBTZEUR", "1INCHUSD", "AAVEETH", "AAVEEUR"]
    historical_data = kraken_api.get_historical_data(list_pairs)
    print(historical_data)

    # Create an instance of KrakenAPIAcctMgt and test its methods
    kraken_api = KrakenAPIAcctMgt()

    resp = kraken_api.get_balance()
    print("\nGet Balance:")
    print(resp)

    resp = kraken_api.get_extended_balance()
    print("\nGet Extended Balance:")
    print(resp)

    asset = "XXBT"
    resp = kraken_api.get_trade_orders(asset)
    print("\nGet Trade Orders:")
    print(resp)

    tades_bool = True
    resp = kraken_api.get_open_orders(tades_bool)
    print("\nOpen Orders:")
    print(resp)

    resp = kraken_api.get_closed_orders()
    print("\nClosed Orders:")
    print(resp)

    txid = "OBCMZD-JIEE7-77TH3F,OMMDB2-FSB6Z-7W3HPO"
    resp = kraken_api.query_orders_info(txid)
    print("\nQuery Orders Info:")
    print(resp)

    resp = kraken_api.get_trades_history()
    print("\nGet Trades History:")
    print(resp)

    resp = kraken_api.get_open_positions()
    print("\nGet Open Positions:")
    print(resp)

if __name__ == "__main__":
    main()
