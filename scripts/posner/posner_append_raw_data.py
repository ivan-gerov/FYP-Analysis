# %matplotlib qt # Jupyter

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import scipy.io
from functools import reduce
import json

CURRENT_PARTICIPANT = 'par_11'

PARTICIPANT_FOLDER = os.path.join(os.getcwd(), CURRENT_PARTICIPANT)
RAW_FOLDER = os.path.join(PARTICIPANT_FOLDER, 'raw_files')
DATA_APPENDED = os.path.join(PARTICIPANT_FOLDER, 'data')

if 'data' not in os.listdir(PARTICIPANT_FOLDER):
    os.mkdir(DATA_APPENDED)

# Get each separate sound condition table into a collection dict
all_data = {
    'lofi': [],
    'white': [],
    'silence': []
}

for file_ in os.listdir(RAW_FOLDER):
    if 'lofi' in file_:
        all_data['lofi'].append(
            pd.read_csv(os.path.join(RAW_FOLDER, file_))
        )
    elif 'white' in file_:
        all_data['white'].append(
            pd.read_csv(os.path.join(RAW_FOLDER, file_))
        )
    elif 'silence' in file_:
        all_data['silence'].append(
            pd.read_csv(os.path.join(RAW_FOLDER, file_))
        )

# Concatenate each sound condition table into a single homogenous table
for key, value in all_data.items():
    all_data[key] = pd.concat([value[0], value[1], value[2]],
                             ignore_index= True)


# Concatenate each table into a single table containing all of the behavioural data
data = pd.concat([df for df in all_data.values()], ignore_index= True)

# Save behavioural data
data.to_csv(
    os.path.join(DATA_APPENDED, 'behavioural_data.csv'),
    encoding= 'utf8',
    index= False
)