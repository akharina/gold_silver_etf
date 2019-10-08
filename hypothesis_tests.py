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


def hypothesis_test_one(alpha = None, cleaned_data):
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

def hypothesis_test_three():
    pass

def hypothesis_test_four():
    pass
