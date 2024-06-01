# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!! MAKE SURE refresh_rate IS SET TO YOUR MONITOR'S REFRESH RATE !!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import psychopy.visual
import psychopy.event
import psychopy.core
import time
import numpy as np
import pylsl
import random
import csv
import os
import pandas as pd
import screeninfo
# Global variables
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!! MAKE SURE refresh_rate IS SET TO YOUR MONITOR'S REFRESH RATE !!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

win = None # Global variable for window (Initialized in main)
mrkstream_out = None # Global variable for LSL marker stream output (Initialized in main)
results_in = None # Global variable for LSL result input (Initialized in main)
fixation = None # Global variable for fixation cross (Initialized in main)
training_mode = True # train the model?
GUI_only_mode = True
bg_color = [0, 0, 0]
monitor_info = screeninfo.get_monitors()[0] #gets info about you monitor (height, width, etc.)
width = monitor_info.width # Width of your monitor in pixels
height = monitor_info.height  # Height of your monitor in pixels

cursor_mode = True
#========================================================
# High Level Functions
#========================================================
def Paradigm():
    win_w = 2736/2
    win_h = 1824/2
    win_size = [win_w, win_h]  # Window size    
    win = psychopy.visual.Window(size = (width, height), units="pix", color=[-1, -1, -1], fullscr=True)
        #refresh_rate = 60

    refresh_rate = win.getActualFrameRate()
    if refresh_rate is None:
        print("Could not measure frame rate, assuming 60Hz")
        refresh_rate = 60
    # refresh_rate = 165. # Monitor refresh rate (CRITICAL FOR TIMING)
    # Define the squares (stimuli)
    stim_freqs = [8, 9, 10, 11]  # Frequencies for SSVEP stimuli in Hz
    phase_shifts = [0.5, 0, 0, 0]

    # makes random set of training squares and exports to csv file
    training_length = 20
    random.seed()
    training_sequence = pd.DataFrame(columns = ["freq", "shift", "time"])
    red_square_seq = []

    for i in range(training_length):
        red_sq_index = random.randint(0,3)
        red_square_seq.append(red_sq_index)
        new_row = pd.DataFrame({"freq": [stim_freqs[red_sq_index]], "shift": [phase_shifts[red_sq_index]], "time": [None]})
        training_sequence = pd.concat([training_sequence, new_row], ignore_index = True)

    # Directory where the files will be saved
    directory = './ssvep_speller/training_sequence/'

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    ######################## making gui

    stimuli = []

    if cursor_mode == True:
        key_positions = [(0, height/2 - 50), (width/2 - 50, 0), (0, -height/2 + 50), (-width/2 + 50, 0)]
    else:
        key_positions = [(-width/4, height/4), (width/4, height/4), (-width/4, -height/4), (width/4, -height/4)]  # Positions for each key/square
    
    # Create square stimuli
    stimuli = []
    training_stimuli = []
    for i, pos in enumerate(key_positions):
        square = psychopy.visual.Rect(win, width=100, height=100, pos=pos, fillColor=[1, 1, 1], lineColor=None)
        training_square = psychopy.visual.Rect(win, width=100, height=100, pos=pos, fillColor=None, lineColor="red", lineWidth=10)
        stimuli.append(square)
        training_stimuli.append(training_square)

    # Main experiment loop
    terminate1 = False # first while loop if key pressed
    terminate2 = False # second while loop if key pressed
    k = 0
    while not terminate1 and k < training_length:
        while not terminate2 and k < training_length:
            # INTERSTIMULATORY INVERVAL (NO FLASHING)
            # 1000ms no flashing
            for frame in range(MsToFrames(1000, refresh_rate)):
                for stim_index, square in enumerate(stimuli):
                    if training_mode:
                        square.draw()
                        training_stimuli[red_square_seq[k]].draw()
                        #update meta dataframe with time red square was shown 
                        training_sequence.at[k, "time"] = pylsl.local_clock()
                    else:
                        square.draw()
                    

                # Break if there's a keyboard event
                if len(psychopy.event.getKeys()) > 0:
                    terminate1 = True
                    terminate2 = True
                if GUI_only_mode != True:
                    mrkstream_out.push_sample(pylsl.vectorstr(["0"])) # isi marker

                win.flip()
            # STIMULATORY INTERVAL (FLASHING)
            # 1500ms flicker square stim
            for frame in range(MsToFrames(1500, refresh_rate)):
                current_time = psychopy.core.getTime()
                for stim_index, square in enumerate(stimuli):
                    if GUI_only_mode != True:
                        mrkstream_out.push_sample(pylsl.vectorstr(["16"])) # si marker

                    if int(current_time * stim_freqs[stim_index]) % 2 == 0: #draw flickers 
                        square.draw()
                    

                # Break if there's a keyboard event
                if len(psychopy.event.getKeys()) > 0:
                    terminate1 = True
                    terminate2 = True
                    break

                win.flip()
            k+=1

        """ # Wait until we get a valid result from the backend
        results = None
        print('Looking for result')
        while results is None:
            results, t = results_in.pull_sample(timeout=0)  
            if results != None:
                break
        
        # Once results found, display them
        text.text = f'Classifier returned: {results[0]}'
        print(f'{text.text}')
        for frame in range(MsToFrames(1000, refresh_rate)):
            text.draw()
            win.flip() """

    ############################## Export to CSV

    psychopy.event.clearEvents()
    win.close()
    # Get the list of existing files in the directory
    existing_files = os.listdir(directory)

    # Initialize the run number
    run_number = 1

    # Iterate through existing files to find the highest run number
    for file in existing_files:
        if file.startswith('training_sequence_run') and file.endswith('.csv'):
            current_run_number = int(file.split('_run')[1].split('.csv')[0])
            if current_run_number >= run_number:
                run_number = current_run_number + 1

    # Construct the new file path with the incremented run number
    file_path = os.path.join(directory, f'training_sequence_run{run_number}.csv')

    # Export to CSV
    # with open(file_path, 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(training_sequence)
    training_sequence.to_csv(file_path)

    print(f'File saved as: {file_path}')

            
def MsToFrames(ms, fs):
    dt = 1000 / fs;
    return np.round(ms / dt).astype(int);

def lsl_mrk_outlet(name):
    info = pylsl.stream_info(name, 'Markers', 1, 0, pylsl.cf_string, 'ID0123456789');
    outlet = pylsl.stream_outlet(info, 1, 1)
    print('task.py created outlet.')
    return outlet
    
def lsl_inlet(name):
    # Resolve all marker streams
    inlet = None
    tries = 0
    info = pylsl.resolve_stream('name', name)
    inlet = pylsl.stream_inlet(info[0], recover=False)
    print(f'task.py has received the {info[0].type()} inlet.')
    return inlet

if __name__ == "__main__":
    # Set random seed
    random.seed()

    if GUI_only_mode != True:
        # Initialize LSL marker streams
        mrkstream_out = lsl_mrk_outlet('Task_Markers') # important this is first
        results_in = lsl_inlet('Result_Stream')

        # Wait a second for the streams to settle down
        time.sleep(1)

        # wait for markerstream to be used by LabRecorder
        while not mrkstream_out.have_consumers():
            psychopy.core.wait(0.2)

        # Run through paradigm
        if mrkstream_out.have_consumers():
            Paradigm()
    else:
        Paradigm()