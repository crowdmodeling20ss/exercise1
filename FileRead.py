import numpy as np
import ast
from Constant import *

def read_setup_file():
    pedestrian_locations = []
    target_locations = []
    obstacle_locations = []
    grid_size = ()
    speed = S_SPEED
    avoidance = S_AVOIDANCE

    f = open(S_FILENAME, "r")
    lines = f.readlines()

    for line in lines:
        setup = line.strip().split("=")
        setup[0] = setup[0].strip().lower()
        setup[1] = setup[1].strip()
        obj = ast.literal_eval(setup[1])

        # Create arrays and values to setup the grid map
        if setup[0] == S_GRID_SIZE_TUPLE_NAME.lower():
            grid_size = obj
        elif setup[0] == S_PEDESTRIAN_LOCATION_ARR_NAME.lower():
            pedestrian_locations = obj
        elif setup[0] == S_TARGET_LOCATION_ARR_NAME.lower():
            target_locations = obj
        elif setup[0] == S_OBSTACLE_LOCATION_ARR_NAME.lower():
            obstacle_locations = obj
        elif setup[0] == S_SPEED_INT_NAME.lower():
            speed = obj
        elif setup[0] == S_AVOIDANCE_INT_NAME.lower():
            avoidance = obj

    return grid_size, pedestrian_locations, target_locations, obstacle_locations, speed, avoidance


def create_grid():
    # Get values from file to create the grid
    grid_size, pedestrian_locations, target_locations, obstacle_locations, speed, avoidance = read_setup_file()
    grid = np.zeros(grid_size)

    # Insert pedestrians, targets and obstacles to the grid.
    for loc in pedestrian_locations:
        grid[loc] = S_PEDESTRIAN
    for loc in target_locations:
        grid[loc] = S_TARGET
    for loc in obstacle_locations:
        grid[loc] = S_OBSTACLE

    return grid

