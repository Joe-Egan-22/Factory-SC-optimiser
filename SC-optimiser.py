import pulp
import pandas as pd
import numpy as np

# Product database input in csv format
PRODUCT_FILE = 'Databases/Finishedproducts.csv'


def read_data():
    '''
    Create pandas dataframes from csv files in directory
    '''
    # Create dataframes
    product_df = pd.read_csv(PRODUCT_FILE, delimiter=',', index_col='ProductID')

    # Access desired columns from dataframe
    profits = product_df['ProfitPerUnit']
    variable_names = product_df['ProductName']

    return profits, variable_names

def lp_model():
    '''
    Creates the LP model
    '''

    # define lp model
    model = pulp.LpProblem('Profit Maximisation Problem', pulp.LpMaximize)


    return model

def test_function():
    '''
    Function to test outputs of individual functions.
    '''
    data = read_data()

    obj_coef_array = np.array(data[0])

    return print(obj_coef_array)



test_function()