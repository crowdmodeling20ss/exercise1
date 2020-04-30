import numpy as np
import ast
from Constant import *


def scenario_1():
    # Corridor with 2m wide and 40m long
    width = int(200/PEDESTRIAN_SIZE)  # 5x40cm = 2m
    length = int(4000/PEDESTRIAN_SIZE)  # 100x40cm = 40m = 100
    grid_size = (width, length)
    pedestrian_locations = [(2, 0)]  # halfway
    obstacle_locations = []
    target_locations = []
    for i in range(0, width):
        target_locations.append((i, length - 1))

    return grid_size, pedestrian_locations, target_locations, obstacle_locations


def scenario_4(line_movement):
    # Corridor with 1000m long, 10m wide
    density = 1  # TODO: Read from the scenario.txt file or from Constant.py
    line_movement = line_movement.lower()
    width = int(1000 / PEDESTRIAN_SIZE_SCENARIO_4)
    length = int(100000 / PEDESTRIAN_SIZE_SCENARIO_4)
    obstacle_locations = []
    target_locations = []
    pedestrian_locations = []

    if line_movement == "true":
        width = 1

    grid_size = (width, length)

    if line_movement == "true":
        block_size = int(500 / PEDESTRIAN_SIZE_SCENARIO_4)  # 20cm x 500cm = 1sqm, so block size is 25
        if density >= 1:
            for j in range(0, length, block_size):
                loc_y = np.random.choice(list(range(j, j + block_size)), density, replace=False)
                for k in range(density):
                    pedestrian_locations.append((0, loc_y[k]))
        else:
            for j in range(0, length, block_size * 2):
                loc_y = np.random.choice(list(range(j, j + (block_size * 2))), 1, replace=False)
                pedestrian_locations.append((0, loc_y[0]))
    else:
        block_size = int(100 / PEDESTRIAN_SIZE_SCENARIO_4) # We need 100/20=5 block to represent 1 meter to calculate 1 sqm.
        # Placing pedestrians to 1 sqm block according to density
        if density >= 1:
            for i in range(0, width, block_size):
                for j in range(0, length, block_size):
                    loc_x = np.random.randint(low=i, high=i + block_size, size=density)
                    loc_y = np.random.randint(low=j, high=j + block_size, size=density)
                    for k in range(density):
                        loc = (loc_x[k], loc_y[k])
                        status = True
                        while status:
                            if loc in pedestrian_locations:
                                loc_x_new = np.random.randint(low=i, high=i + block_size)
                                loc_y_new = np.random.randint(low=j, high=j + block_size)
                                loc = (loc_x_new, loc_y_new)
                            else:
                                status = False
                        pedestrian_locations.append(loc)
        else:  # Density = 0.5, we are now putting one pedestrian to every 2 sqm.
            for i in range(0, width, block_size):
                for j in range(0, length, block_size * 2):
                    loc_x = np.random.randint(low=i, high=i + block_size)
                    loc_y = np.random.randint(low=j, high=j + (block_size * 2))
                    loc = (loc_x, loc_y)
                    status = True
                    while status:
                        if loc in pedestrian_locations:
                            loc_x_new = np.random.randint(low=i, high=i + block_size)
                            loc_y_new = np.random.randint(low=j, high=j + (block_size * 2))
                            loc = (loc_x_new, loc_y_new)
                        else:
                            status = False
                    pedestrian_locations.append(loc)

    for i in range(0, width):
        target_locations.append((i, length - 1))

    return grid_size, pedestrian_locations, target_locations, obstacle_locations

def scenario_6():
    width = int(200 / PEDESTRIAN_SIZE)
    side = int(1200 / PEDESTRIAN_SIZE)
    small_length = int(1000 / PEDESTRIAN_SIZE)
    grid_size = (side, side)
    dist_boundry = int(600)
    # TODO: pedestrians with 6m uniformly distributed
    pedestrian_locations = [(side - 3, 0)]

    obstacle_locations = []
    target_locations = []
    for i in range(0, small_length):
        border_up = (side - width - 1, i)
        border_left = (i, side - width - 1)
        obstacle_locations.append(border_up)
        obstacle_locations.append(border_left)
    for i in range(small_length, side):
        target_locations.append((0, i))

    return grid_size, pedestrian_locations, target_locations, obstacle_locations

def scenario_7():
    width = int(SCENARIO_7_WIDTH*100 / PEDESTRIAN_SIZE)  # 20m
    length = int(SCENARIO_7_LENGTH*100 / PEDESTRIAN_SIZE)  # 200m
    grid_size = (width, length)

    # TODO: 50 pedestrians
    pedestrian_locations = [(0, 0)]

    obstacle_locations = []
    target_locations = []
    for i in range(1, width):
        target_locations.append((i, length - 1))

    return grid_size, pedestrian_locations, target_locations, obstacle_locations

def create_grid():
    # Get values from file to create the grid
    f = open(S_FILENAME, "r")
    lines = f.readlines()
    line_movement = False
    for line in lines:
        lin = line.strip().split(" ")
        scenario = int(lin[1].strip())
        if scenario == 4 and len(lin) > 2:
            line_movement = lin[-1]

    if scenario == 1:
        grid_size, pedestrian_locations, target_locations, obstacle_locations = scenario_1()
    elif scenario == 4:
        grid_size, pedestrian_locations, target_locations, obstacle_locations = scenario_4(line_movement)
    elif scenario == 6:
        grid_size, pedestrian_locations, target_locations, obstacle_locations = scenario_6()
    elif scenario == 7:
        grid_size, pedestrian_locations, target_locations, obstacle_locations = scenario_7()
    else:
        return 0

    grid = np.zeros(grid_size)

    # Insert pedestrians, targets and obstacles to the grid.
    for loc in pedestrian_locations:
        grid[loc] = S_PEDESTRIAN
    for loc in target_locations:
        grid[loc] = S_TARGET
    for loc in obstacle_locations:
        grid[loc] = S_OBSTACLE

    return grid
