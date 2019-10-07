""" This script compiles data from Alpha Vantage API
    and transforms the json output into a dataframe and CSV file"""

# script to get API key


def get_keys(path):
    with open(path) as f:
        return json.load(f)

# script to compile data into dataframe per symbol


def vantage_point(symbol):
    """Compiles data per symbol"""
    URL = 'https://www.alphavantage.co/query?'
    PARAMS = {"function": 'TIME_SERIES_DAILY',
              "symbol": f'{symbol}',
              "outputsize": 'full',
              "apikey": api_key}

    response = requests.get(URL, PARAMS)
    print(f"{symbol} response code: {response.status_code}")
    df = pd.DataFrame(response.json()['Time Series (Daily)']).T
    df.columns = [f'{symbol}_open', f'{symbol}_high',
                  f'{symbol}_low', f'{symbol}_close', f'{symbol}_volume']
    df.to_csv(f"data/raw/{symbol}.csv")
    return df
