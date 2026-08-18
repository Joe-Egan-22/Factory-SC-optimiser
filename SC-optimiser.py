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

    model = model_creation.create_lp_model(data)

    solution = model_solver.solve_model(model)

    reporting.print_solution(solution)

    return #test comment

if __name__ == "__main__": main()

