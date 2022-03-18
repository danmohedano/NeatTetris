import neattetris.gamestates
from neattetris import *
from neat.nn import FeedForwardNetwork
import numpy as np
import sys
import select


class HumanActivation():
    decision_dict = {
        'a': 0,
        'd': 1,
        'q': 2,
        'e': 3,
        's': 4
    }

    def activate(self, inputs):
        i, o, e = select.select([sys.stdin], [], [], 0.5)
        if i:
            x = sys.stdin.readline().strip()
        else:
            x = 's'
        response = np.zeros(len(self.decision_dict.keys()))
        response[self.decision_dict[x]] = 1
        return response


def main():
    state = neattetris.gamestates.GameStateTetris()
    sim = neattetris.simulator.Simulator()

    print(sim.simulation(HumanActivation(), state, True))


if __name__ == '__main__':
    main()