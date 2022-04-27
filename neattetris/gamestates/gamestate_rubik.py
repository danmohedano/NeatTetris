from typing import Tuple
import numpy as np
from .gamestate import GameState
import random
from termcolor import colored
import colorama


class Face:
    def __init__(self, value, size):
        self.size = size
        self.data = [[value for y in range(size)] for x in range(size)]

    def __getitem__(self, loc):
        if loc[0] == -1:
            if loc[1] == -1:
                # Full Face
                return self.data
            else:
                # Access to a column (:, y)
                column = [0 for i in range(self.size)]
                for j in range(self.size):
                    column[j] = self.data[j][loc[1]]
                return column
        else:
            if loc[1] == -1:
                # Access to a line (x, :)
                line = [0 for i in range(self.size)]
                for j in range(self.size):
                    line[j] = self.data[loc[0]][j]
                return line
            else:
                # Access to a single element
                return self.data[loc[0]][loc[1]]

    def replace(self, new, x=-1, y=-1):

        if y == -1:
            # Replacement of a line
            for i in range(self.size):
                self.data[x][i] = new[i]
        else:
            # Replacement of a column
            for i in range(self.size):
                self.data[i][y] = new[i]

    def rotate(self, direction):
        if direction:
            aux1 = self.data[0][0]
            aux2 = self.data[0][1]
            self.data[0][0] = self.data[2][0]
            self.data[0][1] = self.data[1][0]
            self.data[2][0] = self.data[2][2]
            self.data[1][0] = self.data[2][1]
            self.data[2][2] = self.data[0][2]
            self.data[2][1] = self.data[1][2]
            self.data[0][2] = aux1
            self.data[1][2] = aux2
        else:
            aux1 = self.data[0][2]
            aux2 = self.data[0][1]
            self.data[0][2] = self.data[2][2]
            self.data[0][1] = self.data[1][2]
            self.data[2][2] = self.data[2][0]
            self.data[1][2] = self.data[2][1]
            self.data[2][0] = self.data[0][0]
            self.data[2][1] = self.data[1][0]
            self.data[0][0] = aux1
            self.data[1][0] = aux2

    def get_color(self, x, y):
        colors = ['grey', 'red', 'green', 'magenta', 'blue', 'yellow']
        return colors[self.data[x][y]]


class GameStateRubik(GameState):
    def __init__(self, size = 3):
        self.size = size
        self.down = Face(0, size)
        self.front = Face(1, size)
        self.right = Face(2, size)
        self.back = Face(3, size)
        self.left = Face(4, size)
        self.up = Face(5, size)
        self._scramble()

    def _scramble(self):
        for i in range(20):
            self.perform_action(random.randint(0, 11))

    def visual(self):
        # colored(u'\u25ae', self.down.get_color(), self.down.get_on_color())
        print(u'\u25af\u25af\u25af' + ' ' +
              colored(u'\u25ae', self.up.get_color(0, 0)) +
              colored(u'\u25ae', self.up.get_color(0, 1)) +
              colored(u'\u25ae', self.up.get_color(0, 2)) +
              ' ' + u'\u25af\u25af\u25af' +
              ' ' + u'\u25af\u25af\u25af' + ' ')

        print(u'\u25af\u25af\u25af' + ' ' +
              colored(u'\u25ae', self.up.get_color(1, 0)) +
              colored(u'\u25ae', self.up.get_color(1, 1)) +
              colored(u'\u25ae', self.up.get_color(1, 2)) +
              ' ' + u'\u25af\u25af\u25af' +
              ' ' + u'\u25af\u25af\u25af' + ' ')

        print(u'\u25af\u25af\u25af' + ' ' +
              colored(u'\u25ae', self.up.get_color(2, 0)) +
              colored(u'\u25ae', self.up.get_color(2, 1)) +
              colored(u'\u25ae', self.up.get_color(2, 2)) +
              ' ' + u'\u25af\u25af\u25af' +
              ' ' + u'\u25af\u25af\u25af' + ' ')

        print(colored(u'\u25ae', self.left.get_color(0, 0)) +
              colored(u'\u25ae', self.left.get_color(0, 1)) +
              colored(u'\u25ae', self.left.get_color(0, 2)) + ' ' +
              colored(u'\u25ae', self.front.get_color(0, 0)) +
              colored(u'\u25ae', self.front.get_color(0, 1)) +
              colored(u'\u25ae', self.front.get_color(0, 2)) + ' ' +
              colored(u'\u25ae', self.right.get_color(0, 0)) +
              colored(u'\u25ae', self.right.get_color(0, 1)) +
              colored(u'\u25ae', self.right.get_color(0, 2)) + ' ' +
              colored(u'\u25ae', self.back.get_color(0, 0)) +
              colored(u'\u25ae', self.back.get_color(0, 1)) +
              colored(u'\u25ae', self.back.get_color(0, 2)))

        print(colored(u'\u25ae', self.left.get_color(1, 0)) +
              colored(u'\u25ae', self.left.get_color(1, 1)) +
              colored(u'\u25ae', self.left.get_color(1, 2)) + ' ' +
              colored(u'\u25ae', self.front.get_color(1, 0)) +
              colored(u'\u25ae', self.front.get_color(1, 1)) +
              colored(u'\u25ae', self.front.get_color(1, 2)) + ' ' +
              colored(u'\u25ae', self.right.get_color(1, 0)) +
              colored(u'\u25ae', self.right.get_color(1, 1)) +
              colored(u'\u25ae', self.right.get_color(1, 2)) + ' ' +
              colored(u'\u25ae', self.back.get_color(1, 0)) +
              colored(u'\u25ae', self.back.get_color(1, 1)) +
              colored(u'\u25ae', self.back.get_color(1, 2)))

        print(colored(u'\u25ae', self.left.get_color(2, 0)) +
              colored(u'\u25ae', self.left.get_color(2, 1)) +
              colored(u'\u25ae', self.left.get_color(2, 2)) + ' ' +
              colored(u'\u25ae', self.front.get_color(2, 0)) +
              colored(u'\u25ae', self.front.get_color(2, 1)) +
              colored(u'\u25ae', self.front.get_color(2, 2)) + ' ' +
              colored(u'\u25ae', self.right.get_color(2, 0)) +
              colored(u'\u25ae', self.right.get_color(2, 1)) +
              colored(u'\u25ae', self.right.get_color(2, 2)) + ' ' +
              colored(u'\u25ae', self.back.get_color(2, 0)) +
              colored(u'\u25ae', self.back.get_color(2, 1)) +
              colored(u'\u25ae', self.back.get_color(2, 2)))

        print(u'\u25af\u25af\u25af' + ' ' +
              colored(u'\u25ae', self.down.get_color(0, 0)) +
              colored(u'\u25ae', self.down.get_color(0, 1)) +
              colored(u'\u25ae', self.down.get_color(0, 2)) +
              ' ' + u'\u25af\u25af\u25af' +
              ' ' + u'\u25af\u25af\u25af' + ' ')

        print(u'\u25af\u25af\u25af' + ' ' +
              colored(u'\u25ae', self.down.get_color(1, 0)) +
              colored(u'\u25ae', self.down.get_color(1, 1)) +
              colored(u'\u25ae', self.down.get_color(1, 2)) +
              ' ' + u'\u25af\u25af\u25af' +
              ' ' + u'\u25af\u25af\u25af' + ' ')

        print(u'\u25af\u25af\u25af' + ' ' +
              colored(u'\u25ae', self.down.get_color(2, 0)) +
              colored(u'\u25ae', self.down.get_color(2, 1)) +
              colored(u'\u25ae', self.down.get_color(2, 2)) +
              ' ' + u'\u25af\u25af\u25af' +
              ' ' + u'\u25af\u25af\u25af' + ' ')

    def input(self):
        move = input("Move ( l | r | u | d | f | b )(' for counter-clockwise): ")
        if move == 'exit':
            return 1

        if len(move) == 2:
            direction = 0
        else:
            direction = 1

        if move[0] == 'l':
            self.m_left(direction)
        elif move[0] == 'r':
            self.m_right(direction)
        elif move[0] == 'u':
            self.m_up(direction)
        elif move[0] == 'd':
            self.m_down(direction)
        elif move[0] == 'f':
            self.m_front(direction)
        elif move[0] == 'b':
            self.m_back(direction)

        return 0

    def m_left(self, direction):
        self.left.rotate(direction)
        # Accessed: F[-1,0] | U[-1,0] | B[-1,2] | D[-1,0]
        aux = self.up[-1, 0]
        if direction:
            self.up.replace(self.back[-1, 2], -1, 0)
            self.back.replace(self.down[-1, 0], -1, 2)
            self.down.replace(self.front[-1, 0], -1, 0)
            self.front.replace(aux, -1, 0)
        else:
            self.up.replace(self.front[-1, 0], -1, 0)
            self.front.replace(self.down[-1, 0], -1, 0)
            self.down.replace(self.back[-1, 2], -1, 0)
            self.back.replace(aux, -1, 2)

    def m_right(self, direction):
        self.right.rotate(direction)
        # Accessed: F[-1,2] | U[-1,2] | B[-1,0] | D[-1,2]
        aux = self.up[-1, 2]
        if direction:
            self.up.replace(self.front[-1, 2], -1, 2)
            self.front.replace(self.down[-1, 2], -1, 2)
            self.down.replace(self.back[-1, 0], -1, 2)
            self.back.replace(aux, -1, 0)
        else:
            self.up.replace(self.back[-1, 0], -1, 2)
            self.back.replace(self.down[-1, 2], -1, 0)
            self.down.replace(self.front[-1, 2], -1, 2)
            self.front.replace(aux, -1, 2)

    def m_up(self, direction):
        self.up.rotate(direction)
        # Accessed: F[0, -1] | R[0, -1] | B[0, -1] | L[0, -1]
        aux = self.front[0, -1]
        if direction:
            self.front.replace(self.right[0, -1], 0, -1)
            self.right.replace(self.back[0, -1], 0, -1)
            self.back.replace(self.left[0, -1], 0, -1)
            self.left.replace(aux, 0, -1)
        else:
            self.front.replace(self.left[0, -1], 0, -1)
            self.left.replace(self.back[0, -1], 0, -1)
            self.back.replace(self.right[0, -1], 0, -1)
            self.right.replace(aux, 0, -1)

    def m_down(self, direction):
        self.down.rotate(direction)
        # Accessed: F[2, -1] | R[2, -1] | B[2, -1] | L[2, -1]
        aux = self.front[2, -1]
        if direction:
            self.front.replace(self.left[2, -1], 2, -1)
            self.left.replace(self.back[2, -1], 2, -1)
            self.back.replace(self.right[2, -1], 2, -1)
            self.right.replace(aux, 2, -1)
        else:
            self.front.replace(self.right[2, -1], 2, -1)
            self.right.replace(self.back[2, -1], 2, -1)
            self.back.replace(self.left[2, -1], 2, -1)
            self.left.replace(aux, 2, -1)

    def m_front(self, direction):
        self.front.rotate(direction)
        # Accessed: U[2, -1] | R[-1,0] | D[0, -1] | L[-1,2]
        aux = self.up[2, -1]
        if direction:
            self.up.replace(self.left[-1, 2], 2, -1)
            self.left.replace(self.down[0, -1], -1, 2)
            self.down.replace(self.right[-1, 0], 0, -1)
            self.right.replace(aux, -1, 0)
        else:
            self.up.replace(self.right[-1, 0], 2, -1)
            self.right.replace(self.down[0, -1], -1, 0)
            self.down.replace(self.left[-1, 2], 0, -1)
            self.left.replace(aux, -1, 2)

    def m_back(self, direction):
        self.back.rotate(direction)
        # Accessed: U[0, -1] | R[-1,2] | D[2, -1] | L[-1,0]
        aux = self.up[0, -1]
        if direction:
            self.up.replace(self.right[-1, 2], 0, -1)
            self.right.replace(self.down[2, -1], -1, 2)
            self.down.replace(self.left[-1, 0], 2, -1)
            self.left.replace(aux, -1, 0)
        else:
            self.up.replace(self.left[-1, 0], 0, -1)
            self.left.replace(self.down[2, -1], -1, 0)
            self.down.replace(self.right[-1, 2], 2, -1)
            self.right.replace(aux, -1, 2)

    def pre_checks(self) -> bool:
        return True

    def perform_action(self, decision: int):
        face = decision // 2
        direction = -1 if decision % 2 else 1

        if face == 1:
            self.m_front(direction)
        elif face == 2:
            self.m_right(direction)
        elif face == 3:
            self.m_back(direction)
        elif face == 4:
            self.m_left(direction)
        elif face == 5:
            self.m_up(direction)
        else:
            self.m_down(direction)

    def post_checks(self) -> Tuple[bool, float]:
        faces = [self.down[:, :], self.front[:, :], self.right[:, :], self.back[:, :], self.left[:, :], self.up[:, :]]
        for i in range(6):
            if len(np.unique(faces[i])) > 1:
                return True, -1.0

        return False, 0.0

    @property
    def data(self) -> np.ndarray:
        faces = [self.down[:, :], self.front[:, :], self.right[:, :], self.back[:, :], self.left[:, :], self.up[:, :]]
        state = np.zeros([6, 3, 3, 6])
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    state[i, j, k, faces[i][j][k]] = 1.0

        return state.flatten()

