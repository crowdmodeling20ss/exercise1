from ConfigurableSimulation import ConfigurableSimulation
from PredefinedSimulation import PredefinedSimulation
import sys

def main():
    print("main")
    IS_DIJKSTRA_ENABLED = True
    IS_PEDESTRIAN_EXIT = True
    SPEED_OF_PEDESTRIANS = None
    SPEED_PER_PEDESTRIAN_IS_ON = False
    SHOW_COST_MAP = True
    SHOW_SPEED_GRAPH = True
   
    if len(sys.argv) == 1 or sys.argv[1].lower() == "predefined":  # python simulation.py   or   python simulation.py predefined
        PredefinedSimulation(IS_DIJKSTRA_ENABLED, IS_PEDESTRIAN_EXIT, SPEED_OF_PEDESTRIANS, SPEED_PER_PEDESTRIAN_IS_ON, SHOW_COST_MAP, SHOW_SPEED_GRAPH).run()
    elif len(sys.argv) > 1  and sys.argv[1].lower() == "configurable":  # python simulation.py configurable
        ConfigurableSimulation(IS_DIJKSTRA_ENABLED, IS_PEDESTRIAN_EXIT, SPEED_OF_PEDESTRIANS, SPEED_PER_PEDESTRIAN_IS_ON, SHOW_COST_MAP, SHOW_SPEED_GRAPH).run()

if __name__ == '__main__':
    main()
