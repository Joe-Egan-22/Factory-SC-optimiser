import pandas as pd

def print_solution(solution, objective):
    '''
    Prints the solution to the LP problem
    '''

    # Display solution
    print('--------------------------------------------')
    print(f'     SOLUTION TO {objective.upper()} PROBLEM       ')
    print('--------------------------------------------')

    products = solution['Products']
    obj = solution['Objective']
    print(products)

    print(f'{objective} = {obj:.2f}')

    return

def create_dataframe(solution):
    '''
    Takes solution and displays in a pandas dataframe
    '''


    prod_df = pd.DataFrame(solution['Products'])
    obj_df = pd.DataFrame(solution['Objective'], columns=['Profit'])

    sol_df = pd.concat([prod_df, obj_df], axis=1)

    return print(sol_df)