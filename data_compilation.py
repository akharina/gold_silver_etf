import requests
import pandas as pd
import json

''' This script compiles data from Alpha Vantage API
    and transforms the JSON output into a dataframe and CSV file'''

# def get_keys(path):
#     '''get API key'''
#     with open(path) as f: 
#         return json.load(f)

def call_api_one_symbol(symbol, verbose=True):
    '''call API and compile data for each symbol'''
    #api_key = get_keys('/Users/alyssaliguori/secret/alpha_vantage_api.json')

    URL = 'https://www.alphavantage.co/query?'
    PARAMS = {'function': 'TIME_SERIES_DAILY', 
              'symbol': symbol,
              'outputsize': 'full',
              'apikey': 'QQWPF2KTW701PG7H'
              }
    response = requests.get(URL, PARAMS)
    if response.status_code == 200:
        if verbose: 
            print(f'The response code for {symbol} is {response.status_code}')
    else:
        raise ValueError(f'Error getting data from {url} API. Response code: {response.status_code}')  
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


