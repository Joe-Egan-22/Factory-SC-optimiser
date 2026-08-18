import pulp
import pandas as pd

# Import modules
import data_reader
import validation
import data_prep
import model_creation

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

    model = model_creation.create_lp_model(data)

    print_solution(model)

    return

if __name__ == "__main__": main()

