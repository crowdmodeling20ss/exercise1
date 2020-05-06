#!/usr/bin/python
import time
from abc import ABC

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors


class Simulation(ABC):
    def __init__(self, IS_DIJKSTRA_ENABLED=True, IS_PEDESTRIAN_EXIT=True, SPEED_OF_PEDESTRIANS=None,
                 SPEED_PER_PEDESTRIAN_IS_ON=False, SHOW_COST_MAP=True, SHOW_SPEED_GRAPH=False, OBSTACLE_AVOIDANCE=True):
        self._is_running = False
        self.IS_DIJKSTRA_ENABLED = IS_DIJKSTRA_ENABLED
        self.IS_PEDESTRIAN_EXIT = IS_PEDESTRIAN_EXIT
        self.SPEED_OF_PEDESTRIANS = SPEED_OF_PEDESTRIANS
        self.SPEED_PER_PEDESTRIAN_IS_ON = SPEED_PER_PEDESTRIAN_IS_ON
        self.SHOW_COST_MAP = SHOW_COST_MAP
        self.SHOW_SPEED_GRAPH = SHOW_SPEED_GRAPH
        self.OBSTACLE_AVOIDANCE = OBSTACLE_AVOIDANCE

    def run(self):
        print("Simulation(ABC).run(self)")

    def runSimulation(self, ca_model, velocity_graph_enabled=True):
        cmap = colors.ListedColormap(['ghostwhite', 'Khaki', 'mediumaquamarine', 'firebrick'])
        bounds = [0, 1, 2, 3, 4]
        norm = colors.BoundaryNorm(bounds, cmap.N)

        simulation_boolean = True
        time_tick = []
        path_pedestrians = {}
        velocity_pedestrians = {}
        position_history = {}
        for i in ca_model.pedestrians:
            p = ca_model.pedestrians[i]
            path_pedestrians[p.p_id] = []
            velocity_pedestrians[p.p_id] = []
            position_history[p.p_id] = []

        time_counter = 0
        plt.show()
        while self._is_running and simulation_boolean == True:
            plt.cla()
            plt.imshow(ca_model.grid_map.data, interpolation='nearest', origin='upper', cmap=cmap, norm=norm)
            plt.pause(5)
            start = time.time()
            ca_model.tick()
            plt.cla()
            done = time.time()
            elapsed = done - start

            simulation_boolean = ca_model.end_simulation()

            if velocity_graph_enabled:
                time_counter += 1
                for i in ca_model.pedestrians:
                    p = ca_model.pedestrians[i]
                    last_distance = 0 if len(path_pedestrians[p.p_id]) == 0 else path_pedestrians[p.p_id][
                        time_counter - 2]
                    last_position = np.array(p.visited_path[len(p.visited_path) - 2])
                    current_position = np.array(p.visited_path[len(p.visited_path) - 1])  # or p.position
                    distance = np.linalg.norm(current_position - last_position)
                    total_distance = last_distance + distance

                    path_pedestrians[p.p_id].append(total_distance)
                    velocity_pedestrians[p.p_id].append(distance)
                    position_history[p.p_id] += [[time_counter, i] for i in p.path_cost_history[len(position_history[p.p_id]):]] # not tested

                time_tick.append(time_counter)

        if velocity_graph_enabled: self.show_path_time_plot(path_pedestrians, velocity_pedestrians, position_history, time_tick, True)

    def saveToFile(self, path_pedestrians, velocity_pedestrians, position_history, time_tick):
        f = open("path_pedestrians.txt", "w")
        f.write(str([path_pedestrians[g] for g in path_pedestrians]))
        f.close()
        f = open("velocity_pedestrians.txt", "w")
        f.write(str([velocity_pedestrians[g] for g in velocity_pedestrians]))
        f.close()
        f = open("position_history.txt", "w")
        f.write(str([position_history[g] for g in position_history]))
        f.close()
        f = open("time_tick.txt", "w")
        f.write(str(time_tick))
        f.close()

    def show_cost_map(self, cost_map, duration):
        print('Calculated cost Map')
        print(cost_map)
        plt.show()
        plt.interactive(False)
        plt.cla()
        plt.imshow(cost_map, cmap='Blues', interpolation='nearest')
        plt.pause(duration)

    def show_path_time_plot(self, path_pedestrians, velocity_pedestrians, position_history, time_tick, is_saved):
        t = len(time_tick)
        for i in range(len(path_pedestrians)):
            if (len(path_pedestrians[i]) < t):
                for _ in range(t - len(path_pedestrians[i])):
                    try:
                        path_pedestrians[i] += [path_pedestrians[i][len(path_pedestrians[i]) - 1]]
                    except:
                        path_pedestrians[i] += [0]
                for _ in range(t - len(velocity_pedestrians[i])):
                    velocity_pedestrians[i] += [0]

        if is_saved:
            self.saveToFile(path_pedestrians, velocity_pedestrians, position_history, time_tick)

        plt.show()
        plt.cla()
        for i in range(len(path_pedestrians)):
            plt.plot(time_tick, path_pedestrians[i], label="P#" + str(i))
        plt.xlabel('Time')
        plt.ylabel('Path')
        plt.title('Path/Time Pedestrian')
        plt.legend()
        plt.show()
        plt.pause(1)

        plt.show()
        plt.cla()
        for i in range(len(path_pedestrians)):
            plt.plot(time_tick, velocity_pedestrians[i], label="V#"+str(i))
        plt.xlabel('Time')
        plt.ylabel('Speed')
        plt.title('Speed/Time Pedestrian')
        plt.legend()
        plt.show()
        plt.pause(1)
