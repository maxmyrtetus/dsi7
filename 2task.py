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

# Global variables
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!! MAKE SURE refresh_rate IS SET TO YOUR MONITOR'S REFRESH RATE !!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

win = None # Global variable for window (Initialized in main)
mrkstream_out = None # Global variable for LSL marker stream output (Initialized in main)
results_in = None # Global variable for LSL result input (Initialized in main)
fixation = None # Global variable for fixation cross (Initialized in main)
training = False # train the model?
bg_color = [0, 0, 0]
win_w = 2736/2
win_h = 1824/2
win_size = [win_w, win_h]  # Window size    
win = psychopy.visual.Window(win_size, color=[-1, -1, -1], fullscr=True)
    #refresh_rate = 60

refresh_rate = win.getActualFrameRate()
if refresh_rate is None:
    print("Could not measure frame rate, assuming 60Hz")
    refresh_rate = 60
#refresh_rate = 165. # Monitor refresh rate (CRITICAL FOR TIMING)


#========================================================
# High Level Functions
#========================================================
def Paradigm():
    # Define the squares (stimuli)
    stim_freqs = [2, 3, 4, 5]  # Frequencies for SSVEP stimuli in Hz
    training_sequence = [random.randint(0, 3) for _ in range(21)] # random predict (inclusive)
    stimuli = []
    key_positions = [(-.5,.5), (.5, .5), (-.5, -.5), (.5, -.5)]  # Positions for each key/square

    # Create square stimuli
    stimuli = []
    training_stimuli = []
    for i, pos in enumerate(key_positions):
        square = psychopy.visual.Rect(win, width=0.2, height=0.3, pos=pos, fillColor=[1, 1, 1], lineColor=None)
        training_square = psychopy.visual.Rect(win, width=0.2, height=0.3, pos=pos, fillColor=None, lineColor="red")
        stimuli.append(square)
        training_stimuli.append(training_square)

    # Main experiment loop
    terminate1 = False # first while loop
    terminate2 = False # second while loop
    k = 0
    while not terminate1 and k <20:
        while not terminate2 and k < 20:
            #isi
            for frame in range(MsToFrames(1000, refresh_rate)):
                for stim_index, square in enumerate(stimuli):
                    if training:
                        training_stimuli[k].draw()
                        square.draw()
                    else:
                        square.draw()
                    

                # Break if there's a keyboard event
                if len(psychopy.event.getKeys()) > 0:
                    terminate1 = True

                mrkstream_out.push_sample(pylsl.vectorstr(["0"])) # isi marker

                win.flip()

            # 1500ms flicker square stim
            for frame in range(MsToFrames(1500, refresh_rate)):
                current_time = psychopy.core.getTime()
                for stim_index, square in enumerate(stimuli):

                    mrkstream_out.push_sample(pylsl.vectorstr(["16"])) # si marker

                    if int(current_time * stim_freqs[stim_index]) % 2 == 0: #draw flickers 
                        if training:
                            training_stimuli[k].draw()
                            square.draw()
                        else:
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

        

    psychopy.event.clearEvents()
    win.close()
            
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

    # Initialize LSL marker streams
    mrkstream_out = lsl_mrk_outlet('Task_Markers') # important this is first
    results_in = lsl_inlet('Result_Stream')

    # Wait a second for the streams to settle down
    time.sleep(1)
    
    # Run through paradigm
    Paradigm()