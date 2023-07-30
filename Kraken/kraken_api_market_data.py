import requests
import time
import pandas as pd
from kraken_api_acct_mgt import KrakenAPIAcctMgt, load_api_keys

class KrakenAPIMarketData:
    def __init__(self,since=None):
        """
        Initialize the KrakenAPIMarketData object.

        This constructor sets up the KrakenAPIMarketData object with the API key, API secret, and other URL endpoints
        needed to interact with the Kraken API.

        Attributes:
            api_key (str): Kraken API key.
            api_sec (str): Kraken API secret.
            url_get_asset_info (str): URL for fetching asset information.
            url_get_tradable_asset_pairs (str): URL for fetching tradable asset pairs.
            url_get_OHLC (str): URL for fetching historical OHLC data.
            uri_get_OHLC_Kraken_signature (str): URI path for generating the API signature for OHLC data.
            interval (int): Default time interval in minutes for historical data.
            since (int, optional): Default starting timestamp for historical data. If not provided, the constructor
                                   will use the value corresponding to one week ago from the current time.
        """
        self.api_key, self.api_sec = load_api_keys()
        self.url_get_asset_info = 'https://api.kraken.com/0/public/Assets'
        self.url_get_tradable_asset_pairs = 'https://api.kraken.com/0/public/AssetPairs'
        self.url_get_OHLC = "https://api.kraken.com/0/public/OHLC"
        self.interval = 1440
        self.kraken_api_acct_mgt = KrakenAPIAcctMgt()

        if since is None:
            # Calculate one week ago from the current time
            one_week_ago = int(time.time()) - (7 * 24 * 60 * 60)
            self.since = one_week_ago
        else:
            self.since = since

    def _make_api_call(self, url):
        """
        Make an API call to the specified URL.

        This method sends a GET request to the specified URL and returns the JSON response.

        Parameters:
            url (str): The URL for the API call.

        Returns:
            dict: A dictionary containing the JSON response from the API call or None if an error occurred.
        """
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def get_asset_info(self):
        """
        Get information about the assets that are available for deposit, withdrawal, trading, and staking.

        This method makes an API call to fetch the asset information from Kraken.

        Returns:
            pd.DataFrame: A DataFrame containing information about the available assets.
                          Each row represents an asset, and the columns include details like asset name, symbol, and more.
                          Returns None if an error occurred during the API call.
        """
        resp = self._make_api_call(self.url_get_asset_info)
        if resp is not None:
            result_data = resp.get("result", {})
            df = pd.DataFrame.from_dict(result_data, orient="index")
            df["quote"] = df.index
            return df
        return None

    def get_tradable_asset_pairs(self):
        """
        Get tradable asset pairs from Kraken.

        This method makes an API call to fetch the tradable asset pairs available on Kraken.

        Returns:
            pd.DataFrame: A DataFrame containing tradable asset pairs.
                          Each row represents a trading pair, and the columns include details like base currency, quote currency, and more.
                          Returns None if an error occurred during the API call.
        """
        resp = self._make_api_call(self.url_get_tradable_asset_pairs)
        if resp is not None:
            result_data = resp.get("result", {})
            df = pd.DataFrame.from_dict(result_data, orient="index")
            return df
        return None

    def get_historical_data(self, list_pairs, interval=None, since=None):
        """
        Get historical OHLC data for a list of asset pairs from the Kraken API.

        Parameters:
            list_pairs (list): A list of asset pairs for which historical data is requested.
            interval (int, optional): The time interval in minutes for the data. Default is specified in __init__.
            since (int, optional): The starting timestamp for the data. Default is specified in __init__.

        Returns:
            pd.DataFrame: A DataFrame containing historical OHLC data for all asset pairs.
                          The DataFrame has columns like timestamp, open, high, low, close, volume, and more.
                          The 'pair' column indicates the asset pair associated with each row of data.
                          Returns None if an error occurred during the API call.
        """
        if interval is None:
            interval = self.interval
        if since is None:
            since = self.since

        # Set the columns for the DataFrame containing data for all pairs
        columns_all_pairs = ['pair', 'timestamp', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']
        
        # Create an empty DataFrame to contain data for all pairs
        df_all_pairs = pd.DataFrame(columns=columns_all_pairs)

        # Make a call for each pair in the list
        for pair in list_pairs:
            data = {
                "pair": pair,
                "interval": interval,
                "since": since,
                "nonce": int(1000 * time.time())
            }

            # Generate the API signature
            signature = self.kraken_api_acct_mgt.get_kraken_signature(self.url_get_OHLC, data)
            
            headers = {
                "API-Key": self.api_key,
                "API-Sign": signature
            }

            try:
                # Send the request to the Kraken API
                response = requests.post(self.url_get_OHLC, headers=headers, data=data)
                # response.raise_for_status()  # Raise an exception if the request was unsuccessful
                response = response.json()
                response = response['result'][pair]

                # Define columns for the DataFrame containing data for one pair
                columns_one_pair = ['timestamp' ,'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']
                
                # Create a DataFrame with the response data and the specified columns
                df_pair = pd.DataFrame(response, columns=columns_one_pair)

                # Add the "pair" column with the current pair name to the DataFrame
                df_pair["pair"] = pair

                # Concatenate the DataFrame for the current pair with the DataFrame containing data for all pairs
                df_all_pairs = pd.concat([df_all_pairs, df_pair], axis=0, ignore_index=True)
        
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
    
        return df_all_pairs


if __name__ == "__main__":
    kraken_api = KrakenAPIMarketData()

    print("\n")
    print("Get Asset Info")
    asset_info = kraken_api.get_asset_info()
    print(asset_info)

    print("\n")
    print("Get tradable asset pairs")
    tradable_pairs = kraken_api.get_tradable_asset_pairs()
    print(tradable_pairs)

    print("\n")
    print("Get historical data")
    list_pairs = ["XXBTZEUR", "1INCHUSD", "AAVEETH", "AAVEEUR"]
    historical_data = kraken_api.get_historical_data(list_pairs)
    print(historical_data)
