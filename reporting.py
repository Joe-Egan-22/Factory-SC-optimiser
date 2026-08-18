def print_solution(solution):
    '''
    Prints the solution to the LP problem
    '''


    # Display solution
    print('-------------------------------------')
    print('               SOLUTION              ')
    print('-------------------------------------')

    products = solution['Products']
    profit = solution['Profit']
    print(products)

    print(f'Profit = {profit:.2f}')

    return
