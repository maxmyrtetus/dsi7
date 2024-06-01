from psychopy import visual, core
from psychopy.hardware import keyboard
import numpy as np
from scipy import signal
import screeninfo

# keyboard_classes = [(8, 0),
#                     (9, 0), 
#                     (10, 0), 
#                     (11, 0), 
#                     (12, 0), 
#                     (13, 0), 
#                     (14, 0), 
#                     (15, 0), ]

keyboard_classes = [(8, 0), (10, 0), (12, 0), (14, 0),]

monitor_info = screeninfo.get_monitors()[0] #gets info about you monitor (height, width, etc.)
width = monitor_info.width # Width of your monitor in pixels
height = monitor_info.height  # Height of your monitor in pixels

stim_duration = 5  # in seconds
n_keyboard_classes = len(keyboard_classes)
classes = keyboard_classes
refresh_rate = 60.02  # refresh rate of the monitor
use_retina = False  # whether the monitor is a retina display

                    
# █████████████████████████████████████████████████████████████████████████████

def ms_to_frame(ms, fs):
    dt = 1000 / fs
    return np.round(ms / dt).astype(int)

def create_8_keys(size=120, colors=[-1, -1, -1] * 8):
    positions = []
    positions.extend([[-width / 2 + 100, height / 2 - 90 - i * 200 - 300] for i in range(1)])
    positions.extend([[-width / 2 + 190 * 1 + 100, height / 2 - 90 - i * 200 - 300] for i in range(1)])
    positions.extend([[-width / 2 + 190 * 2 + 100, height / 2 - 90 - i * 200 - 300] for i in range(1)])
    positions.extend([[-width / 2 + 190 * 3 + 100, height / 2 - 90 - i * 200 - 300] for i in range(1)])
    positions.extend([[-width / 2 + 190 * 4 + 100, height / 2 - 90 - i * 200 - 300] for i in range(1)])
    positions.extend([[-width / 2 + 190 * 5 + 100, height / 2 - 90 - i * 200 - 300] for i in range(1)])
    positions.extend([[-width / 2 + 190 * 6 + 100, height / 2 - 90 - i * 200 - 300] for i in range(1)])
    positions.extend([[-width / 2 + 190 * 7 + 100, height / 2 - 90 - i * 200 - 300] for i in range(1)])
    # positions.extend([[width / 2 - 40, height / 2 - 40]])
    keys = visual.ElementArrayStim(win, nElements=8, elementTex=None, elementMask=None, units='pix',
                                   sizes=[size, size], xys=positions, colors=colors)
    return keys

def create_4_keys(size=120, colors=[-1, -1, -1] * 4):
    #positions = []
    #positions.extend([[-width / 2 + 190 * 3 + 150, height / 2 - 90 - i * 200 - 80] for i in range(4)])
    key_positions = [(0, height/2 - 50), (width/2 - 50, 0), (0, -height/2 + 50), (-width/2 + 50, 0)]
    keys = visual.ElementArrayStim(win, nElements=4, elementTex=None, elementMask=None, units='pix',
                                   sizes=[size, size], xys=key_positions, colors=colors)
    return keys

# █████████████████████████████████████████████████████████████████████████████

if __name__ == "__main__":
    kb = keyboard.Keyboard()
    win = visual.Window(
        size=[width, height],
        checkTiming=True,
        allowGUI=False,
        fullscr=True,
        useRetina=use_retina
    )
    flickering_keyboard = create_4_keys()
    stim_duration_frames = ms_to_frame((stim_duration) * 1000,
                                       refresh_rate)  # total number of frames for the stimulation
    frame_indices = np.arange(stim_duration_frames)  # the frames as integer indices
    flickering_frames = np.zeros((len(frame_indices), n_keyboard_classes))
    for i_class, (flickering_freq, phase_offset) in enumerate(keyboard_classes):
        phase_offset += .00001  # nudge phase slightly from points of sudden jumps for offsets that are pi multiples
        flickering_frames[:, i_class] = signal.square(2 * np.pi * flickering_freq * (
                    frame_indices / refresh_rate) + phase_offset * np.pi)  # frequency approximation formula
    while True:
        keys = kb.getKeys()
        for thisKey in keys:
            if thisKey == 'escape':
                core.quit()
        for i_frame, frame in enumerate(flickering_frames):
            next_flip = win.getFutureFlipTime()
            flickering_keyboard.colors = np.array([frame] * 3).T
            flickering_keyboard.draw()
            win.flip()