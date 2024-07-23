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

gamepadType = Gamepad.Xbox360
pollInterval = 0.05

global running
running = True
vertical = 0.0
horizontal = 0.0
lt = 0.0
rt = 0.0
# mouse cursor speed
speed = 10

dict = {}
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

def changeLayer():
    layerList = []
    currentIndex = 0
    filePath = os.path.realpath(__file__)
    dirPath = os.path.dirname(os.path.abspath(sys.argv[2]))
    argPath = os.path.abspath(sys.argv[2])
    for layer in sorted(os.listdir(dirPath)):
        if layer.endswith(".yml"):
            fPathLayer = dirPath + "/" + layer
            layerList.append(fPathLayer)
    for i in range(len(layerList)):
        if layerList[i] == argPath:
            currentIndex = i
    lastIndex = len(layerList) - 1
    if lastIndex > currentIndex:
        nextIndex = currentIndex + 1
    else:
        nextIndex = 0
    command = dirPath + "/change-layer.sh " + filePath + " --config " + layerList[nextIndex]
    print(command + "\n")
    subprocess.call('{0}'.format(command), shell=True)

def showLayer():
    layerList = []
    currentIndex = 0
    dirPath = os.path.dirname(os.path.abspath(sys.argv[2]))
    argPath = os.path.abspath(sys.argv[2])
    for layer in sorted(os.listdir(dirPath)):
        if layer.endswith(".yml"):
            fPathLayer = dirPath + "/" + layer
            layerList.append(fPathLayer)
    for i in range(len(layerList)):
        if layerList[i] == argPath:
            currentIndex = i
    h1 = "\"" + "==LAYER" + str(currentIndex) + "==" + "\n\n"
    h2 = "FUNCTIONS" + "\n"
    h3 = "AXIS" + "\n"
    h4 = "BUTTONS" + "\n"
    b0 = buttonBACK + ": " + dict.get(buttonBACK) + "\n"
    b1 = buttonSTART + ": " + dict.get(buttonSTART) + "\n\n"
    b6 = buttonLT + ": " + dict.get(buttonLT) + "\n"
    b7 = buttonRT + ": " + dict.get(buttonRT) + "\n\n"
    b10 = buttonX + ": " + dict.get(buttonX) + "\n"
    b11 = buttonY + ": " + dict.get(buttonY) + "\n"
    b12 = buttonB + ": " + dict.get(buttonB) + "\n"
    b13 = buttonA + ": " + dict.get(buttonA) + "\""
    if dict.get(buttonLEFT) == "None":
        b2 = buttonLEFT + ": mouse move left" + "\n"
        b4 = buttonRIGHT + ": mouse move right" + "\n"
    elif dict.get(buttonLEFT) == "left":
        b2 = buttonLEFT + ": left" + "\n"
        b4 = buttonRIGHT + ": right" + "\n"
    else:
        b2 = buttonLEFT + ": " + dict.get(buttonLEFT) + "\n"
        b4 = buttonRIGHT + ": " + dict.get(buttonRIGHT) + "\n"
    if dict.get(buttonDOWN) == "None":
        b3 = buttonDOWN + ": mouse move down" + "\n"
        b5 = buttonUP + ": mouse move up" + "\n"
    elif dict.get(buttonDOWN) == "down":
        b3 = buttonDOWN + ": down" + "\n"
        b5 = buttonUP + ": up" + "\n"
    else:
        b3 = buttonDOWN + ": " + dict.get(buttonDOWN) + "\n"
        b5 = buttonUP + ": " + dict.get(buttonUP) + "\n"
    if dict.get(buttonLB) == "None":
        b8 = buttonLB + ": mouse left click" + "\n"
    elif dict.get(buttonLB) == "LDclick":
        b8 = buttonLB + ": mouse double left-click" + "\n"
    else:
        b8 = buttonLB + ": " + dict.get(buttonLB) + "\n"
    if dict.get(buttonRB) == "None":
        b9 = buttonRB + ": mouse right click" + "\n"
    else:
        b9 = buttonRB + ": " + dict.get(buttonRB) + "\n"
    buttonList = h1 + h2 + b0 + b1 + h3 + b2 + b3 + b4 + b5 + b6 + b7 + h4 + b8 + b9 + b10 + b11 + b12 + b13
    command = dirPath + "/show-layer.sh " + buttonList
    print(command + "\n")
    subprocess.call('{0}'.format(command), shell=True)

def updateDict():
    global dict
    configPath = sys.argv[2]
    with open(configPath, 'r') as file:
        config = yaml.safe_load(file)
    # FUNCTIONS BUTTONS
    if config['FUNCTIONS'][buttonBACK] == "":
        dict[buttonBACK] = "None"
    else:
        dict[buttonBACK] = config['FUNCTIONS'][buttonBACK]
    if config['FUNCTIONS'][buttonSTART] == "":
        dict[buttonSTART] = "None"
    else:
        dict[buttonSTART] = config['FUNCTIONS'][buttonSTART]
    # AXIS BUTTONS
    if config['AXIS'][buttonLEFT] == "":
        dict[buttonLEFT] = "None"
        dict[buttonRIGHT] = "None"
    else:
        dict[buttonLEFT] = config['AXIS'][buttonLEFT]
        if dict[buttonLEFT] == "left":
            dict[buttonRIGHT] = "right"
        else:
            dict[buttonRIGHT] = config['AXIS'][buttonRIGHT]
    if config['AXIS'][buttonDOWN] == "":
        dict[buttonDOWN] = "None"
        dict[buttonUP] = "None"
    else:
        dict[buttonDOWN] = config['AXIS'][buttonDOWN]
        if dict[buttonDOWN] == "down":
            dict[buttonUP] = "up"
        else:
            dict[buttonUP] = config['AXIS'][buttonUP]
    if config['AXIS'][buttonLT] == "":
        dict[buttonLT] = "None"
    else:
        dict[buttonLT] = config['AXIS'][buttonLT]
    if config['AXIS'][buttonRT] == "":
        dict[buttonRT] = "None"
    else:
        dict[buttonRT] = config['AXIS'][buttonRT]
    # BUTTONS
    if config['BUTTONS'][buttonLB] == "":
        dict[buttonLB] = "None"
    else:
        dict[buttonLB] = config['BUTTONS'][buttonLB]
    if config['BUTTONS'][buttonRB] == "":
        dict[buttonRB] = "None"
    else:
        dict[buttonRB] = config['BUTTONS'][buttonRB]
    if config['BUTTONS'][buttonX] == "":
        dict[buttonX] = "None"
    else:
        dict[buttonX] = config['BUTTONS'][buttonX]
    if config['BUTTONS'][buttonY] == "":
        dict[buttonY] = "None"
    else:
        dict[buttonY] = config['BUTTONS'][buttonY]
    if config['BUTTONS'][buttonB] == "":
        dict[buttonB] = "None"
    else:
        dict[buttonB] = config['BUTTONS'][buttonB]
    if config['BUTTONS'][buttonA] == "":
        dict[buttonA] = "None"
    else:
        dict[buttonA] = config['BUTTONS'][buttonA]
    print(dict)

def pressedLB():
    b = dict.get(buttonLB)
    if b == "None":
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
    if b == "None":
        print('LB Released')
        pyautogui.mouseUp()
    elif b == "LDclick":
        print('LB Double-click Done')
    else:
        print('LB Released')
        pyautogui.keyUp(b)

def pressedRB():
    b = dict.get(buttonRB)
    if b == "None":
        print('RB Pressed')
        pyautogui.mouseDown(button = 'right')
    else:
        print('RB Pressed')
        pyautogui.keyDown(b)

def releasedRB():
    b = dict.get(buttonRB)
    if b == "None":
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
    if b != "None":
        print('X Pressed')
        pyautogui.keyDown(b)

def releasedX():
    b = dict.get(buttonX)
    if b != "None":
        print('X Released')
        pyautogui.keyUp(b)

def pressedY():
    b = dict.get(buttonY)
    if b != "None":
        print('Y Pressed')
        pyautogui.keyDown(b)

def releasedY():
    b = dict.get(buttonY)
    if b != "None":
        print('Y Released')
        pyautogui.keyUp(b)

def pressedB():
    b = dict.get(buttonB)
    if b != "None":
        print('B Pressed')
        pyautogui.keyDown(b)

def releasedB():
    b = dict.get(buttonB)
    if b != "None":
        print('B Released')
        pyautogui.keyUp(b)

def pressedA():
    b = dict.get(buttonA)
    if b != "None":
        print('A Pressed')
        pyautogui.keyDown(b)

def releasedA():
    b = dict.get(buttonA)
    if b != "None":
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
            if b == "None":
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
            if b == "None":
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
            if b != "None":
                lt = gamepad.axis(buttonLT)
                if lt == 1.0:
                    pyautogui.keyDown(b)
                elif lt == -1.0:
                    pyautogui.keyUp(b)
            b = dict.get(buttonRT)
            if b != "None":
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
