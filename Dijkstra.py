import math
import queue

import numpy as np

from Constant import *


class Dijkstra:
    def __init__(self, grid_map, data):
        self.data = data
        self.grid_map = grid_map
        self.__queue = queue.Queue(0)
        self.__visited_map = self.__create_empty_map()
        self.__cost_map = self.__create_empty_map()

        self.__obstacle_cost_max()

    def calculate_cost_map(self):
        print('Starting djikstra algorithm 1')
        for t in self.grid_map.get_target_positions():  # djikstra calculates cost according to all targets
            self.__empty_visited_grid()
            self.__set_visited(t)
            self.__add_neighbour_to_queue_target(t)  # add available neighbours of target to queue
            print('first:', self.__queue.qsize())
            while self.__queue.empty() == False:
                position_tuple = self.__queue.get()  # get the first element in queue. The element is [[first position], [parent position]]
                new_cost = self.__get_cost(position_tuple[1]) + 1  # parents cost + 1
                current_position = position_tuple[0]
                if (self.__get_cost(current_position) != 0 and self.__get_cost(current_position) > new_cost):  # if there exists a cost but new cost is lower.
                    self.__set_cost(current_position, new_cost)
                elif self.__get_cost(current_position) == 0:  # if the cost is 0 then a new cost has not been assigned
                    self.__set_cost(current_position, new_cost)
                self.__add_neighbour_to_queue(position_tuple[0], position_tuple[1])

        print(str(self.__cost_map))
        return self.__cost_map

    def __create_empty_map(self):
        return np.zeros((np.size(self.data, 0), np.size(self.data, 1)))

    def __set_visited(self, position):
        self.visited_map[position[0]][position[1]] = 1

    def __empty_visited_grid(self):
        self.visited_map = np.zeros((np.size(self.data, 0), np.size(self.data, 1)))

    def __add_neighbour_to_queue_target(self, position):  # since targets do not have parents this function is just for the inital target cell
        for d in DIRECTIONS:  # check all directions
            neighbour_x = position[0] + d[0]
            neighbour_y = position[1] + d[1]
            if 0 <= neighbour_x < len(self.data) and 0 <= neighbour_y < len(self.data[0]):  # check if outside the bounds
                n_state = self.grid_map.get_state([neighbour_x, neighbour_y])  # get the state of neighbour
                if (n_state != S_OBSTACLE) and (n_state != S_TARGET):  # check if available cell (not obstacle or not target)
                    self.__queue.put([[neighbour_x, neighbour_y], [position[0], position[1]]])

    def __add_neighbour_to_queue(self, position, parent):
        # print('In regular neighbour add')
        for d in DIRECTIONS:
            neighbour_x = position[0] + d[0]
            neighbour_y = position[1] + d[1]
            if 0 <= neighbour_x and neighbour_x < len(self.data) and 0 <= neighbour_y and neighbour_y < len(self.data[0]):  # check if outside the bounds
                n_state = self.grid_map.get_state([neighbour_x, neighbour_y])  # get the state of neighbour
                if (n_state != S_OBSTACLE) and (n_state != S_TARGET):
                    if self.visited_map[neighbour_x][neighbour_y] == 0:
                        self.__set_visited([neighbour_x, neighbour_y])
                        self.__queue.put([[neighbour_x, neighbour_y], [position[0], position[1]]])

    def __get_cost(self, position):
        return self.__cost_map[position[0]][position[1]]

    def __set_cost(self, position, new_cost):
        self.__cost_map[position[0]][position[1]] = new_cost

    ###THE MAX COST IS HARDCODED; FIND A BETTER WAY
    def __obstacle_cost_max(self):  # make the costs of obstacle int_max
        obstacles = self.grid_map.get_positions_of_given_state(S_OBSTACLE)
        for obs in obstacles:
            self.__set_cost(obs, math.inf)
