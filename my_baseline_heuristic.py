import random
import math

USERWIN = -1
BOTWIN = 1
REGULAR_DATA_SERIES = 1
FLIPPING_DATA_SERIES = 2
USER_REACTIVE = 3
BOT_REACTIVE = 4
USER_REACTIVE_REG_DATA = 5


class Bot:
    """
    This class represents a bot that can play a game. The bot has a number of predictors that it can use to make predictions about the next move of the opponent.

    Attributes:
    numberOfGameTurns: The number of game turns that have been played.
    userMoves: A list of the user's moves.
    userMovesFlipping: A list of the user's moves in the flipping case (if current=last then 1 else -1).
    botMoves: A list of the bot's moves.
    wins: A list of who won each game turn.
    gameTurn: The current game turn.
    predictors: A list of predictors.
    """

    def __init__(self, numberOfGameTurns):
        """
        Initialize the bot.

        Args:
        numberOfGameTurns: The number of game turns that have been played.
        """
        self.resetBot(numberOfGameTurns)

    def resetBot(self, numberOfGameTurns):
        """
        Reset the bot.

        Args:
        numberOfGameTurns: The number of game turns that have been played.
        """
        self.numberOfGameTurns = numberOfGameTurns
        self.userMoves = []
        self.userMovesFlipping = []
        self.botMoves = []
        self.wins = []
        self.gameTurn = 0
        self.initPredictors()
        self.updateBotPrediction()

    def updateUserMove(self, userMove):
        """
        Update the user's move.

        Args:
        userMove: The user's move.
        """
        self.userMoves.append(userMove)

        if len(self.userMoves) > 1:
            if self.userMoves[self.gameTurn] == self.userMoves[self.gameTurn - 1]:
                self.userMovesFlipping.append(-1)
            else:
                self.userMovesFlipping.append(1)

        self.wins.append(BOTWIN if userMove == self.getBotPrediction() else USERWIN)

        self.gameTurn += 1
        self.updateBotPrediction()

    def getBotPrediction(self):
        """
        Get the bot's prediction for the next move.

        Returns:
        The bot's prediction.
        """
        return self.botMoves[self.gameTurn]

    def updateBotPrediction(self):
        """
        Update the bot's prediction for the next move.
        """
        botPredictionProb = self.aggregateExperts()

        sample = random.random() * 2 - 1
        if botPredictionProb < sample:
            botPrediction = -1
        else:
            botPrediction = 1

        self.botMoves[self.gameTurn] = botPrediction

    def aggregateExperts(self):
        """
        Aggregate the predictions of the experts.

        Returns:
        The aggregate prediction.
        """
        eta = math.sqrt(
            math.log(len(self.predictors)) / (2 * self.numberOfGameTurns - 1)
        )

        denominator = 0
        numerator = 0

        for expertInd in range(len(self.predictors)):
            expertPastAccuracy = self.predictors[expertInd].getPastAccuracy(
                self.userMoves
            )
            expertWeight = math.exp(-1 * eta * expertPastAccuracy)
            currentPrediction = self.predictors[expertInd].makePrediction(
                self.userMoves, self.userMovesFlipping, self.wins
            )
            numerator += currentPrediction * expertWeight
            denominator += expertWeight

        q = numerator / denominator
        return q

    def randomPredictor(self):
        """
        A random predictor that returns -1 or 1 with equal probability.

        Args:
            None.

        Returns:
            -1 or 1.
        """
        return random.randint(-1, 1)

    def initPredictors(self):
        """
        Initializes the predictors.

        Args:
            None.

        Returns:
            None.
        """

        self.predictors = []

        # Create bias predictors.
        biasPredictorMemory = [2, 3, 5]
        for bp in range(len(biasPredictorMemory)):
            self.predictors.append(
                BiasPredictor(biasPredictorMemory[bp], REGULAR_DATA_SERIES)
            )

        biasPredictorMemory = [2, 3, 5]
        for bp in range(len(biasPredictorMemory)):
            self.predictors.append(
                BiasPredictor(biasPredictorMemory[bp], FLIPPING_DATA_SERIES)
            )

        # Create pattern predictors.
        patternPredictorMemory = [2, 3, 4, 5]
        for bp in range(len(patternPredictorMemory)):
            self.predictors.append(
                PatternPredictor(patternPredictorMemory[bp], REGULAR_DATA_SERIES)
            )

        patternPredictorMemory = [2, 3, 4, 5]
        for bp in range(len(patternPredictorMemory)):
            self.predictors.append(
                PatternPredictor(patternPredictorMemory[bp], FLIPPING_DATA_SERIES)
            )

        # Create reactive predictors.
        reactivePredictorMemory = [1, 2]
        for bp in range(len(reactivePredictorMemory)):
            self.predictors.append(
                ReactivePredictor(reactivePredictorMemory[bp], USER_REACTIVE)
            )

        reactivePredictorMemory = [1, 2]
        for bp in range(len(reactivePredictorMemory)):
            self.predictors.append(
                ReactivePredictor(reactivePredictorMemory[bp], USER_REACTIVE_REG_DATA)
            )


class Predictor:
    """
    This class is a predictor prototype.

    Attributes:
      memoryLength: The length of the history to look at.
      dataType: The type of data to operate on.
      predictionsHistory: A list of the past predictions.
    """

    def __init__(self, memoryLength, dataType):
        """
        Initialize the predictor.

        Args:
          memoryLength: The length of the history to look at.
          dataType: The type of data to operate on.
        """
        self.memoryLength = memoryLength
        self.dataType = dataType
        self.predictionsHistory = []

    def getPastAccuracy(self, userMoves):
        """
        Get the past accuracy of the predictor.

        Args:
          userMoves: A list of the user's moves.

        Returns:
          The past accuracy of the predictor.
        """
        pastAccuracy = 0
        for i in range(len(userMoves)):
            pastAccuracy += abs(userMoves[i] - self.predictionsHistory[i])
        return pastAccuracy

    def makePrediction(self, userMoves, userMovesFlipping, wins):
        """
        Make a prediction.

        Args:
          userMoves: A list of the user's moves.
          userMovesFlipping: A list of the user's moves in the flipping case (if current=last then 1 else -1).
          wins: A list of who won each game turn.

        Returns:
          The prediction.
        """
        prediction = 0
        if self.dataType == REGULAR_DATA_SERIES:
            prediction = self.childPredictor(userMoves)
        elif self.dataType == FLIPPING_DATA_SERIES:
            prediction = self.childPredictor(userMovesFlipping) * userMoves[-1] * -1
        elif self.dataType == USER_REACTIVE:
            prediction = (
                self.childPredictor(userMovesFlipping, wins) * userMoves[-1] * -1
            )
        elif self.dataType == USER_REACTIVE_REG_DATA:
            prediction = self.childPredictor(userMoves, wins)

        if math.isnan(prediction):
            prediction = 0

        self.predictionsHistory.append(prediction)
        return prediction


class BiasPredictor(Predictor):
    """
    This class predicts the case of a biased user.

    Attributes:
      memoryLength: The length of the history to look at.
    """

    def __init__(self, memoryLength):
        """
        Initialize the predictor.

        Args:
          memoryLength: The length of the history to look at.
        """
        super().__init__(memoryLength, REGULAR_DATA_SERIES)

    def childPredictor(self, data):
        """
        Make a prediction.

        Args:
          data: A list of the user's moves.

        Returns:
          The prediction.
        """
        historyMean = 0
        cnt = 0
        while cnt < self.memoryLength and (data.length - cnt) > 0:
            historyMean += data[data.length - cnt - 1]
            cnt += 1
        historyMean /= cnt
        return historyMean


class PatternPredictor(Predictor):
    """
    This class predicts the case of a patterned user.

    Attributes:
        memoryLength: The length of the history to look at.
    """

    def __init__(self, memoryLength):
        """
        Initialize the predictor.

        Args:
        memoryLength: The length of the history to look at.
        """
        super().__init__(memoryLength, REGULAR_DATA_SERIES)

    def childPredictor(self, data):
        """
        Make a prediction.

        Args:
        data: A list of the user's moves.

        Returns:
        The prediction.
        """
        pattern = []
        prediction = 0
        score = 0
        ind = 0

        if data.length < self.memoryLength:
            return 0

        def rotatePattern():
            temp = pattern.pop()
            pattern.insert(0, temp)

            # Extract history length
            pattern = data.slice(-self.memoryLength)
            prediction = pattern[
                0
            ]  # The prediction is simply the element in the pattern (i.e. the first in this extracted array)

            # Start right before the pattern
            ind = data.length - self.memoryLength - 1
            while ind >= math.max(
                0, data.length - 3 * self.memoryLength
            ):  # Check maximum 2 appearances of the full pattern
                if pattern[pattern.length - 1] == data[ind]:
                    score += 1
                rotatePattern()
                ind -= 1

            score /= (
                2 * self.memoryLength
            )  # The maximum score is achieved when the pattern repeats itself twice
            return prediction * score


class ReactivePredictor(Predictor):
    """
    This class predicts the case of a reactive user.

    Attributes:
        memoryLength: The length of the history to look at.
    """

    def __init__(self, memoryLength):
        """
        Initialize the predictor.

        Args:
        memoryLength: The length of the history to look at.
        """
        super().__init__(memoryLength, REGULAR_DATA_SERIES)

        self.stateMachine = [0] * (2 ** (2 * memoryLength - 1))
        self.indMap = []
        for i in range(2 * memoryLength):
            self.indMap.append(2**i)

    def childPredictor(self, moves, wins):
        """
        Make a prediction.

        Args:
        moves: A list of the user's moves.
        wins: A list of who won each game turn.

        Returns:
        The prediction.
        """
        lastState = []
        lastStateInd = 0
        for i in range(self.memoryLength):
            lastState.append(wins[i])
            lastState.append(moves[i])
            lastStateInd += self.indMap[i]

        # Update the state machine.
        if self.stateMachine[lastStateInd] == 0:  # No prior info
            self.stateMachine[lastStateInd] = moves[-1] * 0.3
        elif (
            self.stateMachine[lastStateInd] == moves[-1] * 0.3
        ):  # We've been here before so strengthen prediction
            self.stateMachine[lastStateInd] = moves[-1] * 0.8
        elif (
            self.stateMachine[lastStateInd] == moves[-1] * 0.8
        ):  # We've been here before so strengthen prediction
            self.stateMachine[lastStateInd] = moves[-1] * 1
        elif self.stateMachine[lastStateInd] == moves[-1] * 1:  # Maximum confidence
            self.stateMachine[lastStateInd] = moves[-1] * 1
        else:  # Changed his mind - so go back to 0
            self.stateMachine[lastStateInd] = 0

        # What is the current state
        currentState = []
        currentStateInd = 0
        for i in range(self.memoryLength):
            currentState.append(wins[i + 1])
            currentState.append(moves[i + 1])
            currentStateInd += self.indMap[i]

        predictionAndScore = self.stateMachine[currentStateInd]

        # print('last state', lastState, ', last ind', lastStateInd, '    current state', currentState, '  current ind', currentStateInd, '    state machine:', self.stateMachine)
        return predictionAndScore
