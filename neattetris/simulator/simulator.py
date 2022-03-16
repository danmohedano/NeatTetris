import numpy as np


class Simulator:
    def __init__(self,
                 grid_width: int = 16,
                 grid_height: int = 24):
        self.grid_width = 16
        self.grid_heigh = 24
        self.grid = np.zeros((grid_width, grid_height))