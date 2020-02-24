# %matplotlib qt # Jupyter

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import scipy.io
from functools import reduce
import json

CURRENT_PARTICIPANT = "par_1"
PART_OF_EXPERIMENT = "part_1"

MAIN_DATA_FOLDER = os.path.abspath("../data")

if CURRENT_PARTICIPANT not in os.listdir(os.getcwd()):

    PARTICIPANT_OUTPUT_FOLDER = os.path.join(os.getcwd(), CURRENT_PARTICIPANT)
    os.mkdir(PARTICIPANT_OUTPUT_FOLDER)

    RAW_FOLDER = os.path.join(PARTICIPANT_OUTPUT_FOLDER, "raw_files")
    os.mkdir(RAW_FOLDER)
else:

    PARTICIPANT_OUTPUT_FOLDER = os.path.join(os.getcwd(), CURRENT_PARTICIPANT)
    RAW_FOLDER = os.path.join(PARTICIPANT_OUTPUT_FOLDER, "raw_files")


def load_data(
    CURRENT_PARTICIPANT=CURRENT_PARTICIPANT,
    PART_OF_EXPERIMENT=PART_OF_EXPERIMENT,
    MAIN_DATA_FOLDER=MAIN_DATA_FOLDER,
):
    """
    Loads posner_data.csv and sequence_of_conditions.json based on the
    current participant and current part of the experiment from the main data folder.
    """

    posner_data_dir = os.path.join(
        MAIN_DATA_FOLDER, CURRENT_PARTICIPANT + "\\posner_data\\" + PART_OF_EXPERIMENT
    )

    # Load posner data into DataFrame
    df = pd.read_csv(os.path.join(posner_data_dir, f"{PART_OF_EXPERIMENT}.csv"))

    # Load sound condition sequence from JSON
    cond_seq = json.load(
        open(os.path.join(posner_data_dir, f"{PART_OF_EXPERIMENT}.json"))
    )

    # Convert sound condition names from "sounds/lofi_track.wav" to "lofi_track"
    for key, val in cond_seq.items():
        slash_start = val.find("/")
        dot_start = val.find(".")
        cond_seq[key] = val[slash_start + 1 : dot_start]

    for key, val in cond_seq.items():
        if "lofi" in val:
            cond_seq[key] = "lofi"
        elif "pink" in val:
            cond_seq[key] = "white"

    return df, cond_seq


df, cond_seq = load_data()


def split_data(df, cond_seq):
    """ 
    Splits the DataFrame into 3 dataframes based on where we have a row. Returns a dict of dataframes - each one is a sound condition block.
    """
    # Find IDs of the empty rows OR where cueOri is None
    empty_rows = np.where(pd.isnull(df["cueOri"]))
    empty_rows = list(empty_rows[0])

    # Transform df into np.ndarray and split it on the IDs of empty rows
    sound_conditions = np.array_split(df, empty_rows)

    # Due to glitchy PsychoPy script, it returns 4 ndarrays. We take only the first three
    sound_conditions = sound_conditions[:3]

    # Match index of sound condition from sound_conditions and cond_seq
    # and put that into the df_collection
    df_collection = {}

    for index, condition_data in enumerate(sound_conditions):
        df_collection[cond_seq[str(index + 1)]] = condition_data

    return df_collection


df_collection = split_data(df, cond_seq)


def transform_df(cond_name, df: pd.DataFrame):
    """
    Returns a sound condition DataFrame in the correct format + removes all unnecessary columns
    """
    df.rename(
        columns={"correct_key_resp.rt": "rt", "correct_key_resp.keys": "corr_resp"},
        inplace=True,
    )

    df = df.loc[df["correct_key_resp.corr"] == 1.0]
    df = df.loc[df["early_resp.keys"] == "None"]

    # Create condition column
    df["condition"] = cond_name

    # Create cueValid column
    df["cueValid"] = ""

    # Right Cue + Right Target = Valid
    df.loc[(df["cueOri"] == 180.0) & (df["targetX"] == 0.5), "cueValid"] = True

    # Left Cue + Left Target = Valid
    df.loc[(df["cueOri"] == 0.0) & (df["targetX"] == -0.5), "cueValid"] = True

    # Right Cue + Left Target = Invalid
    df.loc[(df["cueOri"] == 180.0) & (df["targetX"] == -0.5), "cueValid"] = False

    # Left Cue + Right Target = Invalid
    df.loc[(df["cueOri"] == 0.0) & (df["targetX"] == 0.5), "cueValid"] = False

    # Removing all unncessesary columns
    df = df.loc[:, ["condition", "cueValid", "rt"]]

    df.reset_index(inplace=True, drop=True)

    return df


for key, val in df_collection.items():
    df_collection[key] = transform_df(cond_name=key, df=val)

for key, val in df_collection.items():
    val.to_csv(
        os.path.join(RAW_FOLDER, f"{key}_{PART_OF_EXPERIMENT}.csv"),
        encoding="utf8",
        index=False,
    )
