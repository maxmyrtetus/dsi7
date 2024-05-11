##This is a file just for testing out the GUI part of the experimental task

from psychopy import visual, event, core
import random
import numpy as np

# Define constants
win = visual.Window([800, 600], monitor="testMonitor", units="pix")
num_flashes = 10
flash_duration = 0.1
inter_flash_interval = 0.2

def p300_collection():# Create a white circle in the middle of the screen
    central_circle = visual.Circle(win, radius=30, fillColor='black', lineColor=None)

    # Create four circles around the central circle
    positions = np.array([[0, 150], [150, 0], [0, -150], [-150, 0]])
    outer_circles = [visual.Circle(win, radius=30, pos=pos, fillColor=None, lineColor='white') for pos in positions]

    # Draw the central circle
    central_circle.draw()
    win.flip()

    flash_ind = 0 #initialize index for circle that flashes
    # Run the P300 Speller task
    while(True):
        # Draw the outer circles
        if flash_ind >=4:
            flash_ind = 0
        if('escape' in event.getKeys()):
                win.close()
        
        outer_circles[flash_ind].fillColor = 'white'
        for circle in outer_circles:
            circle.draw()
        

        win.flip()
        central_circle.draw()
        core.wait(inter_flash_interval)
        outer_circles[flash_ind].fillColor = None
        flash_ind += 1

    # Close the window
    win.close()

p300_collection()