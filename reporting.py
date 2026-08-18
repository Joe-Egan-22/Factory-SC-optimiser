def print_solution(solution, objective):
    '''
    Prints the solution to the LP problem
    '''

    # Display solution
    print('-------------------------------------')
    print('               SOLUTION              ')
    print('-------------------------------------')

    products = solution['Products']
    obj = solution['Objective']
    print(products)

    print(f'{objective} = {obj:.2f}')

    return
