# NeatTetris
Implementation of Tetris and usage of NEAT to play the game

### Tetris Information
- Playfield dimensions: 10x[16,24] cells.
- Original scoring system (points awarded at level `n`):
  - 1 line: 40 * (n + 1)
  - 2 lines: 100 * (n + 1)
  - 3 lines: 300 * (n + 1)
  - 4 lines: 1200 * (n + 1)



### Implementation notes
- Simulation: in order to increase the difficulty for each level, akin to what a human player would experience, gravity has been implemented. Gravity determines the amount of frames that pass before a tetromino is dropped one cell. The higher the level, the bigger the gravity, and therefore the faster the tetrominoes drop. Because the AI player can select an action each frame, the reduction in frames until drop reduces the amount of actions the AI can make.
- Actions: even though dropping is a possible action in the game, in order to avoid confusion in the network, the only possible actions for the AI player are :
  - Move left
  - Move right
  - Rotate left
  - Rotate right
- When the AI agent tries to perform an invalid move, the simulator decides to ignore it (possible TODO: reduce scoring with impossible moves).
- 