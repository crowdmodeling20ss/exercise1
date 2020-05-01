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
    line_movement = line_movement.lower()
    width = int(1000 / PEDESTRIAN_SIZE)
    length = int(100000 / PEDESTRIAN_SIZE)
    obstacle_locations = []
    target_locations = []
    pedestrian_locations = []

    if line_movement == "true":
        width = 1

    grid_size = (width, length)

    if line_movement == "true":
        for i in range(0,SCENARIO_4_LINE_MOVEMENT_PEDESTRIANS):
            pedestrian_locations.append((0, i))
    else:
        # TODO: pedestrians with different densities
        pedestrian_locations = [(2, 0)]  # Just an example

        for i in range(0, width):
            target_locations.append((i, length - 1))

    return grid_size, pedestrian_locations, target_locations, obstacle_locations

def scenario_6():
    width = int(200 / PEDESTRIAN_SIZE)
    side = int(1200 / PEDESTRIAN_SIZE)
    small_length = int(1000 / PEDESTRIAN_SIZE)
    grid_size = (side, side)

    # TODO: pedestrians with 6m uniformly distributed
    pedestrian_locations = [(side - 3, 0), (side-2, 0), (side-4, 0)]

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

