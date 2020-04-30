S_EMPTY = 0
S_PEDESTRIAN = 1
S_OBSTACLE = 2
S_TARGET = 4

P_WALKING = 0
P_WAITING = 1
P_EXIT = 2

# Default values
S_FILENAME = "scenario.txt"
S_SPEED = 0
S_AVOIDANCE = 0
PEDESTRIAN_SIZE = 40  # Cm
PEDESTRIAN_SIZE_SCENARIO_4 = 20  # With 40 cm, 6 pedestrians cannot fit in 1 sqm area
SCENARIO_7_WIDTH = 20  # M
SCENARIO_7_LENGTH = 200  # M

# TODO: We can increase number of direction later
DIRECTIONS = [[-1, 0],  # North
              [0, -1],  # East
              [0, 1],  # West
              [1, 0],  # South
              [-1, -1],  # North-East
              [-1, 1],  # North-West
              [1, -1],  # South-East
              [1, 1],  # South-West
              ]
