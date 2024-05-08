import pyautogui


for i in range(4):

    #left
    if i == 0:
        pyautogui.moveRel(-300, 0)
    #up
    if i == 1:
        pyautogui.moveRel(0, -300)
    #right
    if i == 2:
        pyautogui.moveRel(300, 0)
    #down
    if i == 3:
        pyautogui.moveRel(0, 300)
    
    