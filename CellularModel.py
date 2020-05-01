"""
Responsible for creating pedestrians and moving them in the given map
"""

from Map import Map
from Pedestrian import Pedestrian
from Constant import *
import Util


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
        for p_id, p in enumerate(self.pedestrians):
            #p.tick()
            p.tick_multicell()

    # make private
    def import_pedestrians_from_map(self):
        print("CORNERS:", self.grid_map.corners)
        for p_id, corners in enumerate(self.grid_map.corners):
            #print("THIS IS POS", pos)
            #self.pedestrians.append(Pedestrian(p_id, self, self.grid_map, pos, 0, ))
            #print("Corners of this pedestrian:", self.grid_map.corners[p_id])
            ######DEFINE THE R_MAX
            r_max = self.get_size() * 2
            print("R_max:", r_max)
            center = Util.calculate_center(corners)
            self.pedestrians.append(Pedestrian(p_id, self, self.grid_map, center, 0, self.grid_map.corners[p_id], r_max))

    def get_size(self):
        #print("Corners:", self.corners)
        #print("Get Size:", self.corners[1][1] - self.corners[0][1])
        return abs(self.grid_map.corners[0][0][1] - self.grid_map.corners[0][1][1])+1 ###+1 or NOT

    def remove_pedestrian(self, pedestrian):
        self.grid_map.set_state_block(pedestrian.corners, pedestrian.size, S_EMPTY)
        self.pedestrians.remove(pedestrian)
    
    def end_simulation(self):
        if len(self.pedestrians) == 0:
            print("ALL PEDESTRIANS REACHED THE TARGET, ENDING SIMULATION")
            return False
        else:
            return True