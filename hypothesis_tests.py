import pandas as pd
import numpy as np
from scipy import stats
import math
from sklearn.utils import resample
import matplotlib.pyplot as plt


def bootstrap_sim(df, target_var, target_symbol, n_sim = 1000):
    """
    This function gets the clean dataframe and compute the daily % 
    change. Then, it does resampling and geneate n_sim from daily % 
    change.  

    :param df: the input clean data frame
    :param target_var: variable including (close, open, high, low)
    :target_symbol including 'SLV', 'SIL', 'GLD', 'GDX', 'DJI'
    :n_sim it is the number of simulation
    :return 

    """
    df = df.loc[df['symbol'] == target_symbol]
    if df.index.name != 'date':
        df.set_index('date', inplace = True)
    #To compute daily % change and drop the first value
    daily_change = df[target_var].pct_change()
    daily_change.dropna(inplace=True)
    
    #To build an empty dataframe
    df_sim = pd.DataFrame()
    length = len(daily_change)
    count=0
    
    for i in range(n_sim):
        #sample same size as dataset, drop timestamp

        daily_change_sampling= resample(daily_change, replace=True, n_samples=length).reset_index(drop=True)
        
        
        #Add timestamp to shuffled data
        daily_change_sampling.index = df.index[1:]
        
        
        #Use standard deviation as a measure of volatility 
        # and multiplying by sqrt of number of months (12)
        monthly_vol_sampling = daily_change_sampling.resample('M').std()* np.sqrt(12)
        
        
        #Rank the data on ascending order
        
        ranked_months_sampling = pd.DataFrame(monthly_vol_sampling.groupby(monthly_vol_sampling.index.year).rank()).reset_index()
        
        ranked_months_sampling.columns = ['month', 'ranking']
        
        ranked_months_sampling['month'] = ranked_months_sampling['month'].map(lambda x: x.strftime('%b'))
        
        sim_ranking = ranked_months_sampling.groupby('month').mean()
        
        #add each of 1000 sims into df
        df_sim = pd.concat([df_sim,sim_ranking],axis=1)
    all_ranking = df_sim.values.flatten()
    

    return df_sim, all_ranking



def create_sample_dists(cleaned_data, y_var=None, categories=[]):
    """
    Each hypothesis test will require you to create a sample distribution from your data
    Best make a repeatable function

    :param cleaned_data:
    :param y_var: The numeric variable you are comparing
    :param categories: the categories whose means you are comparing
    :return: a list of sample distributions to be used in subsequent t-tests

    """
    htest_dfs = []

    # Main chunk of code using t-tests or z-tests
    return htest_dfs

def compare_pval_alpha(p_val, alpha):
    status = ''
    if p_val > alpha:
        status = "Fail to reject"
    else:
        status = 'Reject'
    return status


def hypothesis_test_one(alpha, VOL_ranking_df, df_clean, target_var, target_symbol, plot_option = False, month_plot ='Nov'):
    """
    By: Jalal Kiani
    Over the past 13 years, October has been the most volatile month 
    on average for the GLD stock and December the least volatile. The question
    is whether this is a persistent signal or just noise in the data?
    
    The goal of this function, here, is to statiscally analyze and test
    this phenomena to check whether is statistically significant or not.
    
    H0 : mu(for each month) = xbar the observed phenomena is not due chance
    HA : mu(for each month) not(=) xbar the observed phenomena is due chance
    
    :param alpha: the critical value of choice
    :param cleaned_data: the cleaned data including GLD prices used used 
    for hypothesis testing
    :return Pvalue,  This function return 
    """
    # Get data for tests
    df_sim, all_ranking = bootstrap_sim(df_clean, target_var, target_symbol, 1000)
    VOL_ranking_mean = VOL_ranking_df.groupby('month').mean().reset_index()
    mean_ranking = all_ranking.mean()
    VOL_ranking_mean['pvalue'] = 2*VOL_ranking_mean['ranking'].\
    map(lambda x: np.sum(all_ranking > x) / all_ranking.shape[0]\
        if x > mean_ranking else np.sum(all_ranking < x) / all_ranking.shape[0])
    
    for month, p_val in zip(VOL_ranking_mean['month'], VOL_ranking_mean['pvalue']):
        # starter code for return statement and printed results
        status = compare_pval_alpha(p_val, alpha)
        assertion = ''
        if status == 'Fail to reject':
            assertion = 'cannot'
        else:
            assertion = "can"
        print(f'Based on the p value of {round(p_val,2)} and our aplha of {alpha} we {status.lower()}  the null hypothesis.'
              f'\n Due to these results, we  {assertion} state that the seasonality in the volatility is due to chance in {month}')
        print('-'*100)
    if plot_option:
        fig, ax = plt.subplots(1,1,figsize = (14, 5));
        n, bins, patches = plt.hist(all_ranking, bins = 30, color = 'b', density = True);
        ax.set_ylabel('Probability density', fontsize=20);
        ax.set_xlabel('Average Ranking', fontsize=20);
        ax.set_title('Bootstrapping results', fontsize=20);
        upper_bound = float(VOL_ranking_mean.loc[VOL_ranking_mean['month'] == month_plot]['ranking'])
        lower_bound = mean_ranking - (upper_bound - mean_ranking)
        upper_bound = bins[(np.abs(bins - upper_bound)).argmin()]
        lower_bound = bins[(np.abs(bins - lower_bound)).argmin()]
        ax.axvline(upper_bound,color='r',ls='--', label='Dec Result',lw=3)
        ax.axvline(lower_bound,color='r',ls='--', label='Dec Result',lw=3)
        for c, p in zip(bins, patches):
            if c < lower_bound or c >= upper_bound:
                plt.setp(p, 'facecolor', 'r')
        pvalue = float(VOL_ranking_mean.loc[VOL_ranking_mean['month'] == month_plot]['pvalue'])
        ax.text(3.5, 0.3, f'P-value = {round(pvalue, 2)}', fontsize=16)
        plt.savefig(f'img/bootstraping_{target_symbol}_{month_plot}.png', transparent = True, figure = fig)
    return VOL_ranking_mean

def hypothesis_test_two():
    pass

def hypothesis_test_three():
    pass

def hypothesis_test_four():
    pass
