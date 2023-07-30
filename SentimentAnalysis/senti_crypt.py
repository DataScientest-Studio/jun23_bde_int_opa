import requests
import pandas as pd

def get_senti_crypt():
    url = 'https://api.senticrypt.com/v2/all.json'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data_list = response.json()
            df = pd.DataFrame(data_list)
            return df
        else:
            print(f"Error: Failed to fetch data. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    data = get_senti_crypt()
    print(data)
