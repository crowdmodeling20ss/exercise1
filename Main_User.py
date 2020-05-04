from PredefinedSimulation import PredefinedSimulation


def main():
    print("main_user")
    IS_DIJKSTRA_ENABLED = True
    IS_PEDESTRIAN_EXIT = True
    SPEED_OF_PEDESTRIANS = [1, 20]
    SPEED_PER_PEDESTRIAN_IS_ON = False
    SHOW_COST_MAP = True
    SHOW_SPEED_GRAPH = True
    IS_USER_DEFINED = True

    predefinedSimulation = PredefinedSimulation(IS_DIJKSTRA_ENABLED,
                                                IS_PEDESTRIAN_EXIT,
                                                SPEED_OF_PEDESTRIANS,
                                                SPEED_PER_PEDESTRIAN_IS_ON,
                                                SHOW_COST_MAP,
                                                SHOW_SPEED_GRAPH,
                                                IS_USER_DEFINED)
    predefinedSimulation.run()


if __name__ == '__main__':
    main()
