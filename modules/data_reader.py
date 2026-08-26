import pandas as pd
from modules.config import get_settings

def read_data():
    '''
    Create pandas dataframes from csv files in directory.
    Extracting relevant data from these dataframes.
    Returning as a dictionary
    '''

    settings = get_settings()
    db_dir = settings['database_dir']

    # Create dataframes
    product_df = pd.read_csv(db_dir / "Finishedproducts.csv", delimiter=',', index_col='ProductID')
    bom_df = pd.read_csv(db_dir / "BOMs.csv", delimiter=',')
    inv_df = pd.read_csv(db_dir / "Rawmaterials.csv", delimiter=',',index_col='MaterialID')
    order_df = pd.read_csv(db_dir / "Productionorders.csv", index_col='ProductID')

    # Creating dataframe for maximum time for machining and labour (not given in CSV)
    available_time_dict = {
        'LabourHours': settings['max_labour_time'],
        'MachineHours': settings['max_machine_time']
    }
    available_time = pd.DataFrame(available_time_dict)

    return {
        "Products": product_df,
        "Inventory": inv_df,
        "AvailableTime": available_time,
        "BOM": bom_df,
        "Orders": order_df
    }