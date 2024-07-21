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
    command = dirPath + "/" + "change-layer.sh " + filePath + " --config " + layerList[nextIndex]
    print(command + "\n")
    subprocess.call('{0}'.format(command), shell=True)

def updateDict():
    global dict
    configpath = sys.argv[2]
    with open(configpath, 'r') as file:
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

def LB_Pressed():
    b = dict.get(buttonLB)
    if b == "None":
        print('LB Pressed')
        pyautogui.mouseDown()
    else:
        print('LB Pressed')
        pyautogui.keyDown(b)

def LB_Released():
    b = dict.get(buttonLB)
    if b == "None":
        print('LB Released')
        pyautogui.mouseUp()
    else:
        print('LB Released')
        pyautogui.keyUp(b)

def RB_Pressed():
    b = dict.get(buttonRB)
    if b == "None":
        print('RB Pressed')
        pyautogui.mouseDown(button = 'right')
    else:
        print('RB Pressed')
        pyautogui.keyDown(b)

def RB_Released():
    b = dict.get(buttonRB)
    if b == "None":
        print('RB Released')
        pyautogui.mouseUp(button = 'right')
    else:
        print('RB Released')
        pyautogui.keyUp(b)

def BACK_Press():
    b = dict.get(buttonBACK)
    if b == "None":
        changeLayer()

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

    gamepad.addButtonPressedHandler(buttonLB, LB_Pressed)
    gamepad.addButtonReleasedHandler(buttonLB, LB_Released)
    gamepad.addButtonPressedHandler(buttonRB, RB_Pressed)
    gamepad.addButtonReleasedHandler(buttonRB, RB_Released)
    gamepad.addButtonReleasedHandler(buttonBACK, BACK_Press)

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
