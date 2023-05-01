from microbit import *
from my_baseline_heuristic import Bot

numberOfGameTurns = 50 # Total game turns (the goal is to get to half of that, must be even number).
maxTime = 10
timePerTurn = 3

userScore = 0
machineScore = 0
turnNumber = 0
timeLeft = maxTime
currentTurnTime = timePerTurn
gameStarted = False
waitForRestart = False

bot = Bot(numberOfGameTurns)

import threading
import time

def updateTime():
    global userScore, machineScore, turnNumber, timeLeft, currentTurnTime, gameStarted, waitForRestart
    while True:
        time.sleep(1)
        if gameStarted:
            timeLeft -= 1
            currentTurnTime -= 1

        if timeLeft == 0:
            machineScore += 1
            timeLeft = maxTime
            currentTurnTime = timePerTurn
            scoreUpdate()

        threading.Thread(target=updateTime).start()

def buttonPressed(button):
    global gameStarted, currentTurnTime, timeLeft, machineScore, userScore, waitForRestart
    if button == button_a:
        userAction(-1)
    elif button == button_b:
        userAction(1)

button_a.was_pressed = False
button_b.was_pressed = False

while True:
    if not gameStarted and waitForRestart:
        if button_a.is_pressed() or button_b.is_pressed():
            restartGame()
    elif gameStarted:
        if currentTurnTime == timePerTurn:
            updateGraphics()
        if button_a.was_pressed and button_b.was_pressed:
            pass
        elif button_a.was_pressed:
            userAction(-1)
        elif button_b.was_pressed:
            userAction(1)
        button_a.was_pressed = button_a.is_pressed()
        button_b.was_pressed = button_b.is_pressed()

def userAction(key):
    global timeLeft, currentTurnTime, machineScore, userScore, gameStarted, waitForRestart

    if waitForRestart:
        return

    gameStarted = True

    if currentTurnTime > 0:
        timeLeft += currentTurnTime
        if timeLeft > maxTime:
            timeLeft = maxTime

    currentTurnTime = timePerTurn

    if bot.getBotPrediction() == key:  # bot won
        machineScore += 1
    else:
        userScore += 1

    scoreUpdate()

    bot.updateUserMove(key)

def scoreUpdate():
    global userScore, machineScore, gameStarted, waitForRestart

    if userScore >= numberOfGameTurns / 2:  # game over user won
        gameStarted = False
        waitForRestart = True

    if machineScore >= numberOfGameTurns / 2:  # game over user won
        gameStarted = False
        waitForRestart = True

    updateGraphics()

def restartGame():
    global numberOfGameTurns, userScore, machineScore, turnNumber, timeLeft, currentTurnTime, gameStarted, waitForRestart, bot

    numberOfGameTurns = 50  # Total game turns (the goal is to get to half of that, must be even number).
    userScore = 0
    machineScore = 0
    turnNumber = 0
    timeLeft = maxTime
    currentTurnTime = timePerTurn
    gameStarted = False
    waitForRestart = False
    bot = Bot(numberOfGameTurns)

    updateGraphics()

def updateGraphics():
    global userScore, machineScore, gameStarted, numberOf
