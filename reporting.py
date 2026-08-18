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
