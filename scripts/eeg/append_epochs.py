# %matplotlib qt # Jupyter

import pandas as pd
import numpy as np
import mne
import os
import matplotlib.pyplot as plt
import scipy.io
from functools import reduce

CURRENT_PARTICIPANT = 'par_1'

if CURRENT_PARTICIPANT not in os.listdir(os.getcwd()):
    
    print('Participant folder not found')
    
    EEG_ANALYSIS_PARTICIPANT_FOLDER = os.path.join(os.getcwd(), CURRENT_PARTICIPANT)
    os.mkdir(EEG_ANALYSIS_PARTICIPANT_FOLDER)
    
    PARTICIPANT_MNE_RAW_PATH = os.path.join(EEG_ANALYSIS_PARTICIPANT_FOLDER, 'mne_raw')
    os.mkdir(PARTICIPANT_MNE_RAW_PATH)
    
else:
    print('Participant folder found!')
    EEG_ANALYSIS_PARTICIPANT_FOLDER = os.path.join(os.getcwd(), CURRENT_PARTICIPANT)
    PARTICIPANT_MNE_RAW_PATH = os.path.join(EEG_ANALYSIS_PARTICIPANT_FOLDER, 'mne_raw')

if 'blocks' not in os.listdir(os.getcwd()):
    BLOCKS_FOLDER = os.path.join(EEG_ANALYSIS_PARTICIPANT_FOLDER, 'blocks')
    os.mkdir(BLOCKS_FOLDER)

all_blocks = {
    'lofi': [],
    'white': [],
    'silence': []
}

for file_ in os.listdir(PARTICIPANT_MNE_RAW_PATH):
    if 'lofi' in file_:
        all_blocks['lofi'].append(os.path.join(PARTICIPANT_MNE_RAW_PATH, file_))
    
    elif 'white' in file_:
        all_blocks['white'].append(os.path.join(PARTICIPANT_MNE_RAW_PATH, file_))
        
    elif 'silence' in file_:
        all_blocks['silence'].append(os.path.join(PARTICIPANT_MNE_RAW_PATH, file_))

for k, v in all_blocks.items():
    all_blocks[k] = [mne.read_epochs(epo) for epo in v]
    all_blocks[k] = mne.concatenate_epochs(all_blocks[k])

for block_name, epochs in all_blocks.items():
    epochs.save(f'{BLOCKS_FOLDER}/{block_name}.fif')