import numpy as np
import ast
from Constant import *


def scenario_1():
    # Corridor with 2m wide and 40m long
    width = int(200/PEDESTRIAN_SIZE)  # as number of blocks, 5x40cm = 2m
    length = int(4000/PEDESTRIAN_SIZE)  # as number of blocks, 100x40cm = 40m = 100
    grid_size = (width, length)
    pedestrian_locations = [(2, 0)]  # halfway
    obstacle_locations = []
    target_locations = []
    for i in range(0, width):
        target_locations.append((i, length - 1))

    return grid_size, pedestrian_locations, target_locations, obstacle_locations


def scenario_4(line_movement):
    # Corridor with 1000m long, 10m wide
    density = 0.5  # TODO: Read from the scenario.txt file or from Constant.py
    line_movement = line_movement.lower()
    width = int(1000 / PEDESTRIAN_SIZE_SCENARIO_4)  # as number of blocks 50
    length = int(100000 / PEDESTRIAN_SIZE_SCENARIO_4)  # as number of blocks, 5000
    obstacle_locations = []
    target_locations = []
    pedestrian_locations = []
    number_of_pedestrians = int(10 * 1000 * density)
    minimum_border_length = int((MINIMUM_BORDER_LENGTH_SCENARIO_4 * 100) / PEDESTRIAN_SIZE_SCENARIO_4)  # as number of blocks, 2000 block is 400 meters, all pedestrians will be distributed before the first measuring point

    if line_movement == "true":
        width = 1
        number_of_pedestrians = int(width * 1000 * density)
        minimum_border_length = int(number_of_pedestrians / width)  # minimum length to fit all pedestrians to the area

    grid_size = (width, length)

    # Place pedestrians according to density, with uniform distribution
    if line_movement == "true":  # TODO: PROBLEM WITH LINE MOVEMENT, NUMBER OF PEDESTRIANS IS BIGGER THAN THE AREA WITH DENSITY = 6, CANNOT FIT
        loc_y = np.random.choice(list(range(0, minimum_border_length)), number_of_pedestrians, replace=False)  # minimum_border_length=6000 out of grid, our grid is 1x5000
        for k in range(number_of_pedestrians):
            loc = (0, loc_y[k])
            status = True
            while status:
                if loc in pedestrian_locations:
                    loc_y_new = np.random.choice(list(range(0, minimum_border_length)), 1, replace=False)
                    loc = (0, loc_y_new[0])
                else:
                    status = False
            pedestrian_locations.append(loc)
    else:
        loc_x = np.random.randint(low=0, high=width, size=number_of_pedestrians)
        loc_y = np.random.randint(low=0, high=minimum_border_length, size=number_of_pedestrians)
        for k in range(number_of_pedestrians):
            loc = (loc_x[k], loc_y[k])
            status = True
            while status:
                if loc in pedestrian_locations:
                    loc_x_new = np.random.randint(low=0, high=width)
                    loc_y_new = np.random.randint(low=0, high=minimum_border_length)
                    loc = (loc_x_new, loc_y_new)
                else:
                    status = False
            pedestrian_locations.append(loc)

    # Place targets
    for i in range(0, width):
        target_locations.append((i, length - 1))

    return grid_size, pedestrian_locations, target_locations, obstacle_locations

def scenario_6():
    width = int(200 / PEDESTRIAN_SIZE)  # as number of blocks
    side = int(1200 / PEDESTRIAN_SIZE)  # as number of blocks
    small_length = int(1000 / PEDESTRIAN_SIZE)  # as number of blocks
    grid_size = (side, side)
    dist_boundary = int(600 / PEDESTRIAN_SIZE)
    pedestrian_locations = []
    obstacle_locations = []
    target_locations = []
    number_of_pedestrians = 20

    # Place 20 pedestrian with uniform distribution
    loc_x = np.random.randint(low=side-width, high=side, size=number_of_pedestrians)
    loc_y = np.random.randint(low=0, high=dist_boundary, size=number_of_pedestrians)
    for k in range(number_of_pedestrians):
        loc = (loc_x[k], loc_y[k])
        status = True
        while status:
            if loc in pedestrian_locations:
                loc_x_new = np.random.randint(low=side - width, high=side)
                loc_y_new = np.random.randint(low=0, high=dist_boundary)
                loc = (loc_x_new, loc_y_new)
            else:
                status = False
        pedestrian_locations.append(loc)

    # Place obstacles
    for i in range(0, small_length):
        border_up = (side - width - 1, i)
        border_left = (i, side - width - 1)
        obstacle_locations.append(border_up)
        obstacle_locations.append(border_left)

    # Place targets
    for i in range(small_length, side):
        target_locations.append((0, i))

    return grid_size, pedestrian_locations, target_locations, obstacle_locations

def scenario_7():
    width = int(SCENARIO_7_WIDTH * 100 / PEDESTRIAN_SIZE)  # as number of blocks
    length = int(SCENARIO_7_LENGTH * 100 / PEDESTRIAN_SIZE)  # as number of blocks
    grid_size = (width, length)
    number_of_pedestrians = 50
    obstacle_locations = []
    target_locations = []
    pedestrian_locations = []
    minimum_border_length = int((MINIMUM_BORDER_LENGTH_SCENARIO_7 * 100) / PEDESTRIAN_SIZE)  # 25 blocks

    # Place 20 pedestrian with uniform distribution
    loc_x = np.random.randint(low=0, high=width, size=number_of_pedestrians)
    loc_y = np.random.randint(low=0, high=minimum_border_length, size=number_of_pedestrians)
    for k in range(number_of_pedestrians):
        loc = (loc_x[k], loc_y[k])
        status = True
        while status:
            if loc in pedestrian_locations:
                loc_x_new = np.random.randint(low=0, high=width)
                loc_y_new = np.random.randint(low=0, high=length)
                loc = (loc_x_new, loc_y_new)
            else:
                status = False
        pedestrian_locations.append(loc)

    # Place targets
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
