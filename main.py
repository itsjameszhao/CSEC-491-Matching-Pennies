import keyboard
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

def keyDownHandler(e):
global gameStarted, currentTurnTime, timeLeft, machineScore, userScore, waitForRestart
if e.name == "right": # Right key
userAction(1)
elif e.name == "left": # Left key
userAction(-1)

keyboard.on_press_key("right", keyDownHandler)
keyboard.on_press_key("left", keyDownHandler)

restartGame()

def userAction(key):
global timeLeft, currentTurnTime, machineScore, userScore, gameStarted, waitForRestart

yaml
Copy code
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

yaml
Copy code
if userScore >= numberOfGameTurns / 2:  # game over user won
    gameStarted = False
    waitForRestart = 1

if machineScore >= numberOfGameTurns / 2:  # game over user won
    gameStarted = False
    waitForRestart = 2

updateGraphics()
def restartGame():
global numberOfGameTurns, userScore, machineScore, turnNumber, timeLeft, currentTurnTime, gameStarted, waitForRestart, bot

makefile
Copy code
numberOfGameTurns = 50  # Total game turns (the goal is to get to half of that, must be even number).
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
updateGraphics()
def updateGraphics():
global userScore, machineScore, gameStarted, numberOfGameTurns, waitForRestart

lua
Copy code
print("User: {0}  Machine: {1}".format(userScore, machineScore))

if not gameStarted and waitForRestart: