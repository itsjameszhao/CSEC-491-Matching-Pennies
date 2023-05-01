from enum import Enum
import random


class Action(Enum):
    """
    Core actions, can be LEFT or RIGHT
    """

    L = -1  # Left
    R = 1  # Right


def random_choice(l_prob, r_prob):
    """
    This function takes in two probabilities and chooses between two actions with those probabilities.

    Args:
      l_prob: The probability of choosing the left action.
      r_prob: The probability of choosing the right action.

    Returns:
      The action that was chosen.
    """

    # Verify that the probabilities sum to 1.
    if round(l_prob + r_prob, 3) != 1.0:
        raise ValueError("The probabilities must sum to 1.")

    # Choose a random number between 0 and 1.
    random_number = random.random()

    # If the random number is less than the left probability, choose the left action.
    if random_number < l_prob:
        return Action.L

    # Otherwise, choose the right action.
    return Action.R


class BushMostellerBot:
    """
    A player that is based on Bush Mosteller reinforced learning algorithm, it
    decides what it will play only depending on its own previous payoffs.
    The probability of playing L or R will be updated using a stimulus which
    represents a win or a loss of value based on its previous play's payoff in
    the specified probability.  The more a play will be rewarded through rounds,
    the more the player will be tempted to use it.
    Names:
    - Bush Mosteller: [Luis2008]_
    """

    def __init__(
        self,
        numberOfGameTurns = 20,
        l_prob: float = 0.5,
        r_prob: float = 0.5,
        aspiration_level_divider: float = 2.0,
        learning_rate: float = 0.5,
    ) -> None:
        """
        Parameters
        c_prob: float, 0.5
           Probability to play C , is modified during the match
        d_prob: float, 0.5
           Probability to play D , is modified during the match
        aspiration_level_divider: float, 3.0
            Value that regulates the aspiration level,
            isn't modified during match
        learning rate [0 , 1]
            Percentage of learning speed
        Variables / Constants
        stimulus (Var: [-1 , 1]): float
            Value that impacts the changes of action probability
        _aspiration_level: float
            Value that impacts the stimulus changes, isn't modified during match
        _init_c_prob , _init_d_prob : float
            Values used to properly set up reset(),
            set to original probabilities
        """
        self._l_prob, self._r_prob = l_prob, r_prob
        self._init_l_prob, self._init_r_prob = l_prob, r_prob
        self._aspiration_level = abs((1 / aspiration_level_divider))

        self._stimulus = 0.0
        self._learning_rate = learning_rate
        self.numberOfGameTurns = numberOfGameTurns

    def updateUserMove(self, opponent_move):
        """
        Updates the stimulus attribute based on the opponent's history. Used by
        the strategy.
        Parameters
        opponent : axelrod.Player
            The current opponent
        """

        my_payoff = 1 if (self.prev_move == opponent_move) else 0

        self._stimulus = (my_payoff - self._aspiration_level) / abs(
            (1 - self._aspiration_level)
        )
        # Lowest range for stimulus
        # Highest doesn't need to be tested since it is divided by the highest
        # reward possible
        if self._stimulus < -1:
            self._stimulus = -1

    def updateBotPrediction(self):
        # Updates probability following previous choice L
        if self.prev_move == Action.L.value:
            if self._stimulus >= 0:
                self._l_prob += (
                    self._learning_rate * self._stimulus * (1 - self._l_prob)
                )

            elif self._stimulus < 0:
                self._l_prob += self._learning_rate * self._stimulus * self._l_prob

            # Normalize right probability
            self._r_prob = 1 - self._l_prob

        # Updates probability following previous choice R
        elif self.prev_move == Action.R.value:
            if self._stimulus >= 0:
                self._r_prob += (
                    self._learning_rate * self._stimulus * (1 - self._r_prob)
                )

            elif self._stimulus < 0:
                self._r_prob += self._learning_rate * self._stimulus * self._r_prob

            # Normalize left probability
            self._l_prob = 1 - self._r_prob


    def getBotPrediction(self) -> Action:
        """Actual strategy definition that determines player's action."""

        self.prev_move = random_choice(self._l_prob, self._r_prob).value
        return self.prev_move
