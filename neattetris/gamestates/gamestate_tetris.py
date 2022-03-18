from typing import Tuple
from .gamestate import GameState
import numpy as np
import random


_PIECES = [
    np.array([[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]),
    np.array([[0, 1, 0], [0, 1, 0], [0, 1, 1]]),
    np.array([[0, 1, 0], [0, 1, 0], [1, 1, 0]]),
    np.array([[1, 1], [1, 1]]),
    np.array([[1, 0, 0], [1, 1, 0], [0, 1, 0]]),
    np.array([[0, 0, 0], [1, 1, 1], [0, 1, 0]]),
    np.array([[0, 0, 1], [0, 1, 1], [0, 1, 0]]),
]
_N_PIECES = len(_PIECES)
_GRAVITY = [10, 10, 9, 9, 8, 8, 7, 7, 6, 6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]
_SCORE_MULTIPLIER = [0, 40, 100, 300, 1200]


class GameStateTetris(GameState):
    def __init__(self,
                 grid_width: int = 16,
                 grid_height: int = 26):
        self.grid = np.zeros((grid_width, grid_height))
        self.active_piece = None
        self.active_piece_position = (0, 0)
        self.next_pieces = []
        self.level = 0
        self.lines_cleared = 0
        self.t = 0
        self._next_piece()

    def _next_piece(self):
        """Updates the next piece in the game state.

        Choses the next piece in the game state and regenerates the piece bag
        if it is empty.
        """
        if len(self.next_pieces) == 0:
            self.next_pieces = list(range(_N_PIECES))
            random.shuffle(self.next_pieces)
        self.active_piece = _PIECES[self.next_pieces[-1]]
        self.active_piece_position = (self.grid.shape[0] // 2 - 2,
                                      self.grid.shape[1] - self.active_piece.shape[1])
        self.next_pieces = self.next_pieces[:-1]

    def _check_action(
            self,
            new_position: Tuple[int, int],
            new_piece: np.ndarray
    ) -> bool:
        """Checks if a certain action, described by the new position and grid
        representation of the piece, is valid.

        Args:
            new_position (Tuple[int, int]): Future position of the piece.
            new_piece (np.ndarray): Future grid representation of the piece.

        Returns:
            bool: True if future state is valid, False otherwise.
        """
        # Check left grid bound
        if new_position[0] < 0:
            for col in range(-new_position[0]):
                if np.sum(new_piece[col, :]) > 0:
                    return False

        # Check right bound
        if new_position[0] + new_piece.shape[0] > self.grid.shape[0]:
            relevant_cols = self.grid.shape[0] - (new_position[0] + new_piece.shape[0])
            for col in range(relevant_cols, 0):
                if np.sum(new_piece[col, :]) > 0:
                    return False

        # Check bottom bound
        if new_position[1] < 0:
            for row in range(-new_position[1]):
                if np.sum(new_piece[:, row]) > 0:
                    return False

        # Check grid colisions
        for j in range(new_piece.shape[1]):
            for i in range(new_piece.shape[0]):
                if new_piece[i][j] == 1 and self.grid[new_position[0] + i][new_position[1] + j] == 1:
                    return False

        return True

    def _check_lines(self) -> int:
        """Searches for complete rows in the grid.

        After locating complete rows in the grid, it removes them and shifts
        them down.

        Returns:
            int: Number of complete lines found.
        """
        lines_found = []

        # Search for complete lines
        for row in range(self.grid.shape[1]):
            if np.sum(self.grid[:, row]) == self.grid.shape[0]:
                lines_found.append(row)
                self.grid[:, row].fill(0)

        # Shift rows if needed
        shifts = 0
        for line in lines_found:
            self.grid[:, line - shifts:] = np.roll(self.grid[:, line - shifts:], -1, axis=1)
            shifts += 1

        return len(lines_found)

    def _leave_piece(self):
        """The active piece is dropped into the grid, updating its values.
        """
        for i in range(self.active_piece.shape[0]):
            for j in range(self.active_piece.shape[1]):
                if self.active_piece[i][j]:
                    self.grid[self.active_piece_position[0] + i][self.active_piece_position[1] + j] = 1

    def _move(
            self,
            direction: int
    ) -> bool:
        """Executes moving action if possible.

        Args:
            direction (int): Direction of movement. -1 left, 1 right, 0 down.

        Returns:
            bool: True if move has been performed, False otherwise.
        """
        if direction == 0:
            new_position = (self.active_piece_position[0],
                            self.active_piece_position[1] - 1)
        else:
            new_position = (self.active_piece_position[0] + direction,
                            self.active_piece_position[1])
        if self._check_action(new_position, self.active_piece):
            self.active_piece_position = new_position
            return True
        else:
            return False

    def _rotate(
            self,
            direction: int
    ) -> bool:
        """Executes rotation action if possible

        Args:
            direction (int): Direction of rotation. -1 left, 1 right.

        Returns:
            bool: True if move has been performed, False otherwise.
        """
        new_piece = np.copy(self.active_piece)
        new_piece = np.rot90(new_piece, -direction)

        if self._check_action(self.active_piece_position, new_piece):
            self.active_piece = new_piece
            return True
        else:
            return False

    def _move_left(self):
        return self._move(-1)

    def _move_right(self):
        return self._move(1)

    def _move_down(self):
        return self._move(0)

    def _rotate_left(self):
        return self._rotate(-1)

    def _rotate_right(self):
        return self._rotate(1)

    def pre_checks(self) -> bool:
        """Checks before decision execution.

        Not necessary for Tetris game logic.

        Returns:
            bool: True if the game state can continue, false otherwise.
        """
        return True

    def perform_action(self, decision: int):
        """Execution of action by game logic.

        Args:
            decision (int): Identifier for the action. Possible values:
                - 0: Move left
                - 1: Move right
                - 2: Rotate left (counter-clockwise)
                - 3: Rotate right (clockwise)
                - Otherwise: No action
        """
        if decision == 0:
            self._move_left()
        elif decision == 1:
            self._move_right()
        elif decision == 2:
            self._rotate_left()
        elif decision == 3:
            self._rotate_right()
        else:
            return

    def post_checks(self) -> Tuple[bool, float]:
        """Post decision checks.

        Checks for gravity activation. If gravity is activated, the piece is
        dropped one row. If this move is not possible, the piece is fused into
        the grid and a new active piece appears, as well as checking for lines.

        Returns:
            bool: True if the game state can continue, false otherwise.
            float: Score update after checks (score delta).
        """
        # Check gravity
        self.t = (self.t + 1) % _GRAVITY[self.level]

        if not self.t:
            drop_flag = self._move_down()

            if not drop_flag:
                # Check for end game if piece cannot be dropped
                if self.active_piece_position[1] == self.grid.shape[1] - self.active_piece.shape[1]:
                    return False, 0.0

                # Put active piece into grid
                self._leave_piece()

                # Check for lines (and shift pieces down if lines are found)
                # and create new piece
                lines = self._check_lines()
                self._next_piece()

                score_delta = _SCORE_MULTIPLIER[lines] * (self.level + 1)
                self.lines_cleared += lines
                self.level = self.lines_cleared // 10

                return True, score_delta

        return True, 0.0

    @property
    def data(self) -> np.ndarray:
        """Game state data represented as NN input.

        Provides the NN with the following information: Active piece grid,
        active piece position and game grid.

        Returns:
            np.ndarray: Game state data.
        """
        piece = np.zeros([4, 4])
        piece[:self.active_piece.shape[0], :self.active_piece.shape[1]] = self.active_piece
        return np.concatenate([piece.flatten(), self.active_piece_position, self.grid.flatten()])

    def visual(self):
        """Visual representation of the game state information.
        """
        print('=' * self.grid.shape[0])
        for j in range(self.grid.shape[1] - 1, -1, -1):
            print()
            for i in range(self.grid.shape[0]):
                if self.grid[i][j]:
                    print('#', end='')
                else:
                    try:
                        x, y = self.active_piece_position
                        if self.active_piece[i - x][j - y] == 1 and \
                                (i - x) >= 0 and (j - y) >= 0:
                            print('#', end='')
                        else:
                            print('-', end='')
                    except:
                        print('-', end='')
        print('\n' + '=' * self.grid.shape[0])
