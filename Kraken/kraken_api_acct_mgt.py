import requests
import time
import hashlib
import hmac
import base64
import urllib.parse
import pandas as pd
from datetime import datetime, timedelta

def load_api_keys():
    """
    Loads API keys from a file called 'keys.txt'.

    Returns:
        tuple: A tuple containing the API key and API secret.
    """
    with open('keys.txt', 'r') as file:
        keys = file.read().splitlines()
    return keys[0], keys[1]

class KrakenAPIAcctMgt: 
    """
    A class that provides methods to interact with the Kraken API for account management tasks.

    Attributes:
        api_url (str): The base URL for the Kraken API.
        api_key (str): The API key used for authentication.
        api_sec (str): The API secret used for signing requests.

    Methods:
        get_kraken_signature(urlpath, data):
            Generates the signature for a Kraken API request.

        kraken_request(uri_path, data):
            Sends a request to the Kraken API and returns the response.

        get_balance():
            Retrieves the user's current account balance from the Kraken API.

        get_extended_balance():
            Retrieves the user's current extended account balance from the Kraken API.

        get_trade_orders(asset):
            Retrieves the user's trade orders for a specific asset from the Kraken API.

        get_open_orders(trades_bool):
            Retrieves the user's open orders from the Kraken API.

        get_closed_orders():
            Retrieves the user's closed orders from the Kraken API.

        query_orders_info(txid):
            Queries information about specific transaction IDs from the Kraken API.

        get_trades_history():
            Retrieves the user's trade history from the Kraken API.

        get_open_positions():
            Retrieves the user's open positions from the Kraken API.
    """
    def __init__(self):
        """
        Initializes the KrakenAPIAcctMgt class.

        It sets the default values for the base URL, API key, and API secret.
        """
        self.api_url = "https://api.kraken.com"
        self.api_key = load_api_keys()[0]
        self.api_sec = load_api_keys()[1]

    def get_kraken_signature(self, urlpath, data):
        """
        Generates the signature for a Kraken API request.

        Args:
            urlpath (str): The API endpoint URL path.
            data (dict): The request data parameters.

        Returns:
            str: The generated signature as a base64-encoded string.
        """
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()
        mac = hmac.new(base64.b64decode(self.api_sec), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    def kraken_request(self, uri_path, data):
        """
        Sends a request to the Kraken API and returns the response.

        Args:
            uri_path (str): The API endpoint URI path.
            data (dict): The request data parameters.

        Returns:
            dict: The JSON response from the Kraken API.
        """
        headers = {}
        headers['API-Key'] = self.api_key
        data['nonce'] = str(int(1000 * time.time()))
        headers['API-Sign'] = self.get_kraken_signature(uri_path, data)
        req = requests.post((self.api_url + uri_path), headers=headers, data=data)
        response = req.json()
        return response

    def get_balance(self):
        return self.kraken_request('/0/private/Balance', {})

    def get_extended_balance(self):
        return self.kraken_request('/0/private/BalanceEx', {})

    def get_trade_orders(self, asset):
        data = {"asset": asset}
        return self.kraken_request('/0/private/TradeBalance', data) 

    def get_open_orders(self, trades_bool):
        data = {"trades": trades_bool}
        return self.kraken_request('/0/private/OpenOrders', data)

    def get_closed_orders(self):
        return self.kraken_request('/0/private/ClosedOrders', {})

    def query_orders_info(self, txid):
        data = {"txid": txid, "trades": True}
        return self.kraken_request('/0/private/QueryOrders', data)

    def get_trades_history(self):
        return self.kraken_request('/0/private/TradesHistory', {})

    def get_open_positions(self):
        data = {"docalcs": True}
        return self.kraken_request('/0/private/OpenPositions', data)

if __name__ == "__main__":
    kraken_api = KrakenAPIAcctMgt()

    # Testing the functions
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

    # Construct the request and print the result
    # txid is a Comma delimited list of transaction IDs to query info about (50 maximum)
    # we can get txid from trades history
    # this txid is only for testing
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
