#!/usr/bin/env python
# coding: utf-8

import os
import sys
import subprocess
import time
import yaml
import argparse
import pyautogui
import Gamepad

global running
gamepadType = Gamepad.Xbox360
running = True
pollInterval = 0.05
vertical = 0.0
horizontal = 0.0
lt = 0.0
rt = 0.0
# mouse cursor speed
speed = 10
layerList = []
dict = {}

# button "LEFT" = "LEFT-X", "-1.0"
# button "DOWN" = "LEFT-Y", "1.0"
# button "RIGHT" = "LEFT-X", "1.0"
# button "UP" = "LEFT-Y", "-1.0"
buttonLB = "LB"
buttonRB = "RB"
buttonLEFT = "LEFT-X"
buttonDOWN = "LEFT-Y"
buttonRIGHT = "RIGHT"
buttonUP = "UP"
buttonLT = "LT"
buttonRT = "RT"
buttonBACK = "BACK"
buttonSTART = "START"
buttonX = "X"
buttonY = "Y"
buttonB = "B"
buttonA = "A"

def killDubProcesses():
    subprocess.call('for i in $(ps aux|grep \'pjoypad.py\'|grep -v grep|awk \'{print $2}\'|head -n -1); do kill "$i"; done', shell=True)

# get the current index, path to the working directory, path to the layer file
def getCurrentParameters():
    global layerList
    currentIndex = 0
    filePath = os.path.realpath(__file__)
    dirPath = os.path.dirname(os.path.abspath(sys.argv[2]))
    argPath = os.path.abspath(sys.argv[2])
    for layer in sorted(os.listdir(dirPath)):
        if layer.endswith(".yml"):
            fPathLayer = dirPath+"/"+layer
            layerList.append(fPathLayer)
    for i in range(len(layerList)):
        if layerList[i] == argPath:
            currentIndex = i
    return [currentIndex, dirPath, filePath]

def changeLayer():
    list = getCurrentParameters()
    currentIndex, dirPath, filePath = list[0], list[1], list[2]
    lastIndex = len(layerList) - 1
    if lastIndex > currentIndex:
        nextIndex = currentIndex+1
    else:
        nextIndex = 0
    command = dirPath+"/change-layer.sh "+filePath+" --config "+layerList[nextIndex]
    print(command+"\n")
    subprocess.call('{0}'.format(command), shell=True)

def getButtonString(x):
    if x!=buttonLEFT and x!=buttonRIGHT and x!=buttonDOWN and x!=buttonUP and x!=buttonLB and x!=buttonRB:
        y = x+": "+dict.get(x)+"\n"
    elif x==buttonLEFT and dict.get(x)=="none":
        y = x+": mouse move left\n"
    elif x==buttonLEFT and dict.get(x)!="none":
        y = x+": "+dict.get(x)+"\n"
    elif x==buttonRIGHT and dict.get(x)=="none":
        y = x+": mouse move right\n"
    elif x==buttonRIGHT and dict.get(x)!="none":
        y = x+": "+dict.get(x)+"\n"
    elif x==buttonDOWN and dict.get(x)=="none":
        y = x+": mouse move down\n"
    elif x==buttonDOWN and dict.get(x)!="none":
        y = x+": "+dict.get(x)+"\n"
    elif x==buttonUP and dict.get(x)=="none":
        y = x+": mouse move up\n"
    elif x==buttonUP and dict.get(x)!="none":
        y = x+": "+dict.get(x)+"\n"
    elif x==buttonLB and dict.get(x)=="none":
        y = x+": mouse left click\n"
    elif x==buttonLB and dict.get(x)=="LDclick":
        y = x+": mouse double left-click\n"
    elif x==buttonLB and dict.get(x)!="none" and dict.get(x)!="LDclick":
        y = x+": "+dict.get(x)+"\n"
    elif x==buttonRB and dict.get(x)=="none":
        y = x+": mouse right click\n"
    elif x==buttonRB and dict.get(x)!="none":
        y = x+": "+dict.get(x)+"\n"
    return y

def showLayer():
    list = getCurrentParameters()
    currentIndex, dirPath, filePath = list[0], list[1], list[2]
    h1 = "\""+"==LAYER"+str(currentIndex)+"=="+"\n\n"
    h2 = "FUNCTIONS"+"\n"
    h3 = "AXIS"+"\n"
    h4 = "BUTTONS"+"\n"
    bs0 = getButtonString(buttonBACK)
    bs1 = getButtonString(buttonSTART)+"\n"
    bs2 = getButtonString(buttonLEFT)
    bs3 = getButtonString(buttonDOWN)
    bs4 = getButtonString(buttonRIGHT)
    bs5 = getButtonString(buttonUP)
    bs6 = getButtonString(buttonLT)
    bs7 = getButtonString(buttonRT)+"\n"
    bs8 = getButtonString(buttonLB)
    bs9 = getButtonString(buttonRB)
    bs10 = getButtonString(buttonX)
    bs11 = getButtonString(buttonY)
    bs12 = getButtonString(buttonB)
    bs13 = buttonA+": "+dict.get(buttonA)+"\""
    buttonList = h1+h2+bs0+bs1+h3+bs2+bs3+bs4+bs5+bs6+bs7+h4+bs8+bs9+bs10+bs11+bs12+bs13
    command = dirPath+"/show-layer.sh "+buttonList
    print(command+"\n")
    subprocess.call('{0}'.format(command), shell=True)

def getButton(x):
    if x is None or x=="" or x=="None":
        y = "none"
    else:
        y = x
    return y

def updateDict():
    global dict
    configPath = sys.argv[2]
    with open(configPath, 'r') as file:
        config = yaml.safe_load(file)
    dict[buttonBACK] = getButton(config['FUNCTIONS'][buttonBACK])
    dict[buttonSTART] = getButton(config['FUNCTIONS'][buttonSTART])
    dict[buttonLEFT] = getButton(config['AXIS'][buttonLEFT])
    dict[buttonDOWN] = getButton(config['AXIS'][buttonDOWN])
    dict[buttonRIGHT] = getButton(config['AXIS'][buttonRIGHT])
    dict[buttonUP] = getButton(config['AXIS'][buttonUP])
    dict[buttonLT] = getButton(config['AXIS'][buttonLT])
    dict[buttonRT] = getButton(config['AXIS'][buttonRT])
    dict[buttonLB] = getButton(config['BUTTONS'][buttonLB])
    dict[buttonRB] = getButton(config['BUTTONS'][buttonRB])
    dict[buttonX] = getButton(config['BUTTONS'][buttonX])
    dict[buttonY] = getButton(config['BUTTONS'][buttonY])
    dict[buttonB] = getButton(config['BUTTONS'][buttonB])
    dict[buttonA] = getButton(config['BUTTONS'][buttonA])
    print(dict)

def pressedLB():
    b = dict.get(buttonLB)
    if b == "none":
        print('LB Pressed')
        pyautogui.mouseDown()
    elif b == "LDclick":
        print('LB Double-click')
        pyautogui.click(clicks=2)
    else:
        print('LB Pressed')
        pyautogui.keyDown(b)

def releasedLB():
    b = dict.get(buttonLB)
    if b == "none":
        print('LB Released')
        pyautogui.mouseUp()
    elif b == "LDclick":
        print('LB Double-click Done')
    else:
        print('LB Released')
        pyautogui.keyUp(b)

def pressedRB():
    b = dict.get(buttonRB)
    if b == "none":
        print('RB Pressed')
        pyautogui.mouseDown(button = 'right')
    else:
        print('RB Pressed')
        pyautogui.keyDown(b)

def releasedRB():
    b = dict.get(buttonRB)
    if b == "none":
        print('RB Released')
        pyautogui.mouseUp(button = 'right')
    else:
        print('RB Released')
        pyautogui.keyUp(b)

def pressBACK():
    b = dict.get(buttonBACK)
    if b == "changeLayer()":
        changeLayer()

def pressSTART():
    b = dict.get(buttonSTART)
    if b == "showLayer()":
        showLayer()

def pressedX():
    b = dict.get(buttonX)
    if b != "none":
        print('X Pressed')
        pyautogui.keyDown(b)

def releasedX():
    b = dict.get(buttonX)
    if b != "none":
        print('X Released')
        pyautogui.keyUp(b)

def pressedY():
    b = dict.get(buttonY)
    if b != "none":
        print('Y Pressed')
        pyautogui.keyDown(b)

def releasedY():
    b = dict.get(buttonY)
    if b != "none":
        print('Y Released')
        pyautogui.keyUp(b)

def pressedB():
    b = dict.get(buttonB)
    if b != "none":
        print('B Pressed')
        pyautogui.keyDown(b)

def releasedB():
    b = dict.get(buttonB)
    if b != "none":
        print('B Released')
        pyautogui.keyUp(b)

def pressedA():
    b = dict.get(buttonA)
    if b != "none":
        print('A Pressed')
        pyautogui.keyDown(b)

def releasedA():
    b = dict.get(buttonA)
    if b != "none":
        print('A Released')
        pyautogui.keyUp(b)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type = argparse.FileType('r', encoding = 'UTF-8'), required = True, help = "path to the configuration file")
    args = parser.parse_args()
    args.config.close()

    if not Gamepad.available():
        print('Please connect your gamepad...')
        while not Gamepad.available():
            time.sleep(1.0)
    gamepad = gamepadType()
    print('Gamepad connected')

    killDubProcesses()
    updateDict()
    showLayer()
    gamepad.startBackgroundUpdates()

    gamepad.addButtonPressedHandler(buttonLB, pressedLB)
    gamepad.addButtonReleasedHandler(buttonLB, releasedLB)
    gamepad.addButtonPressedHandler(buttonRB, pressedRB)
    gamepad.addButtonReleasedHandler(buttonRB, releasedRB)
    gamepad.addButtonReleasedHandler(buttonBACK, pressBACK)
    gamepad.addButtonReleasedHandler(buttonSTART, pressSTART)
    gamepad.addButtonReleasedHandler(buttonX, pressedX)
    gamepad.addButtonReleasedHandler(buttonX, releasedX)
    gamepad.addButtonReleasedHandler(buttonY, pressedY)
    gamepad.addButtonReleasedHandler(buttonY, releasedY)
    gamepad.addButtonReleasedHandler(buttonB, pressedB)
    gamepad.addButtonReleasedHandler(buttonB, releasedB)
    gamepad.addButtonReleasedHandler(buttonA, pressedA)
    gamepad.addButtonReleasedHandler(buttonA, releasedA)

    try:
        while running and gamepad.isConnected():
            b = dict.get(buttonDOWN)
            vertical = -gamepad.axis(buttonDOWN)
            if b == "none":
                if vertical == -1.0:
                    pyautogui.move(0, speed)
                elif vertical == 1.0:
                    pyautogui.move(0, -speed)
            elif b == "down":
                if vertical == -1.0:
                    pyautogui.press(b)
                elif vertical == 1.0:
                    pyautogui.press('up')
            else:
                if vertical == -1.0:
                    pyautogui.press(b)
                elif vertical == 1.0:
                    pyautogui.press(dict.get(buttonUP))
            b = dict.get(buttonLEFT)
            horizontal = gamepad.axis(buttonLEFT)
            if b == "none":
                if horizontal == -1.0:
                    pyautogui.move(-speed, 0)
                elif horizontal == 1.0:
                    pyautogui.move(speed, 0)
            elif b == "left":
                if horizontal == -1.0:
                    pyautogui.press(b)
                elif horizontal == 1.0:
                    pyautogui.press('right')
            else:
                if horizontal == -1.0:
                    pyautogui.press(b)
                elif horizontal == 1.0:
                    pyautogui.press(dict.get(buttonRIGHT))
            b = dict.get(buttonLT)
            if b != "none":
                lt = gamepad.axis(buttonLT)
                if lt == 1.0:
                    pyautogui.keyDown(b)
                elif lt == -1.0:
                    pyautogui.keyUp(b)
            b = dict.get(buttonRT)
            if b != "none":
                rt = gamepad.axis(buttonRT)
                if rt == 1.0:
                    pyautogui.keyDown(b)
                elif rt == -1.0:
                    pyautogui.keyUp(b)
            time.sleep(pollInterval)
    finally:
        gamepad.disconnect()

if __name__ == "__main__":
    main()
