import pandas as pd
import pulp

def create_lp_model(data):
    '''
    Creates the LP model
    '''

    # Create models
    profit_model = pulp.LpProblem('Profit_Maximisation_Problem', pulp.LpMaximize)
    material_model = pulp.LpProblem('Material_Maxmimisation_Problem', pulp.LpMaximize) # We aim to maximise the amount of materials used

    # Create decision variables
    decision_var_names = data["Products"].index
    X = pulp.LpVariable.dicts('Prod', decision_var_names, lowBound=0, cat='Continuous')

    profit_objective_function(profit_model, data, X)
    wastage_objective_function(material_model, data, X)

    apply_constraints(profit_model, data, X)
    apply_constraints(material_model, data, X)

    return {'ProfitModel': profit_model,
            'WastageModel': material_model}

def profit_objective_function(model, data, X):
    '''
    Creates the objective function for profit
    '''

    objective_coeffs = data["Products"]['ProfitPerUnit']

    # Create linear expression from objective coefficients
    model += pulp.lpSum(
        objective_coeffs[p] * X[p]
        for p in objective_coeffs.index
    )

    return model

def material_objective_function(model, data, vars):
    '''
    Creates the objective function for material usage (we wish to maximise this to reduce wastage)
    '''

    objectve_coeffs = data['MatsUsed']

    # Create linear expression from objective coefficients
    model += pulp.lpSum(
        objectve_coeffs[p] * vars[p]
        for p in objectve_coeffs.index
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

def time_constraints(model, data, X):
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

def apply_constraints(model, data, X):
    '''
    Applies all constraints to a LP model
    '''

    material_constraints(model, data, X)
    time_constraints(model, data, X)


    demand_constraints(model, data, X) #Applying results in infeasible solution


    return model