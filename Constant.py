S_EMPTY = 0
S_PEDESTRIAN = 1
S_OBSTACLE = 2
S_TARGET = 4

# Default values
S_FILENAME = "grid_setup.txt"
S_SPEED = 0
S_AVOIDANCE = 0

# Array and tuple name formats in grid_setup.txt
S_GRID_SIZE_TUPLE_NAME = "Grid Size"
S_PEDESTRIAN_LOCATION_ARR_NAME = "Pedestrian"
S_TARGET_LOCATION_ARR_NAME = "Target"
S_OBSTACLE_LOCATION_ARR_NAME = "Obstacle"
S_SPEED_INT_NAME = "Speed"
S_AVOIDANCE_INT_NAME = "Avoidance"

# TODO: We can increase number of direction later
DIRECTIONS = [[-1, 0],  # North
              [0, -1],  # East
              [0, 1],  # West
              [1, 0],  # South
              #[-1, -1],  # North-East
              #[-1, 1],  # North-West
              #[1, -1],  # South-East
              #[1, 1],  # South-West
              ]
