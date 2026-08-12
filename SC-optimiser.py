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

    # Creating dataframe for maximum time for machining and labour (not given in CSV)
    available_time_dict = {
        'LabourHours': [MAX_LABOUR_TIME],
        'MachineHours': [MAX_MACHINE_TIME]
    }
    available_time = pd.DataFrame(available_time_dict)
    
    # Pivot bom table to more convenient format
    bom_piv = (
        bom_df
        .pivot_table(
            index='MaterialID',
            columns='ProductID',
            values='QuantityRequired',
            aggfunc = 'sum',
            fill_value=0,
        )
        .reindex(
            index = inv_df.index,
            columns = product_df.index,
            fill_value=0,
        )
    )
    return {
        "Products": product_df,
        "BOM": bom_piv,
        "Inventory": inv_df,
        "AvailableTime": available_time
    }

def check_names(df, required_cols, name):
    '''
    Checks for expected columns
    '''

    missing = set(required_cols) - set(df.columns)

    if missing:
        raise ValueError(
            f'{name} is missing columns: {sorted(missing)}'
        )

    return


def validate_data(data):
    '''
    Validates input data,
    Ensures dataframes contain necessary information and are labelled correctly
    '''

    # 1) Check columns of each dataframe
    check_names(data["Products"], {'ProfitPerUnit', 'MachineHours', 'LabourHours'}, "Products")
    check_names(data["BOM"], data['Products'].index, "BOM")
    check_names(data["Inventory"], {'QuantityInStock'}, "Inventory")

    

    return

def create_lp_model(data):
    '''
    Creates the LP model
    '''
    
    # LHS Coefficients
    objective_coeffs = data["Products"]['ProfitPerUnit']
    mat_constraint_coeffs = data["BOM"]
    time_constraint_coeffs = data['Products'][['MachineHours', 'LabourHours']].transpose()

    # RHS Coefficients
    mat_rhs = data['Inventory']['QuantityInStock']
    time_rhs = data['AvailableTime'] # Need to have these in CSV

    # Names
    decision_var_names = data["Products"].index

    # Define lp model
    model = pulp.LpProblem('Profit_Maximisation_Problem', pulp.LpMaximize)

    # Create variable names
    X = pulp.LpVariable.dicts('Prod', decision_var_names, lowBound=0, cat='Continuous')

    # Create linear expression from objective coefficients
    model += pulp.lpSum(
        objective_coeffs[p] * X[p]
        for p in objective_coeffs.index
    )

    # Using lpSum to create linear expression for material constraints
    for material in mat_constraint_coeffs.index:

        model += (
            pulp.lpSum(
                mat_constraint_coeffs.loc[material, product] * X[product]
                for product in decision_var_names
            )
            <= mat_rhs[material],
            material
        )

    for constr in time_constraint_coeffs.index: 

        model += (
            pulp.lpSum(
                time_constraint_coeffs.loc[constr, prod] * X[prod]
                for prod in decision_var_names
            )
            <= time_rhs[constr],
            constr
        )

    return model

def solve_model(model): # may not work, need to fix create_lp_model first
    '''
    Solves and displays LP model
    '''
    # Solve model
    model.solve(pulp.PULP_CBC_CMD(msg=False))

    # Display solution
    print('-------------------------------------')
    print('               SOLUTION              ')
    print('-------------------------------------')

    print('')
    print(pulp.LpStatus[model.status])
    print('')

    for v in model.variables():
        print(f"{v}: {v.value():.2f}")

    print("Profit =", pulp.value(model.objective))

    return None

def test_function():
    '''
    Function to test outputs of individual functions.
    '''
    data = read_data()

    validate_data(data)

    #model = create_lp_model(data)

    #solve_model(model)

    return None

test_function()