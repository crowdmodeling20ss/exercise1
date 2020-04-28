"""
Responsible for creating pedestrians and moving them in the given map
"""

from Map import Map
from Pedestrian import Pedestrian
from Constant import *


class CellularModel:
    """
    :type pedestrians: list
    :param grid_map: Map
    :type grid_map: Map
    """

    def __init__(self, grid_map):
        self.pedestrians = []
        self.grid_map = grid_map

        self.import_pedestrians_from_map()

    # Move all pedestrians one iteration
    # Assume 1 iteration is 1 second
    # if we want to change time, we can change number of iteration. i.e. 1 iteration is 10 second
    def tick(self):
        for p in self.pedestrians:
            p.tick()

    # make private
    def import_pedestrians_from_map(self):
        i=S_PEDESTRIAN
        for pos in self.grid_map.get_positions_of_given_state(S_PEDESTRIAN):
            self.pedestrians.append(Pedestrian(i, self, self.grid_map, pos))
            i += 1

    def remove_pedestrian(self, pedestrian):
        #self.pedestrians.remove(pedestrian)
        return