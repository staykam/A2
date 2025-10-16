#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prepdata_sp500.py

Purpose:
    Prepare the data on SP500

Version:
    1       First start, outline for students to start with

Date:
    2025/9/22

Author:
    ???
"""
###########################################################
### Imports
import numpy as np
import pandas as pd
import glob

###########################################################
### df= PrepSPY(dtArg)
import pandas as pd
import numpy as np
import glob

def PrepSPY(dtArg):
    """
    Purpose:
        Read and prepare the data for a specific group of symbols from wide-format Excel files.
    """
    sGlob = f'data/Price*_all_*_i0.xlsx'
    asF = np.sort(glob.glob(sGlob))

    # Get the list of symbol columns we need to keep
    symbols_to_keep = dtArg['symbols'].split() # e.g., ['SPY5.L', 'SPY5z.CHIX', 'SPY5.P']
    
    # Also specify the column to use for the timestamp
    time_column = 'DateTime'
    
    list_of_monthly_dfs = []

    # Loop through each monthly file
    for filename in asF:
        print(f'Processing {filename}...')
        
        # 1. Read the entire Excel file
        temp_df = pd.read_excel(filename)
        
        # 2. Select only the necessary columns: the timestamp and your 3 symbols
        # We create a list of all columns we are interested in
        columns_to_select = [time_column] + symbols_to_keep
        subset_df = temp_df[columns_to_select]
        
        # 3. Reshape the data from "wide" to "long" format using melt()
        # This will create a 'symbol' column and a 'price' column, which is much more flexible.
        long_df = subset_df.melt(id_vars=[time_column], 
                                 var_name='symbol', 
                                 value_name='price')
        
        list_of_monthly_dfs.append(long_df)

    # 4. Combine all the monthly dataframes into one
    df = pd.concat(list_of_monthly_dfs, ignore_index=True)
    
    # 5. Final cleanup: set the timestamp as the index and drop any rows with missing prices
    df = df.set_index(time_column)
    df = df.dropna(subset=['price'])
    
    return df

###########################################################
### main
def main():
    # Magic numbers
    dtArg= {
        'symbols': 'SPY5.L SPY5z.CHIX SPY5.P',        # Change list of symbols to the symbols of your group
        'group': 'g21'
    }

    # Initialisation
    # Initialise(dtArg)

    # Estimation
    df= PrepSPY(dtArg)

    # Output
    sOut= f'output/sp_{dtArg["group"]}.csv'
    df.to_csv(sOut)

    print (f'See {df.shape} observations in {sOut}')
    print ('Beginning of filename:')
    print (df.head())

###########################################################
### start main
if __name__ == "__main__":
    main()
