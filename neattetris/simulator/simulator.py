from neattetris.gamestates.gamestate import GameState
from neat.nn import FeedForwardNetwork
import numpy as np


class Simulator:
    def __init__(self):
        self.fitness = 0
        self.game_state = None

    def simulation(
            self,
            net: FeedForwardNetwork,
            game_state: GameState,
            visual: bool = False
    ) -> float:
        """Simulation of a given neural network.

        Simulates the game logic with a given neural network agent. For each
        frame, the simulator calculates the agent's response to the game state
        and executes the action.

        Args:
            net (FeedForwardNetwork): Neural network agent to decide the
                actions taken through the simulation.
            game_state (GameState): Initialized GameState to simulate.
            visual (bool): If the execution should be shown or not.

        Returns:
            float: Fitness of the given neural network provided.
        """
        # 1. Initialize game state and needed simulation variables
        self.game_state = game_state
        self.fitness = 0.0

        # 2. While the game is not over, execute simulation steps
        if visual:
            self.game_state.visual()

        while self.simulation_step(net):
            if visual:
                self.game_state.visual()

        return self.fitness

    def simulation_step(
            self,
            net: FeedForwardNetwork
    ) -> bool:
        """Simulation step for a given neural network.

        Executes a simulation step for a given neural network agent. The step
        consists in the evalutation of the game state by the network and the
        corresponding execution of the action chosen by the agent.

        Args:
            net: Neural network agent to decide the action.

        Returns:
            bool: True if the game state can continue, false otherwise.
        """
        # 0. Pre-decision checks and updates
        if not self.game_state.pre_checks():
            return False

        # 1. Evaluation of game state by the agent and selection of action
        output = net.activate(self.game_state.data)
        decision = np.argmax(output)

        # 2. Performing of selected action (if possible)
        self.game_state.perform_action(decision)

        # 3. Post-decision checks and updates
        end_flag, fitness_delta = self.game_state.post_checks()
        self.fitness += fitness_delta

        return end_flag
