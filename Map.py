from Constant import *
import numpy as np
import queue

class Map:
    """

    :param width: of the cell in cm in the given 'data'.
    :type width: int
    :param height of the cell in cm in the given 'data'.
    :type height: int
    :param data MXN numpy array
    """

    def __init__(self, width, height, data):
        self.id = 0
        self.width = width
        self.height = height
        self.data = data
        self.queue = queue.Queue(0)
        self.cost_map = self.create_empty_map()
        self.visited_map = self.create_empty_map()
        self.iter = 0

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

    # TODO:
    """
    Calculate cost starting from target and save costs in cost_map 
    """
    def create_empty_map(self): #return empty cost map with same size as data matrix
        return np.zeros((np.size(self.data, 0), np.size(self.data, 1))) 

    def calculate_cost_map(self, djiksta_boolean = 1):
        if djiksta_boolean == 1:
            print('Starting djikstra algorithm 1')
            for t in self.get_target_positions(): #djikstra calculates cost according to all targets
                self.empty_visited_grid()
                self.set_visited(t)
                self.add_neighbour_to_queue_target(t)#add available neighbours of target to queue
                print('first:', self.queue.qsize())
                while self.queue.empty() == False:
                    position_tuple = self.queue.get()#get the first element in queue. The element is [[first position], [parent position]]
                    new_cost = self.get_cost(position_tuple[1]) + 1 #parents cost + 1
                    current_position = position_tuple[0]
                    if (self.get_cost(current_position) != 0 and self.get_cost(current_position) > new_cost): #if there exists a cost but new cost is lower.
                        self.set_cost(current_position, new_cost)
                    elif self.get_cost(current_position) == 0: #if the cost is 0 then a new cost has not been assigned
                        self.set_cost(current_position, new_cost)
                    self.add_neighbour_to_queue(position_tuple[0], position_tuple[1])
    
    def set_visited(self, position):
        self.visited_map[position[0]][position[1]] = 1

    def empty_visited_grid(self):
        self.visited_map = np.zeros((np.size(self.data, 0), np.size(self.data, 1)))  
    
    def get_cost(self, position):
        return self.cost_map[position[0]][position[1]]

    def set_cost(self, position, new_cost):
        self.cost_map[position[0]][position[1]] = new_cost

    def add_neighbour_to_queue_target(self, position):#since targets do not have parents this function is just for the inital target cell
        for d in DIRECTIONS:#check all directions
            neighbour_x = position[0] + d[0]
            neighbour_y = position[1] + d[1]
            if 0 <= neighbour_x < len(self.data) and 0 <= neighbour_y < len(self.data[0]): #check if outside the bounds
                n_state = self.get_state([neighbour_x, neighbour_y]) #get the state of neighbour    
                if (n_state != S_OBSTACLE) and (n_state != S_TARGET): #check if available cell (not obstacle or not target)
                    self.queue.put([[neighbour_x, neighbour_y],[position[0], position[1]]])

    def add_neighbour_to_queue(self, position, parent):
        #print('In regular neighbour add')
        for d in DIRECTIONS:
            neighbour_x = position[0] + d[0]
            neighbour_y = position[1] + d[1]
            if 0 <= neighbour_x and neighbour_x < len(self.data) and 0 <= neighbour_y and neighbour_y < len(self.data[0]): #check if outside the bounds
                n_state = self.get_state([neighbour_x, neighbour_y]) #get the state of neighbour
                if (n_state != S_OBSTACLE) and (n_state != S_TARGET):
                    if self.visited_map[neighbour_x][neighbour_y] == 0:
                        self.set_visited([neighbour_x, neighbour_y])
                        self.queue.put([[neighbour_x, neighbour_y],[position[0], position[1]]])

    ###THE MAX COST IS HARDCODED; FIND A BETTER WAY
    def obstacle_cost_max(self): #make the costs of obstacle int_max
        obstacles = self.get_positions_of_given_state(S_OBSTACLE)
        for obs in obstacles:
            self.set_cost(obs, 10000000)
    