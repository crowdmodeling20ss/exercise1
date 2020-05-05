S_EMPTY = 0
S_EMPTY2 = 1
S_PEDESTRIAN = 2
S_OBSTACLE = 3
S_TARGET = 4

P_INIT = 0
P_WAITING = 1
P_WALKING = 2
P_EXIT = 3

# Default values
S_FILENAME = "scenario.txt"
S_SPEED = 0
S_AVOIDANCE = 0
PEDESTRIAN_SIZE = 40  # Cm
PEDESTRIAN_SIZE_SCENARIO_4 = 20  # With 40 cm, 6 pedestrians cannot fit in 1 sqm area
SCENARIO_4_LINES = 10  # Number of lines for line movement
SCENARIO_7_WIDTH = 20  # M
SCENARIO_7_LENGTH = 200  # M
MINIMUM_BORDER_LENGTH_SCENARIO_4 = 400  # M
MINIMUM_BORDER_LENGTH_SCENARIO_7 = 10  # M

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
