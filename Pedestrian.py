from Map import Map
from Constant import *
import numpy as np
import math


class Pedestrian:
    def __init__(self, p_id, ca_model, grid_map, position, desired_speeds=None, corners=None):
        """
        :param p_id: Pedestrian Id
        :param ca_model: CellularModel
        :param grid_map: Map
        :param position: list [x,y]
        :param desired_speeds: list [min, max]
        :param corners:
        """
        self.p_id = p_id
        self.ca_model = ca_model
        self.grid_map = grid_map
        self.position = position
        self.corners = [position, position, position, position]
        self.desired_speeds = desired_speeds if desired_speeds is None else self.get_initial_speeds()
        self.visited_path = [position]

    def get_initial_speeds(self):
        return [min(self.grid_map.width, self.grid_map.height),
                np.sqrt(self.grid_map.width ** 2 + self.grid_map.height ** 2)]

    def tick(self):
        next_position = self.get_best_next_position(1)
        next_state = self.grid_map.get_state(next_position)

        if next_state == S_TARGET:
            self.exit()
        else:
            self.forward(next_position)
            print(next_position)

    def forward(self, next_position):
        self.grid_map.set_state(next_position, S_PEDESTRIAN)
        self.grid_map.set_state(self.position, S_EMPTY)
        self.position = next_position
        self.visited_path.append(next_position)

    def exit(self):
        self.grid_map.set_state(self.position, S_EMPTY)
        self.ca_model.remove_pedestrian(self)

    def get_best_next_position(self, Dijkstra_boolean=0):
        neighbours = self.grid_map.get_neighbours(self.position)
        empty_neighbours = [n for n in neighbours if [S_EMPTY, S_TARGET].count(self.grid_map.get_state(n))]
        if len(empty_neighbours) == 0:
            print("self.position:" + str(self.position) + str(neighbours) + str(empty_neighbours))
            print("MAP")
            print(str(self.grid_map.data))
            return self.position

        # Distance Cost
        if Dijkstra_boolean == 0:
            distance_cost = [self.calculate_distance_cost(n) for n in empty_neighbours]
        else:
            distance_cost = []
            for n in empty_neighbours:
                distance_cost.append(self.grid_map.get_cost(n))
                print(distance_cost)

        # TODO: add interaction cost to distance cost
        # Interaction Cost
        interaction_cost = [self.calculate_interaction_cost(n) for n in empty_neighbours]

        return empty_neighbours[np.argmin(np.array(distance_cost) + np.array(interaction_cost))]

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
        pedestrians = self.grid_map.get_positions_of_given_state(S_PEDESTRIAN)
        pedestrians.remove(self.position)
        total_interaction_cost = 0

        for p in pedestrians:
            cost = 0
            r = np.linalg.norm(np.array(p) - np.array(neighbour_position))
            r_max = 2
            if r < r_max:
                cost = np.exp(r ** 2 - r_max ** 2)
            total_interaction_cost += cost

        return total_interaction_cost
