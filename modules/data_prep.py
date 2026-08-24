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

def summed_bom(pivot_bom):
    '''
    Sums each column of pivoted BOM table and returns series
    '''

    return pivot_bom.sum()

def prepare_data(data):
    '''
    Prepares validated and transformed data
    '''

    modified_bom = transform_bom(data['BOM'])

    return {
            "Products": data['Products'],
            "Inventory": data['Inventory'],
            "AvailableTime": data['AvailableTime'],
            "BOM": modified_bom,
            'Orders': data['Orders'],
            'MatsUsed': summed_bom( modified_bom )
        }