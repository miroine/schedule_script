import pandas as pd
import numpy as np

def generate_random_production_dataframe(num_fields=5, num_rows=50, 
                                         columns=['FGPR', 'FOPR', 'FWPR'], start_date='2023-01-01', freq='D'):

    """Generates a random production dataframe to test for schedule

    Returns:
        _type_: _description_
    """
    dfs = []
    for i in range(num_fields):
        # Generate random numbers
        random_numbers = np.random.rand(num_rows, len(columns)) *1000
        # Create a date range for the index
        date_range = pd.date_range(start=start_date, periods=num_rows, freq=freq)

        # Create the DataFrame
        temp =pd.DataFrame(random_numbers, index=date_range, columns=columns)
        temp ['FIELD'] = f'FIELD_{i}'
        dfs.append(temp)

    # Concatenate the DataFrames
    df = pd.concat(dfs)
    mother_field = {'FIELD_0':'FIELD', 'FIELD_1':'FIELD', 'FIELD_2':'FIELD_0', 'FIELD_3':'FIELD_1','FIELD_4':'FIELD_1'}
    df['MOTHER_FIELD'] = df.FIELD.map(mother_field)
    return df

