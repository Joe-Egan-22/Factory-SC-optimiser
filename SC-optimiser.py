import pulp
import pandas as pd

# Import modules
import data_reader
import validation
import data_prep
import model_creation
import model_solver
import reporting

def main():
    '''
    Function to test outputs of individual functions.
    '''
    data = data_reader.read_data()

    validation.validate_data(data) # will raise errors if needed

    data = data_prep.prepare_data(data)

    models = model_creation.create_lp_model(data)
    profit_model = models['ProfitModel']
    wastage_model = models['WastageModel']

    profit_solution = model_solver.solve_model(profit_model)
    wastage_solution = model_solver.solve_model(wastage_model)

    reporting.print_solution(profit_solution, "Profit")
    reporting.print_solution(wastage_solution, "Materials used")

    return

if __name__ == "__main__": main()

