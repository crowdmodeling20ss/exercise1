import numpy as np

from Constant import *

'''
    RiMEA scenarios
'''

def scenario_1():  # Scenario number: 1
    # Corridor with 2m wide and 40m long
    width = int(200 / PEDESTRIAN_SIZE)  # as number of blocks, 5x40cm = 2m
    length = int(4000 / PEDESTRIAN_SIZE)  # as number of blocks, 100x40cm = 40m = 100
    grid_size = (width, length)
    pedestrian_locations = [(2, 0)]  # halfway
    obstacle_locations = []
    target_locations = []
    is_dijkstra = True
    is_exit = True
    speed = [[13, 20]]
    scale_var = 4

    for i in range(0, width):
        target_locations.append((i, length - 1))

    return grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra, is_exit, speed, scale_var


def scenario_4(line_movement, density):  # Scenario number: 4
    # Corridor with 1000m long, 10m wide
    width = int(1000 / PEDESTRIAN_SIZE_SCENARIO_4)  # as number of blocks 50
    length = int(100000 / PEDESTRIAN_SIZE_SCENARIO_4)  # as number of blocks, 5000
    obstacle_locations = []
    target_locations = []
    pedestrian_locations = []
    number_of_pedestrians = int(10 * 1000 * density)
    # as number of blocks, 2000 block is 400 meters, all pedestrians will be distributed before the first measuring point
    minimum_border_length = int((MINIMUM_BORDER_LENGTH_SCENARIO_4 * 100) / PEDESTRIAN_SIZE_SCENARIO_4)
    is_dijkstra = True
    is_exit = True
    speed = [[13, 20]]
    scale_var = 1 #4

    if line_movement == "true":
        width = SCENARIO_4_LINES

    grid_size = (width, length)

    # Place pedestrians according to density, with uniform distribution
    if line_movement:  # Here, pedestrians are placed one after the other in lines
        border = int(number_of_pedestrians / SCENARIO_4_LINES)
        for j in range(border):
            for i in range(width):
                loc = (i, j)
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

    return grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra, is_exit, speed, scale_var


def scenario_6():  # Scenario number: 6
    width = int(200 / PEDESTRIAN_SIZE)  # as number of blocks
    side = int(1200 / PEDESTRIAN_SIZE)  # as number of blocks
    small_length = int(1000 / PEDESTRIAN_SIZE)  # as number of blocks
    grid_size = (side, side)
    dist_boundary = int(600 / PEDESTRIAN_SIZE)
    pedestrian_locations = []
    obstacle_locations = []
    target_locations = []
    number_of_pedestrians = 20
    is_dijkstra = True
    is_exit = True
    speed = [[13, 20]]
    scale_var = 4

    # Place 20 pedestrian with uniform distribution
    loc_x = np.random.randint(low=side - width, high=side, size=number_of_pedestrians)
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

    return grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra, is_exit, speed, scale_var


def scenario_7():  # Scenario number: 7
    width = int(SCENARIO_7_WIDTH * 100 / PEDESTRIAN_SIZE)  # as number of blocks
    length = int(SCENARIO_7_LENGTH * 100 / PEDESTRIAN_SIZE)  # as number of blocks
    grid_size = (width, length)
    number_of_pedestrians = 50
    obstacle_locations = []
    target_locations = []
    pedestrian_locations = []
    minimum_border_length = int((MINIMUM_BORDER_LENGTH_SCENARIO_7 * 100) / PEDESTRIAN_SIZE)  # 25 blocks
    is_dijkstra = True
    is_exit = True
    speed = [[6,20],[12,20],[16,20],[16,20],[15.5,20],[15,20],[14,20],[13,20],[11,20],[7,20]]*5
    scale_var = 1

    # Place 50 pedestrian with uniform distribution
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

    return grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra, is_exit, speed, scale_var


'''
    Task scenarios
'''


def task_2():  # Scenario number: 2
    grid_size = (50, 50)
    pedestrian_locations = [(24, 4)]
    target_locations = [(24, 24)]
    obstacle_locations = []
    is_dijkstra = False
    is_exit = False
    speed = [[1, 20]]
    scale_var = 1
    return grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra, is_exit, speed, scale_var


def task_3():  # Scenario number: 3
    grid_size = (50, 50)
    pedestrian_locations = [(24, 11), (24, 37), (11, 24), (36, 19),
                            (36, 29)]  # Creating pedestrians in almost circular around the target
    target_locations = [(24, 24)]
    obstacle_locations = []
    is_dijkstra = False
    is_exit = False
    speed = [[1, 20]]
    scale_var = 1
    return grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra, is_exit, speed, scale_var


def task_4_bottleneck():  # Scenario number: 41, as second argument: 0 for disabling Dijkstra, 1 for enabling
    room_side = int(1000 / PEDESTRIAN_SIZE_SCENARIO_4)  # 50 blocks = 10m
    corridor_length = int(500 / PEDESTRIAN_SIZE_SCENARIO_4)  # 25 blocks
    corridor_width = int(
        100 / PEDESTRIAN_SIZE_SCENARIO_4)  # pedestrians are 20cm because we cannot represent 1m with 40cm blocks
    near_corridor = int(450 / PEDESTRIAN_SIZE_SCENARIO_4)
    grid_length = room_side + room_side + corridor_length
    number_of_pedestrians = 150

    grid_size = (room_side, grid_length + 1)  # +1 to properly implement Exit gate
    pedestrian_locations = []
    target_locations = []
    obstacle_locations = []
    is_dijkstra = False
    is_exit = True
    speed = [[1, 20]]
    scale_var = 1

    # Place 150 pedestrians with uniform distribution
    loc_x = np.random.randint(low=0, high=room_side, size=number_of_pedestrians)
    loc_y = np.random.randint(low=0, high=corridor_length, size=number_of_pedestrians)
    for k in range(number_of_pedestrians):
        loc = (loc_x[k], loc_y[k])
        status = True
        while status:
            if loc in pedestrian_locations:
                loc_x_new = np.random.randint(low=0, high=room_side)
                loc_y_new = np.random.randint(low=0, high=corridor_length)
                loc = (loc_x_new, loc_y_new)
            else:
                status = False
        pedestrian_locations.append(loc)

    # Place obstacles for shape of room
    for i in range(near_corridor):
        loc_left_up = (i, room_side)
        loc_left_down = (room_side - 1 - i, room_side)
        loc_right_up = (i, room_side + corridor_length - 1)
        loc_right_down = (room_side - 1 - i, room_side + corridor_length - 1)
        loc_exit_up = (i, grid_length)
        loc_exit_down = (room_side - 1 - i, grid_length)
        obstacle_locations.append(loc_left_up)
        obstacle_locations.append(loc_left_down)
        obstacle_locations.append(loc_right_up)
        obstacle_locations.append(loc_right_down)
        obstacle_locations.append(loc_exit_up)
        obstacle_locations.append(loc_exit_down)

    for i in range(corridor_length):
        loc_up = (near_corridor - 1, room_side + i)
        loc_down = (near_corridor + corridor_width + 1, room_side + i)
        obstacle_locations.append(loc_up)
        obstacle_locations.append(loc_down)

    # Place target (exit)
    for i in range(corridor_width + 1):
        target_locations.append((near_corridor + i, grid_length))

    return grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra, is_exit, speed, scale_var

def task_4_chicken_test():  # Scenario number: 42, as second argument: 0 for disabling Dijkstra, 1 for enabling
    grid_size = (50, 50)
    pedestrian_locations = [(24, 0), (20, 0), (28, 0)]
    target_locations = [(24, 49)]
    obstacle_locations = []
    is_dijkstra = False
    is_exit = True
    speed = [[1, 20]]
    scale_var = 1

    for i in range(15, 35):
        obstacle_locations.append((i, 35))
    for j in range(15, 35):
        obstacle_locations.append((15, j))
        obstacle_locations.append((34, j))

    return grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra, is_exit, speed, scale_var


def create_grid():
    # Get scenario number to create the grid
    f = open(S_FILENAME, "r")
    lines = f.readlines()
    line_movement = False
    density = 1
    scenario = 1
    is_dijkstra_4 = False
    is_exit = False
    is_dijkstra = False
    for line in lines:
        lin = line.strip().split(" ")
        scenario = int(lin[0].strip( ))
        if scenario == 4 and len(lin) > 1:
            density = float(lin[2])
            if lin[1] == "1":
                line_movement = True
        elif (scenario == 41 or scenario == 42) and len(lin) > 1:
            if lin[1] == "1":
                is_dijkstra_4 = True


    if scenario == 1:
        grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra, is_exit, speed, scale_var = scenario_1()
    elif scenario == 4:
        grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra, is_exit, speed, scale_var = scenario_4(line_movement, density)
    elif scenario == 6:
        grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra, is_exit, speed, scale_var = scenario_6()
    elif scenario == 7:
        grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra, is_exit, speed, scale_var = scenario_7()
    elif scenario == 2:
        grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra, is_exit, speed, scale_var = task_2()
    elif scenario == 3:
        grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra, is_exit, speed, scale_var = task_3()
    elif scenario == 41:
        grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra, is_exit, speed, scale_var = task_4_bottleneck()
        is_dijkstra = is_dijkstra_4
    elif scenario == 42:
        grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra, is_exit, speed, scale_var = task_4_chicken_test()
        is_dijkstra = is_dijkstra_4
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

    print("SPEED: ", speed)

    return grid, is_dijkstra, is_exit, speed, scale_var
