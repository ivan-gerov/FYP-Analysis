# %matplotlib qt # Jupyter

import pandas as pd
import numpy as np
import os
import re
import matplotlib.pyplot as plt
import scipy.io
from functools import reduce
import json

# Loading data from participants
participants = []
for file_ in os.listdir(os.getcwd()):
    if re.match("par_\d", file_) != None:
        participants.append(file_)

# Dictionary of behavioural dataframes { participant : data }
dfs = {}
for par in participants:
    data = os.path.join(os.getcwd(), f"{par}\\data\\behavioural_data.csv")
    dfs[par] = pd.read_csv(data)

print(dfs["par_1"])


def transform_data(df):
    """ Transforms the participant behavioural dataframe to
    a format where each cell has the mean reaction time based on the 
    cueValid/cueInvalid over the lofi, silence and white conditions"""

    # Get the mean over the groupings as explained in the DocString
    df = df.groupby(["cueValid", "condition"]).mean()

    # Original first level of the index are bools, which make
    # Pandas act funky, so change those to 'cueInvalid', 'cueValid'

    def ensure_mapping(index_tuple):
        """ Ensures the correct mapping of the
        cueValidity bool to the new index name"""

        a, b = index_tuple

        if a == True:
            a = "cueValid"
            b = "cueInvalid"
        else:
            b = "cueValid"
            a = "cueInvalid"

        print(f"Index tuple: {index_tuple}")
        print(f"Re-indexed tuple: {(a, b)}")
        return (a, b)

    df.index = df.index.set_levels(ensure_mapping(df.index.levels[0]), level=0)

    # Transpose the DataFrame
    df = df.T

    # Flatten columns
    df.columns = df.columns.map("_".join)

    # Important to remove the index for ease of use
    df.reset_index(drop=True, inplace=True)

    return df


complete_behavioural_data = pd.concat(
    [transform_data(df) for df in dfs.values()], ignore_index=True
)

# Discarding trials where RT > 0.5s ? 
# dfs['par_1'].loc[dfs['par_1']['rt'] > 0.5]

if True:
    complete_behavioural_data.to_csv(
        './rt_mean_over_conditions.csv',
        encoding= 'utf8',
        index= False
    )