from CellularModel import CellularModel
from GridCreator import GridCreator
from Map import Map
from NewScenarios import create_grid_new_scenario
from Simulation import Simulation


class ConfigurableSimulation(Simulation):
    def run(self):
        self._is_running = True

        CONFIGURABLE_grid, is_dijkstra_enabled, speed, num_pedestrian = create_grid_new_scenario()
        self.IS_DIJKSTRA_ENABLED = is_dijkstra_enabled
        self.SHOW_COST_MAP = is_dijkstra_enabled
        num_speed = len(speed)
        # Num speed is to assign speeds in the new_scenario.txt to that number of pedestrians, rest will be filled with default speed 1
        if num_speed > 1:
            self.SPEED_PER_PEDESTRIAN_IS_ON = True
            for i in range(num_pedestrian - num_speed):
                speed.append([1,20])  # Assigning default speed for the rest of the pedestrians
            self.SPEED_OF_PEDESTRIANS = speed
        elif num_speed == 1:
            self.SPEED_PER_PEDESTRIAN_IS_ON = False
            self.SPEED_OF_PEDESTRIANS = speed[0]

        CONFIGURABLE_the_grid = GridCreator(CONFIGURABLE_grid, 1)  # No scale variable for new scenarios
        CONFIGURABLE_map_obj = Map(CONFIGURABLE_the_grid.grid.shape[0], CONFIGURABLE_the_grid.grid.shape[1],
                                   CONFIGURABLE_the_grid.grid, CONFIGURABLE_the_grid.corners, self.IS_DIJKSTRA_ENABLED)

        if self.SHOW_COST_MAP:
            self.show_cost_map(CONFIGURABLE_map_obj.cost_map, 5)

        CONFIGURABLE_model = CellularModel(CONFIGURABLE_map_obj, self.IS_PEDESTRIAN_EXIT, self.SPEED_OF_PEDESTRIANS,
                                           self.SPEED_PER_PEDESTRIAN_IS_ON)
        self.runSimulation(CONFIGURABLE_model, self.SHOW_SPEED_GRAPH)

