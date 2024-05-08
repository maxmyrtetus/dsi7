from psychopy import visual, event, core
import random
import numpy as np

# Define constants
win = visual.Window([800, 600], monitor="testMonitor", units="pix")
num_flashes = 10
flash_duration = 0.1
inter_flash_interval = 0.2

# Create a white circle in the middle of the screen
central_circle = visual.Circle(win, radius=30, fillColor='black', lineColor=None)

# Create four circles around the central circle
positions = np.array([[0, 150], [150, 0], [0, -150], [-150, 0]])
outer_circles = [visual.Circle(win, radius=30, pos=pos, fillColor='white', lineColor=None) for pos in positions]

# Draw the central circle
central_circle.draw()
win.flip()

# Run the P300 Speller task
while(True):
    # Draw the outer circles
    for circle in outer_circles:
        if('escape' in event.getKeys()):
            win.close()
        circle.draw()
    
    win.flip()
    central_circle.draw()
    core.wait(flash_duration)
    win.flip()
    central_circle.draw()
    core.wait(inter_flash_interval)


# Close the window
win.close()
