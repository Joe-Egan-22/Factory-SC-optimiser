import pulp
import pandas as pd

# Import modules
import data_reader
import validation
import data_prep

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

    validation.validate_data(data) # will raise errors if needed

    data = data_prep.prepare_data(data)

    model = create_lp_model(data)

    print_solution(model)

    return

if __name__ == "__main__": main()

