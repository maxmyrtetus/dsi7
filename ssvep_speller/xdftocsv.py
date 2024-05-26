# THANK YOU CHAT GPT
# entirely written by GPT-4

# Instructions
# Place the XDF file you want to conver in the directory xdf. Run `xdfToCSV.py`. Result
# should be placed in `xdf-results`. There should be two files. One contains the channels
# one contains the markers.

import os
import pyxdf
import pandas as pd
import numpy as np

def save_stream_to_csv(stream, xdf_file, target_dir, stream_index):
    """
    Saves a single stream to a CSV file.
    """
    # Extract common information
    #stream_type = stream['info']['type'][0].replace(' ', '_')
    #stream_name = stream['info']['name'][0].replace(' ', '_')
    stream_type = stream['info']['type'][0] if stream['info']['type'][0] is not None else 'Unknown_Type'
    stream_name = stream['info']['name'][0] if stream['info']['name'][0] is not None else 'Unknown_Name'
    stream_type = stream_type.replace(' ', '_')
    stream_name = stream_name.replace(' ', '_')
    timestamps = stream['time_stamps']
    
    # Determine content based on the presence of time_series or time_stamps
    if 'time_series' in stream:
        content = stream['time_series']
        if isinstance(content[0], list) or isinstance(content[0], np.ndarray):
            # For multi-dimensional data
            columns = [f'Channel_{i+1}' for i in range(len(content[0]))]
        else:
            # For single-dimensional data
            columns = ['Value']
        df = pd.DataFrame(content, columns=columns)
    else:
        # Default to a single column of values if 'time_series' is not present
        df = pd.DataFrame(timestamps, columns=['Timestamps'])
    
    df.insert(0, 'Timestamp', timestamps)
    
    # Construct CSV file name and path
    csv_file_name = f"{xdf_file.replace('.xdf', '')}_Stream{stream_index+1}_{stream_type}_{stream_name}.csv"
    csv_path = os.path.join(target_dir, csv_file_name)
    
    # Save to CSV
    df.to_csv(csv_path, index=False)
    print(f"Saved {stream_type} stream to {csv_path}")

# Source and target directories
source_dir = './xdf_from_lab'
target_dir = './csv_from_xdf'

# Ensure target directory exists
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Process each XDF file in the source directory
for xdf_file in os.listdir(source_dir):
    if xdf_file.endswith('.xdf'):
        xdf_path = os.path.join(source_dir, xdf_file)
        streams, header = pyxdf.load_xdf(xdf_path)
        
        # Save each stream to a separate CSV file
        for i, stream in enumerate(streams):
            save_stream_to_csv(stream, xdf_file, target_dir, i)