import concurrent.futures
import math

import numpy as np

import Util
from Constant import *


class Pedestrian:
    def __init__(self, p_id, ca_model, grid_map, position, desired_speeds=None, corners=None, r_max=0,
                 is_pedestrian_exit=True, is_dijkstra_enabled=True):
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
        self.corners = corners  # left-top, right-top, left-bottom, right-bottom
        self.desired_speeds = desired_speeds if desired_speeds != None else self.get_initial_speeds()
        self.size = self.get_size()  # This is to understand how many blocks does the ped. has in ints width/height
        self.r_max = r_max
        self.is_dijkstra_enabled = is_dijkstra_enabled
        self.is_pedestrian_exit = is_pedestrian_exit
        self.p_state = P_INIT
        self.total_path = 0.0
        self.age = 0.0
        self.visited_path = [position]
        self.path_cost_history = []
        self.distance_cost_history = []
        self.interaction_cost_history = []
        # self.last_cost = math.inf

    def get_size(self):
        # print("Corners:", self.corners)
        # print("Get Size:", self.corners[1][1] - self.corners[0][1])
        return abs(self.corners[0][1] - self.corners[1][1]) + 1  ###+1 or NOT

    def get_initial_speeds(self):
        return [self.get_size(), np.sqrt(self.get_size() ** 2 + self.get_size() ** 2)]

    def tick(self):
        next_position = self.get_best_next_position(1)
        next_state = self.grid_map.get_state(next_position)

        if next_state == S_TARGET:
            self.exit()
        else:
            self.forward(next_position)
            # print(next_position)

    def tick_multicell(self):
        self.age += 1.0
        while self.p_state != P_EXIT and self.velocity() < self.desired_speeds[0]:
            previous_position = np.array(self.position)
            self.get_best_next_position_Multicell()
            if (len(self.distance_cost_history) > 0 and self.distance_cost_history[len(self.distance_cost_history) - 1] == [-2, -2, -2, -2]):
                print("Stuck case. # Ped:" + str(self.p_id))
                break
            distance = np.linalg.norm(np.array(self.position) - previous_position)
            self.total_path += distance

        self.visited_path.append(self.position)

    def velocity(self):
        return self.total_path / self.age

    def forward(self, next_position):
        self.grid_map.set_state(next_position, S_PEDESTRIAN)
        self.grid_map.set_state(self.position, S_EMPTY)
        self.position = next_position
        self.visited_path.append(next_position)

    def exit(self):
        self.p_state = P_EXIT
        self.grid_map.set_state(self.position, S_EMPTY)
        self.ca_model.remove_pedestrian(self)

    ###TODO: Make this function make multi-cell decision
    def get_best_next_position_Multicell(self):
        # print("get best next position size", self.size)

        neighbour_costs = self.grid_map.get_neighbours_multicell(self.corners, self.size)
        self.distance_cost_history.append(neighbour_costs.copy())
        ## we will get a vector with costs of [top, right, bottom. left]
        ##The cost of -1 means that the neighbor of that side has a target
        ##The cost of -2 means that the neighbor of that side has a obstacle or ped. so we cant move there.

        empty_neighbours = [n for n in neighbour_costs if [-1, -2].count(n) == 0]
        if len(empty_neighbours) == 0:
            return

        ##The interaction cost is not added yet.
        if self.pedestrian_end_check(neighbour_costs) == True:
            self.exit_multicell()
        else:
            if self.is_dijkstra_enabled == False:
                s = math.inf
                b = -1
                i_costs = []
                for i in range(len(neighbour_costs)):
                    interaction_value = self.interaction_cost_multicell(i)
                    i_costs.append(interaction_value)
                    if neighbour_costs[i] != -1 and neighbour_costs[i] != -2 and s > (neighbour_costs[i] + interaction_value):
                        
                        s = neighbour_costs[i] + interaction_value
                        b = i
                self.interaction_cost_history.append(i_costs)

                if b != -1:
                    self.forward_multicell(b)
                return
            best = self.calculate_interaction_cost_multicell(neighbour_costs)
            if best != -1:  # There is a possible way
                # if self.last_cost < cost:
                #    return
                # else:
                self.forward_multicell(best)

    def calculate_interaction_cost_multicell(self, neighbour_costs):
        best = -1
        cost = math.inf
        normalization_var = np.amax(neighbour_costs) / 2 * 3
        interaction_cost_tmp = []  # DEBUG PURPOSE
        for i in range(4):  # check all sides
            if neighbour_costs[i] != -2:
                # print("##################")
                # print("Direction:", i)
                # print("Cost before adding interaction_cost", neighbour_costs[i])
                # print("The Cost", self.interaction_cost_multicell(i))
                interaction_cost = self.interaction_cost_multicell(i)  # * normalization_var
                neighbour_costs[i] += interaction_cost
                interaction_cost_tmp.append(interaction_cost)  # DEBUG PURPOSE
                # print("Cost after adding interaction_cost", neighbour_costs[i])

                if cost > neighbour_costs[i]:
                    cost = neighbour_costs[i]
                    best = i
            else:
                interaction_cost_tmp.append(0)  # DEBUG PURPOSE
        self.interaction_cost_history.append(interaction_cost_tmp)  # DEBUG PURPOSE

        return best

    def exit_multicell(self):
        self.p_state = P_EXIT
        if self.is_pedestrian_exit:
            self.grid_map.set_state_block(self.corners, self.size, S_EMPTY2)
            self.ca_model.remove_pedestrian(self)
            print("Removed Pedestrian p_id:" + str(self.p_id) + " center:" + str(self.position))

    def pedestrian_end_check(self, n_costs):
        for i in n_costs:
            if i == -1:
                ###end the pedestrian
                return True
        return False

    def interaction_cost_multicell(self, direction):
        neighbour_center = []
        if direction == D_TOP:  # average of left top corner and right top with x values -1
            neighbour_center = [(self.corners[0][0] + self.corners[1][0]) / 2 - 1,
                                (self.corners[0][1] + self.corners[1][1]) / 2]
        elif direction == D_RIGHT:
            neighbour_center = [(self.corners[1][0] + self.corners[3][0]) / 2,
                                (self.corners[1][1] + self.corners[3][1]) / 2 + 1]
        elif direction == D_BOTTOM:
            neighbour_center = [(self.corners[2][0] + self.corners[3][0]) / 2 + 1,
                                (self.corners[2][1] + self.corners[3][1]) / 2]
        elif direction == D_LEFT:
            neighbour_center = [(self.corners[0][0] + self.corners[2][0]) / 2,
                                (self.corners[0][1] + self.corners[2][1]) / 2 - 1]
        cost = self.interaction_cost_multicell_calculator(neighbour_center)
        # print("Interaction Cost:", cost)
        return cost

    def interaction_cost_multicell_calculator(self, neighbour_position):
        cost = []
        for p in self.ca_model.pedestrians:
            if p != self:
                center = p.position
                r = np.linalg.norm(np.array(center) - np.array(neighbour_position))
                if r < self.r_max:
                    cost.append(np.exp(1 / (r ** 2 - self.r_max ** 2)))
        if len(cost) == 0: return 0
        return sum(cost) / len(cost) * 1.0

    def threaded_interaction_cost_multicell_calculator(self, direction, neighbour_position):
        total_cost = 0
        print("The center List:", [p.position for p in self.ca_model.pedestrians])
        for p in self.ca_model.pedestrians:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # future = executor.submit(foo, 'world!')
                if p != self:
                    center = p.position
                    print("HI!!!!")
                    future = executor.submit(self.thread_interaction, center, neighbour_position, self.r_max)
                    # print("Thread Result:", future.result())
                    total_cost += future.result()

                    # r = np.linalg.norm(np.array(center) - np.array(neighbour_position))
                    # if r < self.r_max:
                    # total_cost = np.exp(r ** 2 - self.r_max ** 2)
        return total_cost

    def thread_interaction(self, center, neighbour_position, r_max):
        r = np.linalg.norm(np.array(center) - np.array(neighbour_position))
        # print("R is:", r)
        if r < r_max:
            # print("center:", center)
            # print("neighbour position", neighbour_position)
            # print("Result is: ", np.exp(r ** 2 - r_max ** 2) + self.size)
            return (np.exp(r ** 2 - r_max ** 2) + self.size)
        else:
            return 0

    def forward_multicell(self, direction):  ##move size many blocks into the direction.
        #####UPDATE CORNERS: 
        if direction == D_TOP:  # row -1
            self.grid_map.set_state_multicell(self.corners[2], D_BOTTOM, self.size,
                                              S_EMPTY2)  # Empty the existing cells that move
            self.grid_map.set_state_multicell([self.corners[0][0] - 1, self.corners[0][1]], D_TOP, self.size,
                                              S_PEDESTRIAN)
            for i in range(4):
                self.corners[i] = [self.corners[i][0] - 1, self.corners[i][1]]
        elif direction == D_RIGHT:  # column +1
            self.grid_map.set_state_multicell(self.corners[0], D_LEFT, self.size,
                                              S_EMPTY2)  # Empty the existing cells that move
            self.grid_map.set_state_multicell([self.corners[1][0], self.corners[1][1] + 1], D_RIGHT, self.size,
                                              S_PEDESTRIAN)
            for i in range(4):
                # print("error", self.corners[i][1])
                self.corners[i] = [self.corners[i][0], self.corners[i][1] + 1]
        elif direction == D_BOTTOM:  # row +1
            self.grid_map.set_state_multicell(self.corners[0], D_TOP, self.size,
                                              S_EMPTY2)  # Empty the existing cells that move
            self.grid_map.set_state_multicell([self.corners[2][0] + 1, self.corners[2][1]], D_BOTTOM, self.size,
                                              S_PEDESTRIAN)
            for i in range(4):
                self.corners[i] = [self.corners[i][0] + 1, self.corners[i][1]]
        elif direction == D_LEFT:  # column -1
            self.grid_map.set_state_multicell(self.corners[1], D_RIGHT, self.size,
                                              S_EMPTY2)  # Empty the existing cells that move
            self.grid_map.set_state_multicell([self.corners[0][0], self.corners[0][1] - 1], D_LEFT, self.size,
                                              S_PEDESTRIAN)
            for i in range(4):
                self.corners[i] = [self.corners[i][0], self.corners[i][1] - 1]

        self.position = Util.calculate_center(self.corners)
        self.path_cost_history.append(self.position)
        self.p_state = P_WALKING

    def get_best_next_position(self, Dijkstra_boolean=0):
        neighbours = self.grid_map.get_neighbours(self.position)
        empty_neighbours = [n for n in neighbours if [S_EMPTY, S_EMPTY2, S_TARGET].count(self.grid_map.get_state(n))]
        if len(empty_neighbours) == 0:
            # print("self.position:" + str(self.position) + str(neighbours) + str(empty_neighbours))
            # print("MAP")
            # print(str(self.grid_map.data))
            return self.position

        # Distance Cost
        if Dijkstra_boolean == 0:
            distance_cost = [self.calculate_distance_cost(n) for n in empty_neighbours]
        else:
            distance_cost = []
            for n in empty_neighbours:
                distance_cost.append(self.grid_map.get_cost(n))
                # print(distance_cost)

        # TODO: add interaction cost to distance cost
        # Interaction Cost
        interaction_cost = [self.calculate_interaction_cost(n) for n in empty_neighbours]

        return empty_neighbours[np.argmin(np.array(distance_cost) + np.array(interaction_cost))]

    # TODO: this can be received from Map.cost_map
    def calculate_distance_cost(self, neighbour_position):
        min_distance = math.inf
        ns = self.grid_map.get_target_positions()
        nearest_row = math.inf
        nearest_column = math.inf
        for t in ns:
            if abs(t[0] - neighbour_position[0]) < nearest_row:
                nearest_row = t[0]
            if abs(t[1] - neighbour_position[1]) < nearest_column:
                nearest_column = t[1]
        min_distance = np.linalg.norm(np.array([nearest_row, nearest_column]) - np.array(neighbour_position))
        # normalize
        min_distance = (min_distance * 1.0) / np.linalg.norm(
            np.array([0, 0]) - np.array([len(self.grid_map.data) - 1, len(self.grid_map.data[0]) - 1]))
        ''' DO NOT CALCULATE NORM EACH TIME
        for t in self.grid_map.get_target_positions():
            distance = np.linalg.norm(np.array(t) - np.array(neighbour_position))
            if distance < min_distance:
                min_distance = distance
        '''
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
