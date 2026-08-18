import pandas as pd

def transform_bom(bom_df):
    '''
    Transforms the validated BOM dataframe to more convenient format
    '''

    # Pivot bom table to more convenient format
    bom_piv = (
        bom_df
        .pivot_table(
            index='MaterialID',
            columns='ProductID',
            values='QuantityRequired',
            aggfunc = 'sum',
            fill_value=0,
        )
    )

    return bom_piv

def prepare_data(data):
    '''
    Prepares validated and transformed data
    '''

    return {
            "Products": data['Products'],
            "Inventory": data['Inventory'],
            "AvailableTime": data['AvailableTime'],
            "BOM": transform_bom(data['BOM']),
            'Orders': data['Orders']
        }