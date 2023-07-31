# Kraken API Interaction Python Code

This Python script provides classes for interacting with the Kraken cryptocurrency exchange API. It includes classes for managing orders, fetching market data, and performing account management tasks.

## Classes

1. **KrakenOrderManager**: This class is used for creating and placing buy/sell orders on the Kraken exchange. It contains methods such as `_create_headers()`, `_create_data_payload()`, `_send_kraken_request()`, `place_buy_order()`, and `place_sell_order()`.

2. **KrakenAPIMarketData**: This class is used to fetch market data from the Kraken API. It contains methods like `_make_api_call()`, `get_asset_info()`, `get_tradable_asset_pairs()`, and `get_historical_data()`.

3. **KrakenAPIAcctMgt**: This class provides methods for account management tasks such as fetching balance, open/closed orders, trades history, and open positions. It includes methods like `get_kraken_signature()`, `kraken_request()`, `get_balance()`, `get_extended_balance()`, `get_trade_orders()`, `get_open_orders()`, `get_closed_orders()`, `query_orders_info()`, `get_trades_history()`, and `get_open_positions()`.

## Running the Code

The script includes a `main()` function that tests the methods of each class. The function creates an instance of each class and calls their methods, printing the results for each call.

To run the script, save it as a Python file (e.g., `kraken_api.py`) and run it using Python:

```
python kraken_api.py
```

Please note that this script requires valid API keys from the Kraken API, which should be placed in a file named `keys.txt` in the same directory. The `keys.txt` file should contain the API key on the first line and the API secret on the second line.

## Dependencies

Please check the requirements.txt file.

You can install these packages using pip:

```
pip install -r requirements.txt
```

## Note

The KrakenOrderManager is set by default to send a validation of the request and not to place an actual request. 
To set an actual request you need to change the validate argument into False, for example:
- `order_manager = KrakenOrderManager()` doesn't place a buy/sell request
- `order_manager = KrakenOrderManager(False)` does place a buy/sell request