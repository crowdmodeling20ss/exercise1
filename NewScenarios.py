import ast

import numpy as np

from Constant import *


def read_setup_file():
    filename = "new_scenario.txt"
    pedestrian_locations = []
    target_locations = []
    obstacle_locations = []
    grid_size = ()

    f = open(filename, "r")
    lines = f.readlines()

    grid_name = "Grid Size"
    pedestrian = "Pedestrian"
    obstacle = "Obstacle"
    target = "Target"

    for line in lines:
        setup = line.strip().split("=")
        setup[0] = setup[0].strip().lower()
        setup[1] = setup[1].strip()
        obj = ast.literal_eval(setup[1])

        if setup[0] == grid_name.lower():
            grid_size = obj
        elif setup[0] == pedestrian.lower():
            pedestrian_locations = obj
        elif setup[0] == target.lower():
            target_locations = obj
        elif setup[0] == obstacle.lower():
            obstacle_locations = obj

    f.close()
    return grid_size, pedestrian_locations, target_locations, obstacle_locations


def create_grid_new_scenario():
    grid_size, pedestrian_locations, target_locations, obstacle_locations = read_setup_file()
    grid = np.zeros(grid_size)

    for loc in pedestrian_locations:
        grid[loc] = S_PEDESTRIAN
    for loc in target_locations:
        grid[loc] = S_TARGET
    for loc in obstacle_locations:
        grid[loc] = S_OBSTACLE

    return grid
