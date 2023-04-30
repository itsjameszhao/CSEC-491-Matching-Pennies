from enum import Enum

class Action(Enum):
    """Core actions in the Prisoner's Dilemma.
    There are only two possible actions, namely Cooperate or Defect,
    which are called C and D for convenience.
    """

    C = 0  # Cooperate
    D = 1  # Defect

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def flip(self):
        """Returns the opposite Action."""
        if self == Action.C:
            return Action.D
        return Action.C

    @classmethod
    def from_char(cls, character):
        """Converts a single character into an Action.
        Parameters
        ----------
        character: a string of length one
        Returns
        -------
        Action
            The action corresponding to the input character
        Raises
        ------
        UnknownActionError
            If the input string is not 'C' or 'D'
        """
        if character == "C":
            return cls.C
        if character == "D":
            return cls.D
        raise UnknownActionError('Character must be "C" or "D".')
