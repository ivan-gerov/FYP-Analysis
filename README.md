# Investigating the effects of background beats on visual attention: an EEG and behavioural study of Lo-Fi Hip Hop - Project Folder Guide

This is a project data folder comprising of participant raw data, processed data, processing pipelines and scripts in Python, Jupyter and Matlab, SPSS analyses and questionnaire data.


# Table of Contents <a id="toc"> </a>
1. [Project Structure](#par_data)
2. [Installation](#install)
3. [Opening data pipelines](#usage)
4. [Credits](#credits)

# 1. Project Structure <a id="par_data"> </a>
[[back to top]](#toc)

 The Project folder comprises of three data folders (**data, posner_analysis and eeg_data**), a **scripts** folder and **sounds** for the audio stimuli.:
*  **root/data** - folder with raw EEG and Behavioural data for each participant divided into three parts (each part consisting of 3 blocks on the attentional task, total of 9 blocks per participant), with the following data structure: 
    ```
    root dir
    |
    |---data
        | survey_answers.csv (questionnaire answers)
        | basic_descriptives.ipynb (jupyter notebook)
        |
        |---par_1
            |
            |---eed_data
            |   | part_1.mat
            |   | part_2.mat
            |   | part_3.mat
            |
            |---posner_data
                |---part_1
                    | part_1.csv
                |---part_2
                    | part_2.csv                    
                |---part_3
                    | part_3.csv                           
    ```
* **root/posner_analysis** - pre-processed Behavioural data. After the final pre-processing data pipeline, each participant's Behavioural data was cleaned from any unnessesary columns and appended into a combined `behavioural_data.csv` file. The table in `rt_mean_over_conditions.csv` has the mean of all participants' reaction times over both the visual and sound factors. Jupyter notebooks hold the data processing pipelines. There is also an SPSS analysis file.
    ```
    root dir
    |
    |---posner_analysis
        | posner_preprocessing.ipynb
        | final_preprocessing.ipynb
        | append_raw_data.ipynb
        | rt_mean_over_conditions.csv
        |
        |---par_1
            |
            |---data
                | behavioural_data.csv
        |---spss
            | two_way_anova.sav
    ```
* **root/eeg_analysis** - pre-processed EEG data. After processing and cleaning the raw EEG data with Pandas, Jupyter, NumPy and MNE - all data was appended and divided into blocks per each sound condition.
    ```
    root dir
    |
    |---eeg_analysis
        | append_raw_data.ipynb
        | eeg_preprocessing.ipynb
        |
        |---par_1
            |
            |---blocks
                | lofi.fif
                | silence.fif
                | white.fif
        |
        |---FieldTrip_processing (data after FieldTrip pipeline)
        |
        |---post_field_trip_processing (data restructured and appended after FieldTrip analysis, also holds two data pipelines)
            | restructuring_fieldtrip_data.ipynb
            | append_left_right_ERP_channels.ipynb
    ```

# 2. Installation <a id="install"></a>
[[back to top]](#toc)
1. Ensure you first have Python 3.7.3 installed on your computer.
2. Create a new folder for the project. That will be the root project folder.
3. In the folder open a command line terminal and create a virtual environment for the correct packaging of the libraries by writing `python -m venv env` in the terminal.
4. Install the dependancies from the **requirements.txt** file by:
    * Enter into the virtual environment from the terminal with - `env/scripts/activate.ps1`
    * Using the **pip** python package manager to install the dependancies by invoking `pip install -r requirements.txt` in the terminal.

# 3. Opening the data processing pipelines <a id="usage"> </a>
[[back to top]](#toc)
1. Open the command line terminal in the root folder of the project.
2. Open Jupyter by calling `jupyter notebook` in the terminal.
3. Browse to any of the **.ipynb** files and open them with Jupyter.

# 4. Credits <a id="credits"></a>
[[back to top]](#toc)

* **Ivan Gerov** - Project Lead - data collection, Behavioural and EEG data processing and statistical analysis, developing of Posner attentional task with PsychoPy.
* **Dr. Johanna Zumer** - Project Supervisor - for helping with theoretical basis of the project, for guidance with methodological direction and contributing with Matlab FieldTrip EEG data processing and analysis pipelines, advice and help with project report writing.
* **Prof. Amanda Wood** - Project Supervisor - for advice and help with project report writing.

