import pulp
import pandas as pd
import numpy as np

# Product database input in csv format
PRODUCT_FILE = 'Databases/Finishedproducts.csv'
BOM_FILE = 'Databases/BOMs.csv'

'''
FOLLOWING GLOBAL VARIABLES DECIDED BASED ON INTERNET SEARCH, 
NOT INCLUDED IN DATA, NEEDS LATER MODIFICATION
'''

LABOUR_CONSTRAINT = 48 #hpw
MACHINE_CONSTRAINT = 60 #hpw


def read_data():
    '''
    Create pandas dataframes from csv files in directory
    '''
    # Create dataframes
    product_df = pd.read_csv(PRODUCT_FILE, delimiter=',', index_col='ProductID')
    bom_df = pd.read_csv(BOM_FILE, delimiter=',', index_col='MaterialID')

    # Access desired columns from dataframes
    profits = product_df['ProfitPerUnit']
    variable_names = product_df['ProductName']
    machine_hours = product_df['MachineHours']
    labour_hours = product_df['LabourHours']


    # Pivot bom table to more convenient format
    bom_piv = (bom_df.pivot_table(index='MaterialID', columns='ProductID',values='QuantityRequired',fill_value=0))

    # Access coefficients of material constraints
    mat_coefs = bom_piv

    '''
    mat_filt_1 = mat_reqs["ProductID"] == 'FP001'
    mats_for_1 = mat_reqs[mat_filt_1]
    '''

    return profits, variable_names, machine_hours, labour_hours, mat_coefs

def lp_model(obj_coefs, dec_vars, const_coefs):
    '''
    Creates the LP model
    '''

    # Define lp model
    model = pulp.LpProblem('Profit Maximisation Problem', pulp.LpMaximize)

    # Create variable names
    X = pulp.LpVariable.dicts('Prod', (i for i in dec_vars), lowBound=0, cat='Continuous')

    return model

def test_function():
    '''
    Function to test outputs of individual functions.
    '''
    data = read_data()

    obj_coef_array = np.array(data[0])
    var_names = data[1].to_dict
    constraint_matrix = data[4]

    lp_model(obj_coef_array, var_names, constraint_matrix)

    return print(data[4])



test_function()