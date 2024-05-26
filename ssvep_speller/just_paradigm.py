import psychopy.visual as visual
import psychopy.event as event
import psychopy.core as core
import time
import numpy as np
import pylsl
import random
import csv
import os
import pandas as pd

#Note: the timestamps added to the csv file created here are from psychopy.core, not pylsl

win = None # Global variable for window (Initialized in main)
mrkstream_out = None # Global variable for LSL marker stream output (Initialized in main)
results_in = None # Global variable for LSL result input (Initialized in main)
fixation = None # Global variable for fixation cross (Initialized in main)
training_mode = True # train the model?
bg_color = [0, 0, 0]

def Paradigm():
    win_w = 2736/2
    win_h = 1824/2
    win_size = [win_w, win_h]  # Window size    
    win = visual.Window(win_size, color=[-1, -1, -1], fullscr=True)
        #refresh_rate = 60

    refresh_rate = win.getActualFrameRate()
    if refresh_rate is None:
        print("Could not measure frame rate, assuming 60Hz")
        refresh_rate = 60
    #refresh_rate = 165. # Monitor refresh rate (CRITICAL FOR TIMING)
    #Define the squares (stimuli)
    stim_freqs = [8, 9, 10, 11]  # Frequencies for SSVEP stimuli in Hz
    phase_shift = 0

    # makes random set of training squares and exports to csv file
    training_length = 20
    random.seed()
    training_sequence = pd.DataFrame(columns = ["freq", "shift", "time"])
    red_square_seq = []

    for i in range(training_length):
        red_sq_index = random.randint(0,3)
        red_square_seq.append(red_sq_index)
        new_row = pd.DataFrame({"freq": [stim_freqs[red_sq_index]], "shift": [phase_shift], "time": [None]})
        training_sequence = pd.concat([training_sequence, new_row], ignore_index = True)

    # Directory where the files will be saved
    directory = './training_sequence/'

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)


    ######################## making gui

    stimuli = []
    key_positions = [(-.5,.5), (.5, .5), (-.5, -.5), (.5, -.5)]  # Positions for each key/square
    #keys layout:
    #  0  1
    #  2  3
    
    # Create square stimuli
    stimuli = []
    training_stimuli = []
    for i, pos in enumerate(key_positions):
        square = visual.Rect(win, width=0.2, height=0.3, pos=pos, fillColor=[1, 1, 1], lineColor=None)
        training_square = visual.Rect(win, width=0.2, height=0.3, pos=pos, fillColor=None, lineColor="red", lineWidth=10)
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
                        training_sequence.at[k, "time"] = core.getTime()
                    else:
                        square.draw()
                    

                # Break if there's a keyboard event
                if len(event.getKeys()) > 0:
                    terminate1 = True
                    terminate2 = True


                win.flip()
            # STIMULATORY INTERVAL (FLASHING)
            # 1500ms flicker square stim
            for frame in range(MsToFrames(1500, refresh_rate)):
                current_time = core.getTime()
                for stim_index, square in enumerate(stimuli):


                    if int(current_time * stim_freqs[stim_index]) % 2 == 0: #draw flickers 
                        square.draw()
                    

                # Break if there's a keyboard event
                if len(event.getKeys()) > 0:
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

    event.clearEvents()
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

    # # Export to CSV
    # with open(file_path, 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(training_sequence)
    training_sequence.to_csv(file_path)

    print(f'File saved as: {file_path}')

def MsToFrames(ms, fs):
    dt = 1000 / fs;
    return np.round(ms / dt).astype(int);

Paradigm()
