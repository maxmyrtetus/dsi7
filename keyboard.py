import psychopy.visual
import psychopy.event
import psychopy.core
import time
import numpy as np
import pylsl
import random

win = None # Global variable for window (Initialized in main)
mrkstream_out = None # Global variable for LSL marker stream output (Initialized in main)
results_in = None # Global variable for LSL result input (Initialized in main)
fixation = None # Global variable for fixation cross (Initialized in main)
bg_color = [0, 0, 0]
win_w = 2736/2
win_h = 1824/2
win_size = [win_w, win_h]  # Window size
win = psychopy.visual.Window(win_size, color=[-1, -1, -1], fullscr=True)

refresh_rate = win.getActualFrameRate()
if refresh_rate is None:
    print("Could not measure frame rate, assuming 60Hz")
    refresh_rate = 60

def keyboard():
    # Define the squares (stimuli)
    stim_freqs = [6, 7.5, 8.5, 10]  # Frequencies for SSVEP stimuli in Hz
    prediction = ['TL', 'TR', 'BL', 'BR'][random.randint(0, 3)] # random predict (inclusive)
    stimuli = []
    key_positions = [(-.5,.5), (.5, .5), (-.5, -.5), (.5, -.5)]  # Positions for each key/square

    # Create square stimuli
    stimuli = []
    for i, pos in enumerate(key_positions):
        square = psychopy.visual.Rect(win, width=.2, height=.3, pos=pos, fillColor=[1, 1, 1], lineColor=None)
        stimuli.append(square)

    # Main experiment loop
    terminate1 = False # first while loop
    terminate2 = False # second while loop
    while not terminate1:
        while not terminate2:

            # 1000ms flicker square stim
            for frame in range(MsToFrames(1000, refresh_rate)):
                current_time = psychopy.core.getTime()
                for stim_index, square in enumerate(stimuli):

                    if int(current_time * stim_freqs[stim_index]) % 2 == 0: # on every other frame draw the square
                        square.draw()

                # Break if there's a keyboard event
                if len(psychopy.event.getKeys()) > 0:
                    terminate1 = True
                    terminate2 = True
                    break

                win.flip()

def MsToFrames(ms, fs):
    dt = 1000 / fs;
    return np.round(ms / dt).astype(int);

keyboard()