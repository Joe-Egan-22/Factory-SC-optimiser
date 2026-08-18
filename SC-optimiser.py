import pulp
import pandas as pd

import data_reader

def transform_bom(bom_df):
    '''
    Transforms the validated BOM dataframe to more convenient format
    '''

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
    )

    return bom_piv

def check_cols(df, required_cols, name):
    '''
    Checks for expected columns
    '''

    missing = set(required_cols) - set(df.columns)

    if missing:
        raise ValueError(
            f'{name} is missing columns: {sorted(missing)}'
        )

    return

def cross_check(bom, product, inventory):
    '''
    Checks if whether product and material IDs match between dataframes
    '''

    missing_products = set(bom["ProductID"]) - set(product.index)
    missing_materials = set(bom["MaterialID"]) - set(inventory.index)

    if missing_products:
        raise ValueError(
            f'Product IDs do not match between the BOM and Finished product databases.'
        )

    if missing_materials:
        raise ValueError(
            f'Material IDs do not match between the BOM and Inventory databases.'
        )

    return

def check_nulls(df, name):
    '''
    Checks for missing/null values within a dataframe
    '''

    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]

    if len(missing_cols) > 0:
        raise ValueError(
            f'{name} is missing values in columns: {missing_cols.to_dict()}'
        )

    return

def check_repeats(values, name):
    '''
    Checks for duplicate rows within dataframe
    '''

    duplicates = values[values.duplicated()]

    if len(duplicates) > 0:
        raise ValueError(
            f'{name} contains duplicate IDs: {duplicates.tolist()}'
        )
        

    return

def validate_data(data):
    '''
    Validates input data,
    Ensures dataframes contain necessary information and are labelled correctly
    '''

    # 1) Check columns of each dataframe
    check_cols(data["Products"], {'ProfitPerUnit', 'MachineHours', 'LabourHours'}, "Products")
    check_cols(data['BOM'], {"ProductID", "MaterialID"}, "BOM")
    check_cols(data["Inventory"], {'QuantityInStock'}, "Inventory")
    check_cols(data['Orders'], {'QuantityToProduce'}, "Orders")

    # 2) Check for null values within each dataframe
    check_nulls(data['Products'], "Products")
    check_nulls(data['BOM'], "BOM")
    check_nulls(data['Inventory'], "Inventory")
    check_nulls(data['Orders'], "Orders")

    # 2) Check for repeats in product/material IDs
    check_repeats(data['Products'].index, 'Products')
    cross_check(data['BOM'], data['Products'], data['Inventory'])
    check_repeats(data['Inventory'].index, 'Inventory')
    check_repeats(data['Orders'].index, 'Orders')

    return

def prepare_data(data):
    '''
    Prepares validated and transformed data
    '''

    return {
            "Products": data['Products'],
            "Inventory": data['Inventory'],
            "AvailableTime": data['AvailableTime'],
            "BOM": transform_bom(data['BOM']),
            'Orders': data['Orders']
        }


def create_lp_model(data):
    '''
    Creates the LP model
    '''
   
    decision_var_names = data["Products"].index

    # Define lp model
    model = pulp.LpProblem('Profit_Maximisation_Problem', pulp.LpMaximize)

    # Create decision variable
    X = pulp.LpVariable.dicts('Prod', decision_var_names, lowBound=0, cat='Continuous')

    objective_function(model, data, X)
    material_constraints(model, data, X)
    time_constrains(model, data, X)
    #demand_constraints(model, data, X) #Applying results in infeasible solution

    return model

def objective_function(model, data, X):
    '''
    Creates the objective function for LP problem
    '''

    objective_coeffs = data["Products"]['ProfitPerUnit']

    # Create linear expression from objective coefficients
    model += pulp.lpSum(
        objective_coeffs[p] * X[p]
        for p in objective_coeffs.index
    )

    return model

def material_constraints(model, data, X):
    '''
    Applies material constraints to LP model
    '''

    mat_constraint_coeffs = data["BOM"]
    mat_rhs = data['Inventory']['QuantityInStock']

    # Using lpSum to create linear expression for material constraints
    for material in mat_constraint_coeffs.index:

        model += (
            pulp.lpSum(
                mat_constraint_coeffs.loc[material, product] * X[product]
                for product in data["Products"].index
            )
            <= mat_rhs[material],
            material
        )

    return model

def time_constrains(model, data, X):
    '''
    Applies time constraints to LP model
    '''

    time_constraint_coeffs = data['Products'][['MachineHours', 'LabourHours']].transpose()
    time_rhs = data['AvailableTime'] # Need to have these in CSV

    for constr in time_constraint_coeffs.index: 

            model += (
                pulp.lpSum(
                    time_constraint_coeffs.loc[constr, prod] * X[prod]
                    for prod in data["Products"].index
                )
                <= time_rhs[constr],
                constr
            )

    return model

def demand_constraints(model, data, X):
    '''
    Applies demand constraints
    '''

    min_demands_coefs = data["Orders"]["QuantityToProduce"]

    for product in data['Products'].index:
        model += (
            X[product] >= min_demands_coefs[product],
            f'Min demand of product: {product}'
        )

    return model

def solve_model(model): # may not work, need to fix create_lp_model first
    '''
    Solves LP model
    '''

    status = model.solve(pulp.PULP_CBC_CMD(msg=False))
    status_name = pulp.LpStatus[status]


    if status_name != 'Optimal':
        raise RuntimeError(
            f"Optimisation failed: {pulp.LpStatus[model.status]}"
        )

    solution = {
        v.name: v.value()
        for v in model.variables()
    }

    profit = pulp.value(model.objective)
    
    return solution, profit

def print_solution(model):
    '''
    Prints the solution to the LP problem
    '''

    solution, profit = solve_model(model)

    # Display solution
    print('-------------------------------------')
    print('               SOLUTION              ')
    print('-------------------------------------')

    print(solution)

    print(f'Profit = {profit:.2f}')

    return

def main():
    '''
    Function to test outputs of individual functions.
    '''
    data = data_reader.read_data()

    validate_data(data) # will raise errors if needed

    data = prepare_data(data)

    model = create_lp_model(data)

    print_solution(model)

    return

if __name__ == "__main__": main()

