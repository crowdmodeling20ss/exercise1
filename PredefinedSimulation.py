from CellularModel import CellularModel
from GridCreator import GridCreator
from Map import Map
from ScenarioGrids import create_grid
from Simulation import Simulation


class PredefinedSimulation(Simulation):

    def run(self):
        self._is_running = True
        CONFIGURABLE_grid, is_dijkstra_enabled, is_pedestrian_exit = create_grid()
        print("is dijkstra enabled ", is_dijkstra_enabled)
        print("is_pedestrian_exit ", is_pedestrian_exit)
        self.IS_DIJKSTRA_ENABLED = is_dijkstra_enabled
        self.SHOW_COST_MAP = is_dijkstra_enabled
        self.IS_PEDESTRIAN_EXIT = is_pedestrian_exit

        CONFIGURABLE_the_grid = GridCreator(CONFIGURABLE_grid, 1)
        CONFIGURABLE_map_obj = Map(CONFIGURABLE_the_grid.grid.shape[0], CONFIGURABLE_the_grid.grid.shape[1],
                                   CONFIGURABLE_the_grid.grid, CONFIGURABLE_the_grid.corners, self.IS_DIJKSTRA_ENABLED)

        if self.SHOW_COST_MAP:
            self.show_cost_map(CONFIGURABLE_map_obj.cost_map, 5)

        CONFIGURABLE_model = CellularModel(CONFIGURABLE_map_obj, self.IS_PEDESTRIAN_EXIT, self.SPEED_OF_PEDESTRIANS,
                                           self.SPEED_PER_PEDESTRIAN_IS_ON, self.OBSTACLE_AVOIDANCE_ENABLED)
        self.runSimulation(CONFIGURABLE_model, self.SHOW_SPEED_GRAPH)
        # """
