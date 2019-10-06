import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns
import pandas as pd

def visualizations(df, symbols, type_price = 'close',
                   start_date = '2010-01-01', end_date = '2010-01-01',
                   fill_na = 'ffill',  moving_average_plot = False , 
                   short_window = None , long_window = None):
    """
    This function get a dataframe as input
    and make several visualizations
    
    inputs are:
    df : data frame
    symbol: showing the previous metal
    start_date: the start date for ploting
    end_date: the end date for ploting
    short_window and long_window are used for making the moving averages plots
    fill_na: Method to use for filling holes in reindexed Series pad / ffill: propagate last valid observation forward to next     valid backfill / bfill: use next valid observation to fill gap.
    """
    df = df.loc[(df['Time'] >= start_date) & (df['Time'] <= end_date)]
    
    if df.index.name != 'Time':
        df.set_index('Time', inplace = True)
    
    for symbol in symbols:
        #slic the data frame
        df_symbol = df.loc[df['symbol'] == symbol]
    
    # Getting just the adjusted prices. This will return a Pandas DataFrame
    # The index in this DataFrame is the major index of the panel_data.
    price = df_symbol[type_price]
    
    # Getting all weekdays between start_date and end_date
    all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
    
    #Align the existing prices in adj price with our new set of dates.
    # Reindex price using all_weekdays as the new index
    price = price.reindex(all_weekdays)
    
    # Reindexing will insert missing values (NaN) for the dates that were not present
    # in the original set. To cope with this, we can fill the missing by replacing them
    # with the latest available price for each instrument.
    price = price.fillna(method='ffill')
    
    # Plot everything by leveraging the very powerful matplotlib package
    fig, ax = plt.subplots(figsize=(16,9))
    print(price.shape)
    
    ax.plot(price.index, price, label= f'{type_price} price for {symbol}')
    if moving_average_plot:
        # Calculate the 20 and 100 days moving averages of the closing prices
        short_rolling = price.rolling(window=20).mean()
        long_rolling = price.rolling(window=100).mean()
        ax.plot(short_rolling.index, short_rolling, label=f'{short_window} days rolling')
        ax.plot(long_rolling.index, long_rolling, label=f'{long_window} days rolling')
    ax.set_xlabel('Date', fontsize = 16)
    ax.set_title('Price', fontsize = 18)
    ax.set_ylabel('Adjusted closing price ($)', fontsize = 16)
    ax.legend()