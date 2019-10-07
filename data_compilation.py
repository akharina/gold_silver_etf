''' This script compiles data from Alpha Vantage API
    and transforms the JSON output into a dataframe and CSV file'''

def get_keys(path):
    '''get API key'''
    with open(path) as f: 
        return json.load(f)

def call_api_one_symbol(symbol, verbose=True):
    '''call API and compile data for each symbol'''
    URL = 'https://www.alphavantage.co/query?'
    PARAMS = {'function': 'TIME_SERIES_DAILY', 
              'symbol': f'{symbol}',
              'outputsize': 'full',
              'apikey': api_key
              }
    response = requests.get(URL, PARAMS)
    print(f'{symbol} response code: {response.status_code}')
    df = pd.DataFrame(response.json()['Time Series (Daily)'])
    df['symbol'] = symbol
    return df

def call_all_symbols(symbol_list):
    '''Calls the API for each symbol in symbol_list and returns 
    pandas dataframe in long format, concatenating all dfs'''
    for i, symbol in enumerate(symbol_list):
        if i == 0:
            df = call_api_one_symbol(symbol)
        else: 
            df = pd.concat(df, call_api_one_symbol(symbol))
        return df


