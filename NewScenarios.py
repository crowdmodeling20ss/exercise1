import ast
import numpy as np
from Constant import *
from CellularModel import CellularModel
from GridCreator import GridCreator
from Map import Map
from PredefinedSimulation import PredefinedSimulation
from Simulation import Simulation

def read_setup_file():
    filename = "new_scenario.txt"
    pedestrian_locations = []
    target_locations = []
    obstacle_locations = []
    grid_size = ()
    is_dijkstra = False
    is_obstacle_avoidance = False
    speed_arr = []

    f = open(filename, "r")
    lines = f.readlines()

    grid_name = "Grid Size"
    pedestrian = "Pedestrian"
    obstacle = "Obstacle"
    target = "Target"
    dijkstra = "Dijkstra"
    obstacle_avoidance = "ObstacleAvoidance"
    speed = "Speed"    # Scale variable not added

    # TODO: add speed

    for line in lines:
        setup = line.strip().split("=")
        setup[0] = setup[0].strip().lower()
        setup[1] = setup[1].strip().capitalize()
        obj = ast.literal_eval(setup[1])

        if setup[0] == grid_name.lower():
            grid_size = obj
        elif setup[0] == pedestrian.lower():
            pedestrian_locations = obj
        elif setup[0] == target.lower():
            target_locations = obj
        elif setup[0] == obstacle.lower():
            obstacle_locations = obj
        elif setup[0] == dijkstra.lower():
            is_dijkstra = obj
        elif setup[0] == obstacle_avoidance.lower():
            is_obstacle_avoidance = obj
        elif setup[0] == speed.lower():
            speed_arr = obj


    f.close()
    return grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra, is_obstacle_avoidance, speed_arr


def create_grid_new_scenario():
    grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra_enabled, is_obstacle_avoidance, speed_arr = read_setup_file()
    grid = np.zeros(grid_size)
    num_pedestrian = len(pedestrian_locations)
    print("num pedestrian: ", num_pedestrian)
    for loc in pedestrian_locations:
        grid[loc] = S_PEDESTRIAN
    for loc in target_locations:
        grid[loc] = S_TARGET
    for loc in obstacle_locations:
        grid[loc] = S_OBSTACLE

    return grid, is_dijkstra_enabled, is_obstacle_avoidance, speed_arr, num_pedestrian

'''
def main():
    ## New scenario from user
    IS_DIJKSTRA_ENABLED = True
    IS_PEDESTRIAN_EXIT = True
    SPEED_OF_PEDESTRIANS = [1, 20]
    SPEED_PER_PEDESTRIAN_IS_ON = False
    SHOW_COST_MAP = True
    SHOW_SPEED_GRAPH = True

    predefinedSimulation = PredefinedSimulation(IS_DIJKSTRA_ENABLED,
                                                IS_PEDESTRIAN_EXIT,
                                                SPEED_OF_PEDESTRIANS,
                                                SPEED_PER_PEDESTRIAN_IS_ON,
                                                SHOW_COST_MAP,
                                                SHOW_SPEED_GRAPH)
    predefinedSimulation.run()

if __name__ == '__main__':
    main()
'''