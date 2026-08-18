import pulp
import pandas as pd

# Import modules
import modules.data_reader as data_reader
import modules.validation as validation
import modules.data_prep as data_prep
import modules.model_creation as model_creation
import modules.model_solver as model_solver
import modules.reporting as reporting

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

