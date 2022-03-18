from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np


class GameState(ABC):
    @abstractmethod
    def pre_checks(self) -> bool:
        """Checks before decision execution.

        Returns:
            bool: True if the game state can continue, false otherwise.
        """
        raise NotImplementedError()

    @abstractmethod
    def perform_action(self, decision: int):
        """Execution of action by game logic.

        Args:
            decision (int): Identifier for the action.
        """
        raise NotImplementedError()

    @abstractmethod
    def post_checks(self) -> Tuple[bool, float]:
        """Checks after decision execution.

        Returns:
            bool: True if the game state can continue, false otherwise.
            float: Fitness delta after the decision is executed.
        """
        raise NotImplementedError()

    @abstractmethod
    def visual(self):
        """Represents visually the game state.
        """
        raise NotImplementedError()

    @property
    def data(self) -> np.ndarray:
        """Game state data represented as NN input.

        Returns:
            np.ndarray: Game state data.
        """
        raise NotImplementedError()
