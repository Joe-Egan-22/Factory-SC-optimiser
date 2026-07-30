import pulp
import pandas as pd
import numpy as np

# Product database input in csv format
PRODUCT_FILE = 'Databases/Finishedproducts.csv'
BOM_FILE = 'Databases/BOMs.csv'
INVENTORY_FILE = 'Databases/Rawmaterials.csv'

'''
FOLLOWING GLOBAL VARIABLES DECIDED BASED ON INTERNET SEARCH, 
NOT INCLUDED IN DATA, NEEDS LATER MODIFICATION
'''

MAX_LABOUR_TIME = 48 #hpw
MAX_MACHINE_TIME = 60 #hpw


def read_data():
    '''
    Create pandas dataframes from csv files in directory.
    Extracting relevant data from these dataframes.
    Returning as a dictionary
    '''
    # Create dataframes
    product_df = pd.read_csv(PRODUCT_FILE, delimiter=',', index_col='ProductID')
    bom_df = pd.read_csv(BOM_FILE, delimiter=',')
    inv_df = pd.read_csv(INVENTORY_FILE, delimiter=',',index_col='MaterialID')

    # Access desired columns from dataframes
    profits = product_df['ProfitPerUnit']
    decision_var_names = product_df.index
    available_mats = inv_df['QuantityInStock']   
    mat_names = inv_df.index
    time_constraints = product_df['MachineHours', 'LabourHours']
    time_constraint_names = time_constraints.columns

    available_time_dict = {
        'MaxLabour': MAX_LABOUR_TIME,
        'MaxMachine': MAX_MACHINE_TIME
    }

    available_time = pd.DataFrame(available_time_dict)
    
    # Pivot bom table to more convenient format
    bom_piv = (bom_df.pivot_table(index='MaterialID', columns='ProductID',values='QuantityRequired',fill_value=0))

    # Access coefficients of material constraints
    mat_coefs = bom_piv


    return {
        "Products": product_df,
        "BOM": bom_df,
        "Inventory": inv_df,
        "Profits": profits,
        "DecisionNames": decision_var_names,
        "ProductionTimes":time_constraints,
        "AvailableMats": available_mats,
        "MatNames": mat_names,
        "TimeConstraintNames": time_constraint_names,
        "MaterialCoeffs": mat_coefs,
        "AvailableTime": available_time
    }


def lp_model(obj_coefs, dec_vars, mat_const_coefs, time_const_coefs, mat_constraint_names, time_constraint_names, mat_rhs, time_rhs):
    '''
    Creates the LP model
    '''

    # Define lp model
    model = pulp.LpProblem('Profit_Maximisation_Problem', pulp.LpMaximize)

    # Create variable names
    X = pulp.LpVariable.dicts('Prod', (i for i in dec_vars), lowBound=0, cat='Continuous')

    # Create linear expression from objective coefficients
    model += (
        pulp.lpSum([
            obj_coefs[i] * X[dec_vars[i]]
            for i in range(len(X))
        ])

    ), 'profit'

    # Use lpSum to create linear expressions from material constraint coefficients
    for i in range(len(mat_const_coefs)):
        model += pulp.lpSum([
            mat_const_coefs[i][j] * X[dec_vars[j]]
            for j in range(len(dec_vars))
            ]) <= mat_rhs[i], mat_constraint_names[i]

    # Use lpSum to create linear expressions from time constraint coefficients
        for i in range(len(time_const_coefs)):
            model += pulp.lpSum([
                time_const_coefs[i][j] * X[dec_vars[j]]
                for j in range(len(dec_vars))
                ]) <= time_rhs[i], time_constraint_names[i]


    return

def test_function():
    '''
    Function to test outputs of individual functions.
    '''
    data = read_data()

    # LHS Coefficients
    objective_coeffs = data["Profits"]
    mat_constraint_coeffs = data["MaterialCoeffs"]
    time_constraint_coeffs = data['MachineHours,LabourHours']

    # RHS Coefficients
    mat_rhs = data['AvailableMats']
    time_rhs = data['AvailableTime']

    # Names
    decision_var_names = data["DecisionNames"]
    mat_constraint_names = data["MatNames"]
    time_constraint_names = data["TimeConstraintNames"]


    lp_prob = lp_model(obj_vector, var_names, mat_constraint_matrix, time_constraint_matrix, mat_constraint_names, time_constraint_names, max_mats, max_times)

    return print(time_constraint_names, mat_constraint_names)



test_function()