from Constant import *
from Dijkstra import Dijkstra
import math


class Map:
    """

    :param width: of the cell in cm in the given 'data'.
    :type width: int
    :param height of the cell in cm in the given 'data'.
    :type height: int
    :param data MXN numpy array
    """

    def __init__(self, width, height, data, corners):
        self.id = 0
        self.width = width
        self.height = height
        self.data = data
        self.cost_map = self.calculate_cost_map()
        self.corners = corners

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


    ##TODO: MULTICELL GET NEIGHBOR WITH COST
    def get_neighbours_multicell(self, corners, size):

        direction_cost = [0,0,0,0] #costs for top, right, bottom, left direction

        
        #for top side, calculate from top-left-corner
        if 0 <= (corners[0][0] -1) <= len(self.data):
            print(size)
            for i in range(size):
                curr_point = self.data[corners[0][0]-1][corners[0][1]+i]
                if curr_point == S_TARGET:
                    direction_cost[D_TOP] = -1
                    return
                    ##EXIT FUNCTION, found the target
                elif curr_point == S_OBSTACLE or curr_point == S_PEDESTRIAN:
                    direction_cost[D_TOP] = -2#invalid neighbour
                    #Check if break works:
                    break
                else:
                    direction_cost[D_TOP] += self.cost_map[corners[0][0]-1][corners[0][1]+i]
        else:
            direction_cost[D_TOP] = -2 #invalid neighbour
        #for right side, calculate from top-right-corner
        if 0 <= (corners[1][1] + 1) <= len(self.data):
            for i in range(size):
                curr_point = self.data[corners[1][0] + i][corners[1][1]+1]
                if curr_point == S_TARGET:
                    direction_cost[D_RIGHT] = -1
                    return
                    ##EXIT FUNCTION, found the target
                elif curr_point == S_OBSTACLE or curr_point == S_PEDESTRIAN:
                    direction_cost[D_RIGHT] = -2#invalid neighbour
                    #Check if break works:
                    break
                else:
                    direction_cost[D_RIGHT] += self.cost_map[corners[1][0]+i][corners[1][1]+1]
        else:
            direction_cost[D_RIGHT] = -2 #invalid neighbour

        #for bottom side, calculate from bottom-left
        if 0 <= (corners[2][0] +1) <= len(self.data):
            for i in range(size):
                curr_point = self.data[corners[2][0]+1][corners[2][1]+i]
                if curr_point == S_TARGET:
                    direction_cost[D_BOTTOM] = -1
                    return
                    ##EXIT FUNCTION, found the target
                elif curr_point == S_OBSTACLE or curr_point == S_PEDESTRIAN:
                    direction_cost[D_BOTTOM] = -2#invalid neighbour
                    #Check if break works:
                    break
                else:
                    direction_cost[D_BOTTOM] += self.cost_map[corners[2][0]+1][corners[2][1]+i]
        else:
            direction_cost[D_BOTTOM] = -2 #invalid neighbour

        #for left side, calculate from top-left
        if 0 <= (corners[0][1] -1) <= len(self.data):
            for i in range(size):
                curr_point = self.data[corners[0][0]+i][corners[0][1]-1]
                if curr_point == S_TARGET:
                    direction_cost[D_LEFT] = -1
                    return
                    ##EXIT FUNCTION, found the target
                elif curr_point == S_OBSTACLE or curr_point == S_PEDESTRIAN:
                    direction_cost[D_LEFT] = -2#invalid neighbour
                    #Check if break works:
                    break
                else:
                    direction_cost[D_LEFT] += self.cost_map[corners[0][0]+i][corners[0][1]-1]
        else:
            direction_cost[D_LEFT] = -2 #invalid neighbour
        
        return direction_cost
        
    def set_state_multicell(self, pos, direction, size, block_type): # to change a row or column
        cell_x = pos[0]
        cell_y = pos[1]
        if direction == D_TOP:#top
            for i in range(size):
                self.data[cell_x][cell_y+i] = block_type
        elif direction == D_RIGHT:#
            for i in range(size):
                self.data[cell_x+i][cell_y] = block_type
        elif direction == D_BOTTOM:
            for i in range(size):
                self.data[cell_x][cell_y+i] = block_type
        elif direction == D_LEFT:
            for i in range(size):
                self.data[cell_x+i][cell_y] = block_type

    def set_state_block(self, corners, size, block_type): #to destroy pedestrians.
        for r in range(size):
            for c in range(size):
                self.data[corners[0][0]+r][corners[0][0]+c] = block_type

    # TODO:
    """
    Calculate cost starting from target and save costs in cost_map 
    """

    def calculate_cost_map(self, djiksta_boolean=1):
        if (djiksta_boolean == 1):
            return Dijkstra(self, self.data).calculate_cost_map()
        return 0

    def get_cost(self, position):
        return self.cost_map[position[0]][position[1]]
