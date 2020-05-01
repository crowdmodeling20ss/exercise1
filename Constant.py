S_EMPTY = 0
S_PEDESTRIAN = 1
S_OBSTACLE = 2
S_TARGET = 4

P_INIT = 0
P_WALKING = 1
P_WAITING = 2
P_EXIT = 3

# Default values
S_FILENAME = "exercise1/scenario.txt"
S_SPEED = 0
S_AVOIDANCE = 0
PEDESTRIAN_SIZE = 40  # Cm
SCENARIO_4_LINE_MOVEMENT_PEDESTRIANS = 20  # Number of pedestrians for line movement in Scenario 4
SCENARIO_7_WIDTH = 20  # M
SCENARIO_7_LENGTH = 200  # M

# TODO: We can increase number of direction later
DIRECTIONS = [[-1, 0],  # North
              [0, -1],  # West
              [0, 1],  # East
              [1, 0],  # South
              [-1, -1],  # North-East
              [-1, 1],  # North-West
              [1, -1],  # South-East
              [1, 1],  # South-West
              ]

D_TOP = 0
D_RIGHT = 1
D_BOTTOM = 2
D_LEFT = 3
