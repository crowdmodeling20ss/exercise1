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
        self.corners = corners #left-top, right-top, left-bottom, right-bottom
        self.desired_speeds = desired_speeds if desired_speeds is None else self.get_initial_speeds()
        self.visited_path = [position]
        self.size = self.get_size()#This is to understand how many blocks does the ped. has in ints width/height

    def get_size(self):
        #print("Corners:", self.corners)
        #print("Get Size:", self.corners[1][1] - self.corners[0][1])
        return abs(self.corners[0][1] - self.corners[1][1]+1) ###+1 or NOT

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

    def tick_multicell(self):
        self.get_best_next_position_Multicell()
        print("corners:", self.corners)
        


    def forward(self, next_position):
        self.grid_map.set_state(next_position, S_PEDESTRIAN)
        self.grid_map.set_state(self.position, S_EMPTY)
        self.position = next_position
        self.visited_path.append(next_position)

    def exit(self):
        self.grid_map.set_state(self.position, S_EMPTY)
        self.ca_model.remove_pedestrian(self)


    ###TODO: Make this function make multi-cell decision
    def get_best_next_position_Multicell(self):
        #print("get best next position size", self.size)

        neighbour_costs = self.grid_map.get_neighbours_multicell(self.corners, self.size)
        ## we will get a vector with costs of [top, right, bottom. left]
        ##The cost of -1 means that the neighbor of that side has a target
        ##The cost of -2 means that the neighbor of that side has a obstacle or ped. so we cant move there.
        
        ##The interaction cost is not added yet.
        if self.pedestrian_end_check(neighbour_costs) == True:
            self.exit_multicell()
        else:
            best = -1
            cost = math.inf
            for i in range(4):#check all sides
                if neighbour_costs[i] != -2 and cost > neighbour_costs[i]:
                    cost = neighbour_costs[i]
                    best = i
            if best != -1: #There is a possible way
                self.forward_multicell(best)
                print("Best direction is:", best)
            
    def exit_multicell(self):
        self.grid_map.set_state_block(self.corners, self.size, S_EMPTY)
        self.ca_model.remove_pedestrian(self)

    def pedestrian_end_check(self, n_costs):
        for i in n_costs:
            if i == -1:
                ###end the pedestrian
                return True
        return False

    def forward_multicell(self, direction):##move size many blocks into the direction.

        #####UPDATE CORNERS: 
        if direction == D_TOP:# row -1
            self.grid_map.set_state_multicell(self.corners[2], D_BOTTOM,self.size, S_EMPTY ) #Empty the existing cells that move
            self.grid_map.set_state_multicell([self.corners[0][0]-1, self.corners[0][1]],D_TOP, self.size, S_PEDESTRIAN)
            for i in range(4):
                self.corners[i] = [self.corners[i][0] -1, self.corners[i][1]]
        elif direction == D_RIGHT: # column +1
            self.grid_map.set_state_multicell(self.corners[0], D_LEFT,self.size, S_EMPTY ) #Empty the existing cells that move
            self.grid_map.set_state_multicell([self.corners[1][0],self.corners[1][1]+1],D_RIGHT, self.size, S_PEDESTRIAN)
            for i in range(4):
                #print("error", self.corners[i][1])
                self.corners[i] = [self.corners[i][0], self.corners[i][1] +1]
        elif direction == D_BOTTOM:#row +1
            self.grid_map.set_state_multicell(self.corners[0], D_TOP,self.size, S_EMPTY ) #Empty the existing cells that move
            self.grid_map.set_state_multicell([self.corners[2][0]+1, self.corners[2][1]],D_BOTTOM, self.size, S_PEDESTRIAN)
            for i in range(4):
                self.corners[i] = [self.corners[i][0] +1, self.corners[i][1]]
        elif direction == D_LEFT: # column -1
            self.grid_map.set_state_multicell(self.corners[1], D_RIGHT,self.size, S_EMPTY ) #Empty the existing cells that move
            self.grid_map.set_state_multicell([self.corners[0][0], self.corners[0][1]-1],D_LEFT, self.size, S_PEDESTRIAN)
            for i in range(4):
                self.corners[i] = [self.corners[i][0], self.corners[i][1] -1]
    
    
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
