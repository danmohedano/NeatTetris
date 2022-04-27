import neat

import neattetris.gamestates
import numpy as np
import sys
import select
import os

WIDTH = 15
HEIGHT = 20


class HumanActivation:
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


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        state = neattetris.gamestates.GameStateTetris(WIDTH, HEIGHT)
        sim = neattetris.simulator.CoordSimulator()
        genome.fitness = sim.simulation(net, state)


def main_human():
    state = neattetris.gamestates.GameStateTetris()
    sim = neattetris.simulator.Simulator()

    print(sim.simulation(HumanActivation(), state, True))


def main_nn():
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), 'config')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # Create population
    p = neat.Population(config)

    # Add stdout reporter to show progress in the terminal
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run 2000 generations
    winner = p.run(eval_genomes, 200)
    #with open('winner', 'w') as f:
    #    winner.write_config(f, config)

    # Simulation for best genome
    while input('TRAINING FINISHED, SIMULATE WINNER') == '':
        net = neat.nn.FeedForwardNetwork.create(winner, config)
        state = neattetris.gamestates.GameStateTetris(WIDTH, HEIGHT)
        sim = neattetris.simulator.CoordSimulator()
        _ = sim.simulation(net, state, visual=True)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main_nn()
    elif sys.argv[1] == 'human':
        main_human()
