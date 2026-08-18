import pandas as pd

# Product database input in csv format
PRODUCT_FILE = 'Databases/Finishedproducts.csv'
BOM_FILE = 'Databases/BOMs.csv'
INVENTORY_FILE = 'Databases/Rawmaterials.csv'
ORDER_FILE = 'Databases/Productionorders.csv'

'''
FOLLOWING GLOBAL VARIABLES DECIDED BASED ON INTERNET SEARCH, 
NOT INCLUDED IN DATA, NEEDS LATER MODIFICATION
'''

MAX_LABOUR_TIME = 48 #hpw
MAX_MACHINE_TIME = 60 #hpw


def read_data():
    '''
    Create pandas dataframes from csv files in directory.
    Extracting relevant data from these dataframes.
    Returning as a dictionary
    '''
    # Create dataframes
    product_df = pd.read_csv(PRODUCT_FILE, delimiter=',', index_col='ProductID')
    bom_df = pd.read_csv(BOM_FILE, delimiter=',')
    inv_df = pd.read_csv(INVENTORY_FILE, delimiter=',',index_col='MaterialID')
    order_df = pd.read_csv(ORDER_FILE, index_col='ProductID')

    # Creating dataframe for maximum time for machining and labour (not given in CSV)
    available_time_dict = {
        'LabourHours': [MAX_LABOUR_TIME],
        'MachineHours': [MAX_MACHINE_TIME]
    }
    available_time = pd.DataFrame(available_time_dict)

    return {
        "Products": product_df,
        "Inventory": inv_df,
        "AvailableTime": available_time,
        "BOM": bom_df,
        "Orders": order_df
    }