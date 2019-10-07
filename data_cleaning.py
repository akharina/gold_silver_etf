import pandas as pd

def rename_columns(df):
    """
    This function is used to rename columns.
    """
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Symbol']
    return df

def change_format(df):
    """
    This function changes the format of the data
    """
    df['Time'] = pd.to_datetime(df['Time'])
    to_be_numeric = ['Open', 'High', 'Low', 'Close', 'Volume'] 
    df[to_be_numeric] = df[to_be_numeric].apply(pd.to_numeric) 
    return df

def clean_SLV(df, scale=10):
    """
    This function adjust the values for SLV.
    """
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume'] 
    df_sliced = df.loc[(df['Symbol'] == 'SLV') & (df['Time'] <= '2008-07-23'), numeric_cols]
    df.loc[(df['Symbol'] == 'SLV') & (df['Time'] <= '2008-07-23'), numeric_cols] = df_sliced / scale
    return df

def full_clean():
    """
    This function is implemented to clean the data.
    """
    #To read the data
    dirty_data = pd.read_csv('data_dirty.csv')
    cleaning_data1 = rename_columns(dirty_data)
    cleaning_data2 = change_format(cleaning_data1)
    cleaning_data3 = clean_SLV(cleaning_data2)
    
    return cleaning_data3