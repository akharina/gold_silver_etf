import pandas as pd
import numpy as np
def compute_volatility(df, target_var, target_symbol):
    """
    This function compute the average volatility for each month
    
    :param df: input clean data frame
    :param target_var: variable including (close, open, high, low)
    :target_symbol including 'SLV', 'SIL', 'GLD', 'GDX', 'DJI'
    :return VOL_ranking_mean: a data frame including average of
    volatility ranking per month and standard deviation of volatility ranking per month
    :return monthly_vol: the value of volability per month for all years
    """
    df = df.loc[df['symbol'] == target_symbol]
    if df.index.name != 'date':
        df.set_index('date', inplace = True)
    #To compute daily % change and drop the first value
    daily_change = df[target_var].pct_change()
    daily_change.dropna(inplace=True)
    #Use standard deviation as a measure of volatility 
    # and multiplying by sqrt of number of months (12)
    monthly_vol = daily_change.resample('M').std()* np.sqrt(12)
    #Rank the data on ascending order
    ranked_months = pd.DataFrame(monthly_vol.groupby(monthly_vol.index.year).rank()).reset_index()
    ranked_months.columns = ['month', 'ranking']
    ranked_months['month'] = ranked_months['month'].map(lambda x: x.strftime('%b'))
    
    #To build a data frame
    monthly_vol_df = pd.DataFrame(monthly_vol).reset_index()
    monthly_vol_df['date'] = monthly_vol_df['date'].map(lambda x: x.strftime('%b'))
    monthly_vol_df.columns = ['month', 'volatility']
    
    return (monthly_vol_df, ranked_months)