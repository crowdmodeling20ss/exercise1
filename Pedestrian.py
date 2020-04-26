from Map import Map
from Constant import *
import numpy as np
import math


class Pedestrian:
    """
    :param grid_map: Map
    :type grid_map: Map
    :param position: x and y of current cell of the pedestrian in the map. [min, max]
    :type position: list
    :param desired_speeds: Desired speed of pedestrian in cm/s [min, max]
    :type desired_speeds: list
    """

    def __init__(self, grid_map, position, desired_speeds=None):
        self.grid_map = grid_map
        self.position = position
        self.desired_speeds = desired_speeds if desired_speeds is None else self.get_initial_speeds()
        self.visited_path = []

    def get_initial_speeds(self):
        return [min(self.grid_map.width, self.grid_map.height),
                np.sqrt(self.grid_map.width ** 2 + self.grid_map.height ** 2)]

    def tick(self):
        neighbours = self.grid_map.get_neighbours(self.position)

        # TODO we can find next position Dijkstra instead of this function
        next_position = self.get_best_next_position(neighbours, 1)
        next_state = self.grid_map.get_state(next_position)

        if not next_state == S_TARGET:
            self.grid_map.set_state(next_position, S_PEDESTRIAN)
            self.grid_map.set_state(self.position, S_EMPTY)
            self.position = next_position
            print(next_position)

    def get_best_next_position(self, neighbours, Dijkstra_boolean = 0):
        # Distance Cost
        if Dijkstra_boolean == 0:
            distance_cost = [self.calculate_distance_cost(n) for n in neighbours]
            # Interaction Cost
            interaction_cost = [self.calculate_interaction_cost(n) for n in neighbours]
            return neighbours[np.argmin(distance_cost)]
        else:
            distance_cost = []
            for n in neighbours:
                distance_cost.append(self.grid_map.get_cost(n))
                #interaction_cost = [self.calculate_interaction_cost(n) for n in neighbours]
                print(distance_cost)
            return neighbours[np.argmin(distance_cost)]
        # TODO: add interaction cost to distance cost

        

    # TODO: this can be received from Map.cost_map
    def calculate_distance_cost(self, neighbour_position):
        min_distance = math.inf
        for t in self.grid_map.get_target_positions():
            distance = np.linalg.norm(np.array(t) - np.array(neighbour_position))
            if distance < min_distance:
                min_distance = distance
        return min_distance

    # TODO: Calculate interaction cost for each neighbour position to closest pedestrian or obstacle
    def calculate_interaction_cost(self, neighbour_position):
        return 0
