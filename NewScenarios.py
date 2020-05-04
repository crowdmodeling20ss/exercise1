import ast
import numpy as np
from Constant import *
from CellularModel import CellularModel
from GridCreator import GridCreator
from Map import Map
from Simulation import Simulation

def read_setup_file():
    filename = "new_scenario.txt"
    pedestrian_locations = []
    target_locations = []
    obstacle_locations = []
    grid_size = ()
    is_dijkstra = False

    f = open(filename, "r")
    lines = f.readlines()

    grid_name = "Grid Size"
    pedestrian = "Pedestrian"
    obstacle = "Obstacle"
    target = "Target"
    dijkstra = "Dijkstra"

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


    f.close()
    return grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra


def create_grid_new_scenario():
    grid_size, pedestrian_locations, target_locations, obstacle_locations, is_dijkstra_enabled = read_setup_file()
    grid = np.zeros(grid_size)

    for loc in pedestrian_locations:
        grid[loc] = S_PEDESTRIAN
    for loc in target_locations:
        grid[loc] = S_TARGET
    for loc in obstacle_locations:
        grid[loc] = S_OBSTACLE

    return grid, is_dijkstra_enabled


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
