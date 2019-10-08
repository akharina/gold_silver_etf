import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Set specific parameters for the visualizations
large = 22; med = 16; small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': med,
          'xtick.labelsize': med,
          'ytick.labelsize': med,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.style.use('seaborn-whitegrid')
sns.set_style("white")


def overlapping_density(package=None, input_vars=None, target_vars=None):
    """
    Set the characteristics of your overlapping density plot
    All arguments are set to None purely as a filler right now

    Function takes package name, input variables(categories), and target variable as input.
    Returns a figure

    Should be able to call this function in later visualization code.

    PARAMETERS

    :param package:        should only take sns or matplotlib as inputs, any other value should throw and error
    :param input_vars:     should take the x variables/categories you want to plot
    :param target_vars:    the y variable of your plot, what you are comparing
    :return:               fig to be enhanced in subsequent visualization functions
    """

    # Set size of figure
    fig = plt.figure(figsize=(16, 10), dpi=80)

    # Starter code for figuring out which package to use
    if package == "sns":
        for variable in input_vars:
            sns.kdeplot(...)
    elif package == 'matplotlib':
        for variable in input_vars:
            plt.plot(..., label=None, linewidth=None, color=None, figure = fig)

    return fig



def boxplot_plot(package=None, input_vars=None, target_vars=None):
    """
    Same specifications and requirements as overlapping density plot

    Function takes package name, input variables(categories), and target variable as input.
    Returns a figure

    PARAMETERS

    :param package:        should only take sns or matplotlib as inputs, any other value should throw and error
    :param input_vars:     should take the x variables/categories you want to plot
    :param target_vars:    the y variable of your plot, what you are comparing
    :return:               fig to be enhanced in subsequent visualization functions
    """
    plt.figure(figsize=(16, 10), dpi=80)

    pass


def visualization_one(volatility_set, target_symbol, target_var, output_image_name=None):
    """
    This function is used to visualize the average volatility for each month
    
    :param target_var: variable including (close, open, high, low)
    :target_symbol including 'SLV', 'SIL', 'GLD', 'GDX', 'DJI'
    :volatility_set: a set including volatility ranking and volatility values
    """
    #df_clean = pd.read_csv('data/clean_data.csv')

    monthly_vol_df, VOL_ranking_df = volatility_set
    my_order = monthly_vol_df.groupby("month")["volatility"].mean().sort_values(ascending=False).index

    fig, axes = plt.subplots(2,1, figsize = (14, 14))
    sns.set(style="whitegrid", palette="pastel", color_codes=True)
    g = sns.violinplot(x= 'month', y = 'volatility', data = monthly_vol_df, order = my_order, ax= axes[0]);
    axes[0].set_xlabel('Month', fontsize=20)
    axes[0].set_ylabel('Volatility', fontsize=20);
    axes[0].set_title('Volatility per month', fontsize=20);

    my_order = VOL_ranking_df.groupby("month")["ranking"].mean().sort_values(ascending=False).index
    g1 = sns.barplot(x='month',y='ranking', data = VOL_ranking_df, ax = axes[1], order = my_order)

    groupedvalues=VOL_ranking_df.groupby('month').mean().reset_index()
    for index, order in enumerate(my_order):
        row = groupedvalues.loc[groupedvalues['month'] == order]
        axes[1].text(index-0.2,float(row['ranking'])+0.2,
                     round(float(row['ranking']),2),
                     color='black', ha="center",
                    fontsize = 14)
    axes[1].set_xlabel('Month', fontsize=20);
    axes[1].set_ylabel('Ranking', fontsize=20);
    axes[1].set_title('Ranking based on volatility', fontsize=20);
    #plt.legend()

    # exporting the image to the img folder
    plt.savefig(f'img/{output_image_name}.png', transparent = True, figure = fig)


# please fully flesh out this function to meet same specifications of visualization one

def visualization_two(output_image_name):
    pass

def visualization_three(output_image_name):
    pass

def visualization_four(output_image_name):
    pass