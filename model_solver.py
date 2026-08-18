import pandas as pd
import pulp

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

    products = {
        v.name: v.value()
        for v in model.variables()
    }

    profit = pulp.value(model.objective)
    
    return {'Products': products, 
            'Profit': profit}
