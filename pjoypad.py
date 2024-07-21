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
pollInterval = 0.1

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
buttonRIGHT = ""
buttonUP = ""
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
    for layer in os.listdir(dirPath):
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
    for layer in os.listdir(dirPath):
        if layer.endswith(".yml"):
            fPathLayer = dirPath + "/" + layer
            layerList.append(fPathLayer)
    for i in range(len(layerList)):
        if layerList[i] == argPath:
            currentIndex = i
    b0 = "==LAYER" + str(currentIndex) + "=="
    b1 = dict.get(buttonLB)
    b2 = dict.get(buttonRB)
    b3 = dict.get(buttonLEFT)
    b4 = dict.get(buttonDOWN)
    b5 = dict.get(buttonLT)
    b6 = dict.get(buttonRT)
    b7 = dict.get(buttonBACK)
    b8 = dict.get(buttonSTART)
    b9 = dict.get(buttonX)
    b10 = dict.get(buttonY)
    b11 = dict.get(buttonB)
    b12 = dict.get(buttonA)
    buttonList = "\"" \
            + b0 + "\n" \
            + buttonLB + ": " + b1 + "\n" \
            + buttonRB + ": " + b2 + "\n" \
            + buttonLEFT + ": " + b3 + "\n" \
            + buttonDOWN + ": " + b4 + "\n" \
            + buttonLT + ": " + b5 + "\n" \
            + buttonRT + ": " + b6 + "\n" \
            + buttonBACK + ": " + b7 + "\n" \
            + buttonSTART + ": " + b8 + "\n" \
            + buttonX + ": " + b9 + "\n" \
            + buttonY + ": " + b10 + "\n" \
            + buttonB + ": " + b11 + "\n" \
            + buttonA + ": " + b12 + "\""
    command = dirPath + "/show-layer.sh " + buttonList
    print(command + "\n")
    subprocess.call('{0}'.format(command), shell=True)

def updateDict():
    global dict
    configPath = sys.argv[2]
    with open(configPath, 'r') as file:
        config = yaml.safe_load(file)
    if config[buttonLB] is None:
        dict[buttonLB] = "None"
    else:
        dict[buttonLB] = config[buttonLB]
    if config[buttonRB] is None:
        dict[buttonRB] = "None"
    else:
        dict[buttonRB] = config[buttonRB]
    if config[buttonLEFT] is None:
        dict[buttonLEFT] = "None"
    else:
        dict[buttonLEFT] = config[buttonLEFT]
    if config[buttonDOWN] is None:
        dict[buttonDOWN] = "None"
    else:
        dict[buttonDOWN] = config[buttonDOWN]
    #if config[buttonRIGHT] is None:
    #    dict[buttonRIGHT] = "None"
    #else:
    #    dict[buttonRIGHT] = config[buttonRIGHT]
    #if config[buttonUP] is None:
    #    dict[buttonUP] = "None"
    #else:
    #    dict[buttonUP] = config[buttonUP]
    if config[buttonLT] is None:
        dict[buttonLT] = "None"
    else:
        dict[buttonLT] = config[buttonLT]
    if config[buttonRT] is None:
        dict[buttonRT] = "None"
    else:
        dict[buttonRT] = config[buttonRT]
    if config[buttonBACK] is None:
        dict[buttonBACK] = "None"
    else:
        dict[buttonBACK] = config[buttonBACK]
    if config[buttonSTART] is None:
        dict[buttonSTART] = "None"
    else:
        dict[buttonSTART] = config[buttonSTART]
    if config[buttonX] is None:
        dict[buttonX] = "None"
    else:
        dict[buttonX] = config[buttonX]
    if config[buttonY] is None:
        dict[buttonY] = "None"
    else:
        dict[buttonY] = config[buttonY]
    if config[buttonB] is None:
        dict[buttonB] = "None"
    else:
        dict[buttonB] = config[buttonB]
    if config[buttonA] is None:
        dict[buttonA] = "None"
    else:
        dict[buttonA] = config[buttonA]
    print(dict)

def pressedLB():
    b = dict.get(buttonLB)
    if b == "None":
        print('LB Pressed')
        pyautogui.mouseDown()
    else:
        print('LB Pressed')
        pyautogui.keyDown(b)

def releasedLB():
    b = dict.get(buttonLB)
    if b == "None":
        print('LB Released')
        pyautogui.mouseUp()
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
    if b == "None":
        changeLayer()

def pressSTART():
    b = dict.get(buttonSTART)
    if b == "None":
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
            vertical = -gamepad.axis(buttonDOWN)
            if vertical == -1.0:
                pyautogui.move(0, speed)
            elif vertical == 1.0:
                pyautogui.move(0, -speed)
            horizontal = gamepad.axis(buttonLEFT)
            if horizontal == -1.0:
                pyautogui.move(-speed, 0)
            elif horizontal == 1.0:
                pyautogui.move(speed, 0)
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
