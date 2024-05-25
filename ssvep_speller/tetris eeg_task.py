"""
written by
    Gunwoo Kim
    Aric Shen
"""
import pylsl
import random
import numpy as np
from psychopy import visual, core, constants, event, prefs, sound

WINDOW = None
CLOCK = core.Clock()
MARKER_OUTLET = None

"""
Pushes a given event onto the marker stream. MARKER_OUTLET must be set up.
"""
def CreateMarker(event):
        # marker_id = utils.get_marker_number(event)
        MARKER_OUTLET.push_sample(pylsl.vectorstr([event])); # gives dsi marker event

"""
Create a randomized sequence of tasks. There will be `n` of each task.
"""
def CreateSequence(n):
    
    selections = ['TOP_LEFT','TOP_RIGHT', 'BOTTOM_LEFT','BOTTOM_RIGHT'] 
    seq = selections*n
    
    # randomize order of sequence
    random.seed()
    random.shuffle(seq)

    return seq

def RunParadigm():

    # SET UP STIMULI
    vidStims = {"LEFT_ARM" : visual.MovieStim(WINDOW, filename='./resources/left-arm.mp4', 
                                       pos=(0, 0), 
                                       size=[224,400],
                                       autoStart=False),
                "RIGHT_ARM" : visual.MovieStim(WINDOW, filename='./resources/right-arm.mp4', 
                                       pos=(0, 0), 
                                       size=[224,400],
                                       autoStart=False),
                "LEFT_LEG" : visual.MovieStim(WINDOW, filename='./resources/left-leg.mp4', 
                                       pos=(0, 0), 
                                       size=[224,400],
                                       autoStart=False),
                "RIGHT_LEG" : visual.MovieStim(WINDOW, filename='./resources/right-leg.mp4', 
                                       pos=(0, 0), 
                                       size=[224,400],
                                       autoStart=False),
    }
    taskStim = visual.TextStim(WINDOW, text='', 
                                       units='norm', 
                                       alignText='center', 
                                       color="white")
    messageStim = visual.TextStim(WINDOW, text='', 
                                       units='norm', 
                                       alignText='center', 
                                       color="black")
    fixation = visual.ShapeStim(WINDOW, vertices=((0, -10), (0, 10), (0,0), (-10, 0), (10, 0)), 
                                        lineWidth=1,  
                                        closeShape=False,  
                                        lineColor="black",
                                        fillColor="black")
    beep = sound.Sound('./resources/beep.wav')
    
    # PARADIGM
    totalChunk = 6 
    taskPerChunk = 5
    for chunk in range(totalChunk):

        sequence = CreateSequence(taskPerChunk)

        for task in sequence:
            # task = LEFT_ARM, RIGHT_ARM, LEFT_LEG, RIGHT_LEG

            # FIXATION
            CreateMarker(task) 
            fixation.draw()
            WINDOW.flip()
            core.wait(2)

            # CUE
            beep.play()
            CreateMarker("CUE")
            core.wait(random.uniform(0.5, 0.8))

            # TASK WITH VIDEO
            taskStim.text = task.replace("_", " ")
            
            vidStim = vidStims[task]
            vidStim.seek(0)
            vidStim.play()
            vidStim.draw()
            CLOCK.reset()
            while CLOCK.getTime() < 2: # stimulus length
                vidStim.draw()
                taskStim.draw()
                WINDOW.flip()
            vidStim.pause()
            vidStim.seek(0)

            # REST
            CreateMarker("MI_START")
            
            WINDOW.flip()
            core.wait(3)
            CreateMarker(f'{task}_END')

            core.wait(random.uniform(0.5,0.85))

        if chunk == totalChunk-1: # on last iteration, exit.
            break

        # LONG BREAK
        messageStim.text = f'You can rest, press SPACE to do next chunk. (progress: {chunk+1}/{totalChunk})'
        messageStim.draw()
        WINDOW.flip()
        event.waitKeys(keyList=['space']) 
    
    # FINISHED
    messageStim.text = "Task completed. Press ANY KEY to exit."
    messageStim.draw()
    WINDOW.flip()
    event.waitKeys(keyList=None) 

########################################################### MAIN
if __name__ == "__main__":
    
    WINDOW = visual.Window(
        screen=0,
        size=[600, 400],
        units="pix",
        fullscr=False,
        color="white",
        gammaErrorPolicy="ignore"
    )

    # create marker stream
    info = pylsl.stream_info('EEG_Markers', 'Markers', 1, 0, pylsl.cf_string, 'unsampledStream');
    MARKER_OUTLET = pylsl.stream_outlet(info, 1, 1)
    
    # warning message for LabRecorder
    warning_msg = visual.TextStim(WINDOW, text='Make sure that LabRecorder is connected with EEG_Markers. \n \
                                                Trial will begin automatically when you start recording in LabRecorder.',
                                          units='norm', alignText='center', color=[1,0,0], bold=True);
    warning_msg.draw()
    WINDOW.flip()

    # wait for markerstream to be used by LabRecorder
    while not MARKER_OUTLET.have_consumers():
        core.wait(0.2)

    # RUN SEQEUENCE OF TRIALS
    RunParadigm()

    # cleanup
    WINDOW.close()
    core.quit()

########################################################### END OF MAIN