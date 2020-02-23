import os
import re
from collections import OrderedDict

# If sort_data.py resides in scripts, navigate to the data folder
os.chdir('../data')

# Get the '/data' folder as a constant
MAIN_DATA_PATH = os.getcwd()


PARTICIPANTS = OrderedDict()
for i in os.listdir(MAIN_DATA_PATH):
    if 'par' in i:
        par_dict[i] = os.path.abspath(os.path.join(MAIN_DATA_PATH, i))

def sort_participant(par_no, par_path):
    par_info = {
        'par_no': par_no,
        'par_path': par_path,
        'eeg_data': os.path.join(par_path, 'eeg_data'),
        'posner_data': os.path.join(par_path, 'posner_data')
    }   
    
    def sort_eeg_files(par_info):
        print('enter_function')
        for file_ in os.listdir(par_info['eeg_data']):
    #         print(file_)

            # Get file no start
            file_no_start = file_.find('.')
            file_no = file_[file_no_start - 1]

            # Get file extension 
            extension_start = file_.find('.')
            file_ext = file_[extension_start:]

            os.rename(os.path.join(par_info['eeg_data'], file_), 
                        os.path.join(par_info['eeg_data'], 'part_' + file_no + file_ext))
    
    def sort_posner_files(par_info):
        for posner_folder in os.listdir(par_info['posner_data']):
            current_posner_part = os.path.join(par_info['posner_data'], posner_folder)
            for file_ in os.listdir(current_posner_part):
    #

                # For each _\d_ in a file name, find the \d position
                file_no_start = (re.search('[_\d_]', file_).start()) + 1

                # Get file extension
                extension_start = re.search('\.\w{3,}', file_).start()
                file_ext = file_[extension_start:]


                os.rename(
                    os.path.join(current_posner_part, file_),
                    os.path.join(current_posner_part, 'part_' + file_[file_no_start] + file_ext)
                )
                
    sort_eeg_files(par_info)
#     sort_posner_files(par_info)
            
for k, v in PARTICIPANTS.items():
    sort_participant(par_no= k, par_path= v)