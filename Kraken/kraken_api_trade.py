import requests
import time
from kraken_api_acct_mgt import KrakenAPIAcctMgt, load_api_keys


class KrakenOrderManager:
    def __init__(self, validate_value=True):
        """
        Initialize the KrakenOrderManager.

        Parameters:
            validate_value (bool, optional): When set to True, orders won't be placed, only tested.
                                            Default is True.
        """
        
        self.api_key = load_api_keys()[0]
        self.api_sec = load_api_keys()[1]
        self.api_url = "https://api.kraken.com"
        self.uri_path_add_order = '/0/private/AddOrder'
        self.validate_value = validate_value
        self.kraken_api_acct_mgt = KrakenAPIAcctMgt()

    def _create_headers(self):
        """
        Create the headers for the API request.

        Returns:
            dict: Dictionary containing the headers with the API key.
        """
        headers = {}
        headers['API-Key'] = self.api_key
        return headers

    def _create_data_payload(self, ordertype, buy_sell_type, pair, volume, price):
        """
        Create the data payload for the API request.

        Parameters:
            ordertype (str): The type of order to place (Enum: "market" "limit" "stop-loss" "take-profit" "stop-loss-limit" "take-profit-limit" "settle-position")
            type (str): buy or sell
            pair (str): The asset pair for which the order should be placed (e.g., 'XXBTZUSD', 'XETHXXBT', etc.).
            volume (float): Order quantity in terms of the base asset.
            price (float): Limit price for limit orders (the order won't be executed above this price).

        Returns:
            dict: Dictionary containing the data payload for the API request.
        """
        data = {
            "nonce": str(int(1000 * time.time())),
            "ordertype": ordertype,
            "type": buy_sell_type,
            "volume": volume,  # Order quantity in terms of the base asset
            "pair": pair,  # Asset pair id or altname
            "price": price,  # Limit price for limit orders
            "validate": self.validate_value  # When set to true, it validates inputs only and doesn't submit orders
        }
        return data

    def _send_kraken_request(self, uri_path, headers, data):
        """
        Send the API request to the Kraken API.

        Parameters:
            uri_path (str): The API URI path for placing the order.
            headers (dict): The headers for the API request.
            data (dict): The data payload for the API request.

        Returns:
            dict: JSON response from the Kraken API.
        """
        headers['API-Sign'] = self.kraken_api_acct_mgt.get_kraken_signature(uri_path, data)
        response = requests.post((self.api_url + uri_path), headers=headers, data=data)
        return response.json()

    def place_buy_order(self, ordertype, pair, volume, price):
        """
        Place a buy order on the Kraken exchange.

        Parameters:
            pair (str): The asset pair for which the order should be placed.
            volume (float): Order quantity in terms of the base asset.
            price (float): Limit price for limit orders.

        Returns:
            dict: JSON response from the Kraken API after placing the buy order.
        """
        headers = self._create_headers()
        data = self._create_data_payload(ordertype, "buy", pair, volume, price)
        response = self._send_kraken_request(self.uri_path_add_order, headers, data)
        return response
# ordertype, buy_sell_type, pair, volume, price):
    def place_sell_order(self, ordertype, pair, volume, price):
        """
        Place a sell order on the Kraken exchange.

        Parameters:
            pair (str): The asset pair for which the order should be placed.
            volume (float): Order quantity in terms of the base asset.
            price (float): Limit price for limit orders.

        Returns:
            dict: JSON response from the Kraken API after placing the sell order.
        """
        headers = self._create_headers()
        data = self._create_data_payload(ordertype, "sell", pair, volume, price)
        response = self._send_kraken_request(self.uri_path_add_order, headers, data)
        return response

if __name__ == "__main__":
    # Create an instance of KrakenOrderManager
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
