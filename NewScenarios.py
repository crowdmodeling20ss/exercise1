import ast

import numpy as np

from Constant import *

from Simulation import *


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


def main():
    ## New scenario from user
    new_grid = create_grid_new_scenario()
    new_the_grid = GridCreator(new_grid, 1)
    new_map_obj = Map(new_the_grid.grid.shape[0], new_the_grid.grid.shape[1],
                      new_the_grid.grid, new_the_grid.corners)
    new_model = CellularModel(new_map_obj, [13, 20])
    runSimulation(new_model)


if __name__ == '__main__':
    main()
