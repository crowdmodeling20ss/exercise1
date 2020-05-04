import concurrent.futures
import math

import numpy as np

from Constant import *
from Dijkstra import Dijkstra


class Map:
    """

    :param width: of the cell in cm in the given 'data'.
    :type width: int
    :param height of the cell in cm in the given 'data'.
    :type height: int
    :param data MXN numpy array
    """

    def __init__(self, width, height, data, corners, is_dijkstra_enabled=True):
        self.id = 0
        self.width = width
        self.height = height
        self.data = data
        self.corners = corners
        self.is_dijkstra_enabled = is_dijkstra_enabled
        self.cost_map = self.calculate_cost_map()

    def set_state(self, position, state):
        self.data[position[0]][position[1]] = state

    def get_state(self, position):
        return self.data[position[0]][position[1]]

    # state int = {S_EMPTY, S_PEDESTRIAN, S_OBSTACLE, S_TARGET}
    def get_positions_of_given_state(self, state):
        positions = []
        for x in range(0, len(self.data)):
            for y in range(0, len(self.data[0])):
                if self.data[x][y] == state:
                    positions.append([x, y])
        return positions

    def get_target_positions(self):
        return self.get_positions_of_given_state(S_TARGET)

    def get_neighbours(self, position):
        available_neighbours = []
        for d in DIRECTIONS:
            neighbour_x = position[0] + d[0]
            neighbour_y = position[1] + d[1]

            if 0 <= neighbour_x < len(self.data) and 0 <= neighbour_y < len(self.data[0]):
                available_neighbours.append([neighbour_x, neighbour_y])

        return available_neighbours

    def neighbour_check_top(self, corners, size):
        direction_cost = 0
        if 0 <= (corners[0][0] - 1) < len(self.data):
            for i in range(size):
                curr_point = self.data[corners[0][0] - 1][corners[0][1] + i]
                if curr_point == S_TARGET:
                    direction_cost = -1
                    return direction_cost
                    ##EXIT FUNCTION, found the target
                elif curr_point == S_OBSTACLE or curr_point == S_PEDESTRIAN:
                    direction_cost = -2  # invalid neighbour
                    return direction_cost
                    # Check if break works:
                else:
                    direction_cost += self.cost_map[corners[0][0] - 1][corners[0][1] + i]
            return direction_cost / 4.0
        else:
            direction_cost = -2  # invalid neighbour
            return direction_cost

    def neighbour_check_right(self, corners, size):
        direction_cost = 0
        if 0 <= (corners[1][1] + 1) < len(self.data[0]):
            for i in range(size):
                curr_point = self.data[corners[1][0] + i][corners[1][1] + 1]
                if curr_point == S_TARGET:
                    direction_cost = -1
                    return direction_cost
                    ##EXIT FUNCTION, found the target
                elif curr_point == S_OBSTACLE or curr_point == S_PEDESTRIAN:
                    direction_cost = -2  # invalid neighbour
                    return direction_cost

                else:
                    direction_cost += self.cost_map[corners[1][0] + i][corners[1][1] + 1]
            return direction_cost / 4.0
        else:
            direction_cost = -2  # invalid neighbour
            return direction_cost

    def neighbour_check_bottom(self, corners, size):
        direction_cost = 0
        if 0 <= (corners[2][0] + 1) < len(self.data):
            for i in range(size):
                curr_point = self.data[corners[2][0] + 1][corners[2][1] + i]
                if curr_point == S_TARGET:
                    direction_cost = -1
                    return direction_cost
                    ##EXIT FUNCTION, found the target
                elif curr_point == S_OBSTACLE or curr_point == S_PEDESTRIAN:
                    direction_cost = -2  # invalid neighbour
                    # Check if break works:
                    return direction_cost
                else:
                    direction_cost += self.cost_map[corners[2][0] + 1][corners[2][1] + i]
            return direction_cost / 4.0
        else:
            direction_cost = -2  # invalid neighbour
            return direction_cost

    def neighbour_check_left(self, corners, size):
        direction_cost = 0
        if 0 <= (corners[0][1] - 1) < len(self.data[0]):
            for i in range(size):
                curr_point = self.data[corners[0][0] + i][corners[0][1] - 1]
                if curr_point == S_TARGET:
                    direction_cost = -1
                    return direction_cost
                    ##EXIT FUNCTION, found the target
                elif curr_point == S_OBSTACLE or curr_point == S_PEDESTRIAN:
                    direction_cost = -2  # invalid neighbour
                    # Check if break works:
                    return direction_cost
                else:
                    direction_cost += self.cost_map[corners[0][0] + i][corners[0][1] - 1]
            return direction_cost / 4.0
        else:
            direction_cost = -2  # invalid neighbour
            return direction_cost

    def thread_function(self, corners, size, direction):
        if direction == 0:
            return self.neighbour_check_top(corners, size)
        elif direction == 1:
            return self.neighbour_check_right(corners, size)
        elif direction == 2:
            return self.neighbour_check_bottom(corners, size)
        elif direction == 3:
            return self.neighbour_check_left(corners, size)

    ##TODO: MULTICELL GET NEIGHBOR WITH COST
    def get_neighbours_multicell(self, corners, size):
        direction_cost = [0, 0, 0, 0]  # costs for top, right, bottom, left direction

        if self.is_dijkstra_enabled:
            for i in range(4):
                # print("i", i)
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                    # future = executor.submit(foo, 'world!')
                    future = executor.submit(self.thread_function, corners, size, i)
                    direction_cost[i] = future.result()
            # direction_cost[D_TOP] = self.neighbour_check_top(corners, size)
            # direction_cost[D_RIGHT] = self.neighbour_check_right(corners, size)
            # direction_cost[D_BOTTOM] = self.neighbour_check_bottom(corners, size)
            # direction_cost[D_LEFT] = self.neighbour_check_left(corners, size)

            # print("The direction costs: ", direction_cost)
            return direction_cost
        else:
            for direction in range(4):
                direction_cost[direction] = self.ddd(direction, corners, size)

            return direction_cost

    def ddd(self, direction, corners, size):
        direction_cost = 0
        direction_cost_size = 0
        if direction == D_TOP:
            if 0 <= (corners[0][0] - 1) < len(self.data):
                for i in range(size):
                    curr_point = self.data[corners[0][0] - 1][corners[0][1] + i]
                    if curr_point == S_TARGET:
                        direction_cost = -1
                        return direction_cost
                        ##EXIT FUNCTION, found the target
                    elif curr_point == S_OBSTACLE or curr_point == S_PEDESTRIAN:
                        direction_cost = -2  # invalid neighbour
                        return direction_cost
                        # Check if break works:
                    else:
                        direction_cost += self.calculate_distance_cost([corners[0][0] - 1, corners[0][1] + i])
                        direction_cost_size += 1
                return direction_cost / float(direction_cost_size)
            else:
                direction_cost = -2  # invalid neighbour
                return direction_cost
        elif direction == D_RIGHT:
            if 0 <= (corners[1][1] + 1) < len(self.data[0]):
                for i in range(size):
                    curr_point = self.data[corners[1][0] + i][corners[1][1] + 1]
                    if curr_point == S_TARGET:
                        direction_cost = -1
                        return direction_cost
                        ##EXIT FUNCTION, found the target
                    elif curr_point == S_OBSTACLE or curr_point == S_PEDESTRIAN:
                        direction_cost = -2  # invalid neighbour
                        return direction_cost

                    else:
                        direction_cost += self.calculate_distance_cost([corners[1][0] + i, corners[1][1] + 1])
                        direction_cost_size += 1
                return direction_cost / float(direction_cost_size)
            else:
                direction_cost = -2  # invalid neighbour
                return direction_cost
        elif direction == D_BOTTOM:
            if 0 <= (corners[2][0] + 1) < len(self.data):
                for i in range(size):
                    curr_point = self.data[corners[2][0] + 1][corners[2][1] + i]
                    if curr_point == S_TARGET:
                        direction_cost = -1
                        return direction_cost
                        ##EXIT FUNCTION, found the target
                    elif curr_point == S_OBSTACLE or curr_point == S_PEDESTRIAN:
                        direction_cost = -2  # invalid neighbour
                        # Check if break works:
                        return direction_cost
                    else:
                        direction_cost += self.calculate_distance_cost([corners[2][0] + 1, corners[2][1] + i])
                        direction_cost_size += 1
                return direction_cost / float(direction_cost_size)
            else:
                direction_cost = -2  # invalid neighbour
                return direction_cost
        elif direction == D_LEFT:
            if 0 <= (corners[0][1] - 1) < len(self.data[0]):
                for i in range(size):
                    curr_point = self.data[corners[0][0] + i][corners[0][1] - 1]
                    if curr_point == S_TARGET:
                        direction_cost = -1
                        return direction_cost
                        ##EXIT FUNCTION, found the target
                    elif curr_point == S_OBSTACLE or curr_point == S_PEDESTRIAN:
                        direction_cost = -2  # invalid neighbour
                        # Check if break works:
                        return direction_cost
                    else:
                        direction_cost += self.calculate_distance_cost([corners[0][0] + i, corners[0][1] - 1])
                        direction_cost_size += 1
                return direction_cost / float(direction_cost_size)
            else:
                direction_cost = -2  # invalid neighbour
                return direction_cost

    def set_state_multicell(self, pos, direction, size, block_type):  # to change a row or column
        cell_x = pos[0]
        cell_y = pos[1]
        # print("CELL X", cell_x)
        # print("CELL Y", cell_y)
        # print("Direction", direction)
        # print("size", size)
        # print("block type", block_type)
        if direction == D_TOP:  # top
            for i in range(size):
                self.data[cell_x][cell_y + i] = block_type
        elif direction == D_RIGHT:  #
            for i in range(size):
                self.data[cell_x + i][cell_y] = block_type
        elif direction == D_BOTTOM:
            for i in range(size):
                self.data[cell_x][cell_y + i] = block_type
        elif direction == D_LEFT:
            # print("size", size)
            # print("pos", pos)
            for i in range(size):
                self.data[cell_x + i][cell_y] = block_type

    def set_state_block(self, corners, size, block_type):  # to destroy pedestrians.
        for r in range(size):
            for c in range(size):
                self.data[corners[0][0] + r][corners[0][1] + c] = block_type
                # print("The new value is :", self.data[corners[0][0]+r][corners[0][1]+c])

    # TODO:
    """
    Calculate cost starting from target and save costs in cost_map 
    """

    def calculate_cost_map(self):
        if self.is_dijkstra_enabled:
            return Dijkstra(self, self.data).calculate_cost_map()
        return 0

    def get_cost(self, position):
        return self.cost_map[position[0]][position[1]]

    def calculate_distance_cost(self, neighbour_position):
        min_distance = math.inf
        """
        ns = self.get_target_positions()
        nearest_row=math.inf
        nearest_column=math.inf
        for t in ns:
            if abs(t[0]-neighbour_position[0]) < nearest_row:
                nearest_row = t[0]
            if abs(t[1]-neighbour_position[1]) < nearest_column:
                nearest_column = t[1]
        min_distance = np.linalg.norm(np.array([nearest_row, nearest_column]) - np.array(neighbour_position))
        # normalize
        min_distance = (min_distance*1.0) / np.linalg.norm(np.array([0,0]) - np.array([0, len(self.data[0])-1]))
        """

        #''' DO NOT CALCULATE NORM EACH TIME
        for t in self.get_target_positions():
            distance = np.linalg.norm(np.array(t) - np.array(neighbour_position))
            if distance < min_distance:
                min_distance = distance
        #'''
        min_distance = (min_distance * 1.0) / np.linalg.norm(np.array([0, 0]) - np.array([0, len(self.data[0]) - 1]))
        return min_distance