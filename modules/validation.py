import pandas as pd

def check_cols(df, required_cols, name):
    '''
    Checks for expected columns
    '''

    missing = set(required_cols) - set(df.columns)

    if missing:
        raise ValueError(
            f'{name} is missing columns: {sorted(missing)}'
        )

    return

def cross_check(bom, product, inventory):
    '''
    Checks if whether product and material IDs match between dataframes
    '''

    missing_products = set(bom["ProductID"]) - set(product.index)
    missing_materials = set(bom["MaterialID"]) - set(inventory.index)

    if missing_products:
        raise ValueError(
            f'Product IDs do not match between the BOM and Finished product databases.'
        )

    if missing_materials:
        raise ValueError(
            f'Material IDs do not match between the BOM and Inventory databases.'
        )

    return

def check_nulls(df, name):
    '''
    Checks for missing/null values within a dataframe
    '''

    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]

    if len(missing_cols) > 0:
        raise ValueError(
            f'{name} is missing values in columns: {missing_cols.to_dict()}'
        )

    return

def check_repeats(values, name):
    '''
    Checks for duplicate rows within dataframe
    '''

    duplicates = values[values.duplicated()]

    if len(duplicates) > 0:
        raise ValueError(
            f'{name} contains duplicate IDs: {duplicates.tolist()}'
        )
        

    return

def validate_data(data):
    '''
    Validates input data,
    Ensures dataframes contain necessary information and are labelled correctly
    '''

    # 1) Check columns of each dataframe
    check_cols(data["Products"], {'ProfitPerUnit', 'MachineHours', 'LabourHours'}, "Products")
    check_cols(data['BOM'], {"ProductID", "MaterialID"}, "BOM")
    check_cols(data["Inventory"], {'QuantityInStock'}, "Inventory")
    check_cols(data['Orders'], {'QuantityToProduce'}, "Orders")

    # 2) Check for null values within each dataframe
    check_nulls(data['Products'], "Products")
    check_nulls(data['BOM'], "BOM")
    check_nulls(data['Inventory'], "Inventory")
    check_nulls(data['Orders'], "Orders")

    # 2) Check for repeats in product/material IDs
    check_repeats(data['Products'].index, 'Products')
    cross_check(data['BOM'], data['Products'], data['Inventory'])
    check_repeats(data['Inventory'].index, 'Inventory')
    check_repeats(data['Orders'].index, 'Orders')

    return