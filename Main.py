from ConfigurableSimulation import ConfigurableSimulation
from PredefinedSimulation import PredefinedSimulation


def main():
    print("main")
    OBSTACLE_COST_ENABLED = False
    IS_DIJKSTRA_ENABLED = False
    IS_PEDESTRIAN_EXIT = True
    SPEED_OF_PEDESTRIANS = None
    SPEED_PER_PEDESTRIAN_IS_ON = False
    SHOW_COST_MAP = True
    SHOW_SPEED_GRAPH = True
    OBSTACLE_AVOIDANCE_ENABLED = False

    PredefinedSimulation(IS_DIJKSTRA_ENABLED, IS_PEDESTRIAN_EXIT, SPEED_OF_PEDESTRIANS, SPEED_PER_PEDESTRIAN_IS_ON, SHOW_COST_MAP, SHOW_SPEED_GRAPH, OBSTACLE_AVOIDANCE_ENABLED).run()
    #ConfigurableSimulation(IS_DIJKSTRA_ENABLED, IS_PEDESTRIAN_EXIT, SPEED_OF_PEDESTRIANS, SPEED_PER_PEDESTRIAN_IS_ON, SHOW_COST_MAP, SHOW_SPEED_GRAPH, OBSTACLE_AVOIDANCE_ENABLED).run()

if __name__ == '__main__':
    main()
