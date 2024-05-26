import pandas as pd
import os

def mark_data(eeg_path, markers_path):
    eeg = pd.read_csv(eeg_path)
    markers = pd.read_csv(markers_path)

    eeg['Marker'] = 0
    for i in range(len(markers)-1):
        if markers['Channel_1'].iloc[i] == 16 and markers['Channel_1'].iloc[i+1] == 16:
            eeg.loc[(eeg['Timestamp'] > markers['Timestamp'].iloc[i]) & 
                    (eeg['Timestamp'] < markers['Timestamp'].iloc[i+1]), 'Marker'] = 16

    if markers['Channel_1'].iloc[0] == 16:
        eeg.loc[eeg['Timestamp'] < markers['Timestamp'].iloc[0], 'Marker'] = 16
    elif markers['Channel_1'].iloc[0] == 0:
        eeg.loc[eeg['Timestamp'] < markers['Timestamp'].iloc[0], 'Marker'] = 0

    if markers['Channel_1'].iloc[-1] == 16:
        eeg.loc[eeg['Timestamp'] > markers['Timestamp'].iloc[-1], 'Marker'] = 16
    elif markers['Channel_1'].iloc[-1] == 0:
        eeg.loc[eeg['Timestamp'] > markers['Timestamp'].iloc[-1], 'Marker'] = 0

    eeg_filename = os.path.basename(eeg_path)
    marked_data_path = './ssvep_speller/marked-data'
    if not os.path.exists(marked_data_path):
        os.makedirs(marked_data_path)
    eeg.to_csv(os.path.join(marked_data_path, 'marked_' + eeg_filename), index=False)

# Source and target directories
eeg_path = './ssvep_speller/csv_from_xdf'
markers_path = './ssvep_speller/training_sequence'

# Ensure target directory exists
if not os.path.exists(eeg_path):
    os.makedirs(eeg_path)

#source_dir = './xdf_from_lab'
#target_dir = './csv_from_xdf'

eeg_files = sorted([file for file in os.listdir(eeg_path) if file.endswith('dsi-7.csv')])
print("EEG files to process:", eeg_files)  # Debug to check what files are ready to be processed

marker_files = sorted([file for file in os.listdir(eeg_path) if file.endswith('Task_Markers.csv')])  # Adjusted for marker files
print("Marker files to process:", marker_files)  # Debug to check marker files

for eeg_file, marker_file in zip(eeg_files, marker_files):
    csv_path_eeg = os.path.join(eeg_path, eeg_file)
    csv_path_markers = os.path.join(eeg_path, marker_file)
    print(csv_path_eeg, csv_path_markers)
    print(f"Processing EEG file: {csv_path_eeg} with Marker file: {csv_path_markers}")  # Debug to confirm files being processed
    mark_data(csv_path_eeg, csv_path_markers)
