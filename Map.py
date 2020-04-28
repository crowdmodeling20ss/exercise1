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

    def __init__(self, width, height, data):
        self.id = 0
        self.width = width
        self.height = height
        self.data = data
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
                if (state == S_PEDESTRIAN and self.data[x][y] >= state) or (state != S_PEDESTRIAN and self.data[x][y] == state):
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

    def calculate_cost_map(self, djiksta_boolean=1):
        if (djiksta_boolean == 1):
            return Dijkstra(self, self.data).calculate_cost_map()
        return 0

    def get_cost(self, position):
        return self.cost_map[position[0]][position[1]]
