from ConfigurableSimulation import ConfigurableSimulation
from PredefinedSimulation import PredefinedSimulation


def main():
    print("main")
    IS_DIJKSTRA_ENABLED = True
    IS_PEDESTRIAN_EXIT = True
    SPEED_OF_PEDESTRIANS = [5, 20]
    SPEED_PER_PEDESTRIAN_IS_ON = False
    SHOW_COST_MAP = True
    SHOW_SPEED_GRAPH = True

    #PredefinedSimulation(IS_DIJKSTRA_ENABLED, IS_PEDESTRIAN_EXIT, SPEED_OF_PEDESTRIANS, SPEED_PER_PEDESTRIAN_IS_ON, SHOW_COST_MAP, SHOW_SPEED_GRAPH).run()
    ConfigurableSimulation(IS_DIJKSTRA_ENABLED, IS_PEDESTRIAN_EXIT, SPEED_OF_PEDESTRIANS, SPEED_PER_PEDESTRIAN_IS_ON, SHOW_COST_MAP, SHOW_SPEED_GRAPH).run()

if __name__ == '__main__':
    main()
