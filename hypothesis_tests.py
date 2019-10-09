"""
This module is for your final hypothesis tests.
Each hypothesis test should tie to a specific analysis question.

Each test should print out the results in a legible sentence
return either "Reject the null hypothesis" or "Fail to reject the null hypothesis" depending on the specified alpha
"""

import pandas as pd
import numpy as np
from scipy import stats
import math


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


def hypothesis_test_one(cleaned_data, alpha=None):
    """
    Describe the purpose of your hypothesis test in the docstring
    These functions should be able to test different levels of alpha for the hypothesis test.
    If a value of alpha is entered that is outside of the acceptable range, an error should be raised.

    :param alpha: the critical value of choice
    :param cleaned_data:
    :return:
    """
    # Get data for tests
    comparison_groups = create_sample_dists(cleaned_data=None, y_var=None, categories=[])

    ###
    # Main chunk of code using t-tests or z-tests, effect size, power, etc
    ###

    # starter code for return statement and printed results
    status = compare_pval_alpha(p_val, alpha)
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        # calculations for effect size, power, etc here as well

    print(f'Based on the p value of {p_val} and our aplha of {alpha} we {status.lower()}  the null hypothesis.'
          f'\n Due to these results, we  {assertion} state that there is a difference between NONE')

    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {str(coh_d)} and power of {power}.")
    else:
        print(".")

    return status


def hypothesis_test_two():
    pass


def hypothesis_test_three_prep(df_clean, type=None, alpha=0.05):
    '''Prepares dataset for paired t-test.
       Signature: hypothesis_test_three_prep(df, type= None, alpha=0.05).
       type options: day, week, month'''

    df_clean['daily_movement'] = (df_clean.close-df_clean.open)*100/df_clean.open
    df_clean = df_clean.loc[df_clean['date'] >= '2014-10-06']
    df_clean_SLV = df_clean.loc[df_clean['symbol'] == 'SLV'][[
        'date', 'symbol', 'open', 'close', 'daily_movement']]
    df_clean_GLD = df_clean.loc[df_clean['symbol'] == 'GLD'][[
        'date', 'symbol', 'open', 'close', 'daily_movement']]

    if type == 'day':
        df_slv_vs_gld = pd.merge(df_clean_SLV,
                                 df_clean_GLD,
                                 how='left',
                                 on='date',
                                 suffixes=('_SLV', '_GLD'))
        df_slv_vs_gld['delta'] = df_slv_vs_gld['daily_movement_SLV'] - \
            df_slv_vs_gld['daily_movement_GLD']

    # Remove outliers
        data = df_slv_vs_gld[(np.abs(stats.zscore(
            df_slv_vs_gld[['daily_movement_SLV', 'daily_movement_GLD', 'delta']])) < 3).all(axis=1)]

        a = df_slv_vs_gld['daily_movement_SLV']
        b = df_slv_vs_gld['daily_movement_GLD']

    elif type == 'week':
        gld_weekly = df_clean_GLD.groupby(['symbol', pd.Grouper(key='date', freq='W')]).mean(
        ).reset_index().sort_values('date', ascending=False)[['date', 'open', 'close']]
        slv_weekly = df_clean_SLV.groupby(['symbol', pd.Grouper(key='date', freq='W')]).mean(
        ).reset_index().sort_values('date', ascending=False)[['date', 'open', 'close']]

        gld_weekly['wk_movement'] = (gld_weekly.open-gld_weekly.close)*100/gld_weekly.open
        slv_weekly['wk_movement'] = (slv_weekly.open-slv_weekly.close)*100/slv_weekly.open

        df_slv_vs_gld_wk = pd.merge(slv_weekly,
                                    gld_weekly,
                                    how='left',
                                    on='date',
                                    suffixes=('_SLV', '_GLD'))

        # Remove outliers
        df_slv_vs_gld_wk = df_slv_vs_gld_wk[(
            np.abs(stats.zscore(df_slv_vs_gld_wk[['wk_movement_SLV', 'wk_movement_GLD']])) < 3).all(axis=1)]

        a = df_slv_vs_gld_wk['wk_movement_SLV']
        b = df_slv_vs_gld_wk['wk_movement_GLD']

    elif type == 'month':

        gld_monthly = df_clean_GLD.groupby(['symbol', pd.Grouper(key='date', freq='M')]).mean(
        ).reset_index().sort_values('date', ascending=False)[['date', 'open', 'close']]
        slv_monthly = df_clean_SLV.groupby(['symbol', pd.Grouper(key='date', freq='M')]).mean(
        ).reset_index().sort_values('date', ascending=False)[['date', 'open', 'close']]

        gld_monthly['mo_movement'] = (gld_monthly.open-gld_monthly.close)*100/gld_monthly.open
        slv_monthly['mo_movement'] = (slv_monthly.open-slv_monthly.close)*100/slv_monthly.open

        df_slv_vs_gld_mo = pd.merge(slv_monthly,
                                    gld_monthly,
                                    how='left',
                                    on='date',
                                    suffixes=('_SLV', '_GLD'))

        # Remove outliers
        df_slv_vs_gld_mo = df_slv_vs_gld_mo[(
            np.abs(stats.zscore(df_slv_vs_gld_mo[['mo_movement_SLV', 'mo_movement_GLD']])) < 3).all(axis=1)]

        a = df_slv_vs_gld_mo['mo_movement_SLV']
        b = df_slv_vs_gld_mo['mo_movement_GLD']

    return a, b


def hypothesis_test_three_pttest(a, b, alpha=0.05):
    ''' Perform paired ttest.
        Parameters:
        a,b = array_like. The arrays must have the same shape.'''

    t_val, p_val = stats.ttest_rel(a, b)
    print(f"t_val = {t_val}, p_val = {p_val}")

    status = compare_pval_alpha(p_val, alpha)
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"

    # calculations for effect size, power, etc here as well
    spooled_S = np.sqrt(((a.std()**2 + b.std()**2)/2))
    coh_d = (a.mean() - b.mean()) / spooled_S
    
    print(f'Based on the p value of {p_val} and our alpha of {alpha} we {status.lower()}  the null hypothesis.'
          f'\nDue to these results, we  {assertion} state that there is a difference between daily movement of SLV and GLD')

    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {str(coh_d)}.")
    else:
        print(".")

    return status


def hypothesis_test_four():
    pass
