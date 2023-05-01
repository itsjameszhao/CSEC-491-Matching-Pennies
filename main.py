import time
from pynput import keyboard
from my_baseline_heuristic import BaselineBot
from my_bush_mosteller import BushMostellerBot

numberOfGameTurns = 80 # Total game turns (the goal is to get to half of that, must be even number).
maxTime = 10
timePerTurn = 3

userScore = 0
machineScore = 0
turnNumber = 0
timeLeft = maxTime
currentTurnTime = timePerTurn
gameStarted = False
waitForRestart = False

# Bot = BaselineBot
Bot = BushMostellerBot
bot = Bot(numberOfGameTurns)

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
    bot.updateBotPrediction()

def keyDownHandler(key):
    global gameStarted, currentTurnTime, timeLeft, machineScore, userScore, waitForRestart
    if key == keyboard.Key.right: # Right key
        userAction(1)
    elif key == keyboard.Key.left: # Left key
        userAction(-1)

def scoreUpdate():
    global userScore, machineScore, gameStarted, waitForRestart

    if userScore >= numberOfGameTurns / 2:  # game over user won
        gameStarted = False
        waitForRestart = 1

    if machineScore >= numberOfGameTurns / 2:  # game over user won
        gameStarted = False
        waitForRestart = 2

    updateGraphics()

def restartGame():
    global numberOfGameTurns, userScore, machineScore, turnNumber, timeLeft, currentTurnTime, gameStarted, waitForRestart, bot

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
    del bot
    bot = Bot(numberOfGameTurns)
    updateGraphics()

def updateGraphics():
    global userScore, machineScore, gameStarted, numberOfGameTurns, waitForRestart, bot

    print("User: {0}  Machine: {1}".format(userScore, machineScore))

    if not gameStarted and waitForRestart:
        print("Game over. Press any key to restart...")
        waitForRestart = False

        # Wait for any key press to restart the game
        with keyboard.Listener(on_press=lambda x: restartGame()) as listener:
            listener.join()


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

with keyboard.Listener(on_press=keyDownHandler) as listener:
    listener.join()

updateTime()
