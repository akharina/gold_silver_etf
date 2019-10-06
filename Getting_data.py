import pandas as pd
#Import required libraries
import requests
import json
import pandas as pd

class Data_cleaning:
    """
    This class is written to obtain the data from alphavantage
    and also to clean the data
    """
    def __init__(self, function,symbol, outputsize, datatype, path):
        self.function = function
        self.outputsize = outputsize
        self.datatype = datatype
        self.symbol = symbol
        self.PATH = path
        self.URL = 'https://www.alphavantage.co/query?'
        self.apikey = self._get_keys()
    
    def _get_keys(self):
        """
        This function gets the api key for alphavantage
        """
        with open(self.PATH) as f:
            return json.load(f)['api_key']
        
    def obtain_data_one_symbol(self, symbol, verbose=True):
        URL_PARAMS = {'function': self.function, 
              'symbol': symbol, 
              'apikey': self.apikey,
              'outputsize' : self.outputsize,
              'datatype': self.datatype}
        response = requests.get(self.URL, params=URL_PARAMS)
        if response.status_code == 200:
            if verbose:
                print(f'The response code for {symbol} is {response.status_code}')
            return response
        else: 
            raise ValueError(f"Error getting data from {self.url} API: Response Code {response.status_code}")
            
    def obtain_data_all_symbols(self, verbose = True):
        output_dict = {}
        for symbol in self.symbol:
            res = self.obtain_data_one_symbol(symbol, verbose = verbose)
            df = pd.DataFrame(res.json()['Time Series (Daily)']).T
            df['Symbol'] = symbol
            output_dict[symbol] = df
        return output_dict
    def getting_cleaning_data(self,verbose=True):
        """
        This function gets all data frames as a dictionary
        and returns a long format dataframe.
        Also, it cleans the dataframe.
        """
        input_dict = self.obtain_data_all_symbols(verbose=verbose)
        all_dfs = []
        for key, temp in input_dict.items():
            temp.reset_index(inplace = True)
            temp.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'volume', 'symbol']
            to_be_numeric = ['Open', 'High', 'Low', 'Close', 'volume'] 
            temp[to_be_numeric] = temp[to_be_numeric].apply(pd.to_numeric) 
            temp['Time'] = pd.to_datetime(temp['Time'])
            temp['Year'] = temp['Time'].dt.year
            temp['Month'] = temp['Time'].dt.month
            temp['Day'] = temp['Time'].dt.day
            print(f'The number of null values in {key} is {temp.isna().sum().sum()}')
            all_dfs.append(temp)
        return pd.concat(all_dfs)