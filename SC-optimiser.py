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

LABOUR_CONSTRAINT = 48 #hpw
MACHINE_CONSTRAINT = 60 #hpw


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
    machine_hours = product_df['MachineHours']
    labour_hours = product_df['LabourHours']
    available_mats = inv_df['QuantityInStock']   
    mat_names = inv_df.index
    time_constraint_names = pd.DataFrame("MachineHours", "LabourHours")
    
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
        "MachineHours": machine_hours,
        "LabourHours": labour_hours,
        "AvailableMats": available_mats,
        "MatNames": mat_names,
        "TimeConstraintNames": time_constraint_names,
        "MaterialCoeffs": mat_coefs

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

    obj_vector = data[0].to_numpy()
    var_names = data[1]

    mat_constraint_names = data[6]
    time_constraint_names = data[7]

    # Make matrix of time constraints
    machine_constraint_array = data[2].to_numpy()
    labour_constraint_array = data[3].to_numpy()
    time_constraint_matrix = np.vstack((machine_constraint_array, labour_constraint_array))

    mat_constraint_matrix = data[4].to_numpy()

    # RHS of constraints
    max_mats = data[5].to_numpy()
    max_times = np.array([MACHINE_CONSTRAINT, LABOUR_CONSTRAINT])

    #lp_prob = lp_model(obj_vector, var_names, mat_constraint_matrix, time_constraint_matrix, mat_constraint_names, time_constraint_names, max_mats, max_times)

    return print(time_constraint_names, mat_constraint_names)



test_function()