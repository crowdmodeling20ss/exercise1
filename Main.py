from PredefinedSimulation import PredefinedSimulation


def main():
    print("main")
    IS_DIJKSTRA_ENABLED = True
    IS_PEDESTRIAN_EXIT = True
    SPEED_OF_PEDESTRIANS = [11, 12]
    SPEED_PER_PEDESTRIAN_IS_ON = False
    SHOW_COST_MAP = True
    SHOW_SPEED_GRAPH = True

    predefinedSimulation = PredefinedSimulation(IS_DIJKSTRA_ENABLED,
                                                IS_PEDESTRIAN_EXIT,
                                                SPEED_OF_PEDESTRIANS,
                                                SPEED_PER_PEDESTRIAN_IS_ON,
                                                SHOW_COST_MAP,
                                                SHOW_SPEED_GRAPH)
    predefinedSimulation.run()


if __name__ == '__main__':
    main()
