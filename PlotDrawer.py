import matplotlib.pyplot as plt
import numpy as np
import ast


from Simulation import show_path_time_plot, saveToFile

def main():
    scenario_4()

def parse(PATH, VELOCITY, POSITION, TIME):
    path_pedestrians = ast.literal_eval(open(PATH, "r").read())
    velocity_pedestrians = ast.literal_eval(open(VELOCITY, "r").read())
    position_history = ast.literal_eval(open(POSITION, "r").read())
    time_tick = ast.literal_eval(open(TIME, "r").read())

    ped_speeds = []
    for p_id, pedestrian in enumerate(position_history):
        for tp in pedestrian:
            tick = tp[0]
            position = tp[1]
            if 4 <= position[0] <= 6 and 50 <= position[1] <= 60:
                ped_speeds.append(velocity_pedestrians[p_id][tick])

    return path_pedestrians, velocity_pedestrians, position_history, time_tick


def scenario_4():
    directory = "test-1"
    PATH = "tests/scenario-4/" + directory + "/path_pedestrians.txt"
    VELOCITY = "tests/scenario-4/" + directory + "/velocity_pedestrians.txt"
    POSITION = "tests/scenario-4/" + directory + "/position_history.txt"
    TIME = "tests/scenario-4/" + directory + "/time_tick.txt"

    """ # FOR 4-0-1-10x100m
    PATH = "tests/scenario-4/4-0-1-10x100m/1path_pedestrians.txt"
    VELOCITY = "tests/scenario-4/4-0-1-10x100m/1velocity_pedestrians.txt"
    POSITION = "tests/scenario-4/4-0-1-10x100m/1position_history.txt"
    TIME = "tests/scenario-4/4-0-1-10x100m/1time_tick.txt"
    
    It seems that all speeds are 1
    """

    """ FOR 4-0-05-10x100m
    PATH = "tests/scenario-4/4-0-05-10x100m/100m_path_pedestrians.txt"
    VELOCITY = "tests/scenario-4/4-0-05-10x100m/100m_velocity_pedestrians.txt"
    POSITION = "tests/scenario-4/4-0-05-10x100m/100m_position_history.txt"
    TIME = "tests/scenario-4/4-0-05-10x100m/100m_time_tick.txt"
    """

    """
    len(np.array(velocity_pedestrians)[np.where((np.array(velocity_pedestrians) > 0) & (np.array(velocity_pedestrians) <= 1))])
    """

    path_pedestrians, velocity_pedestrians, position_history, time_tick = parse(PATH, VELOCITY, POSITION, TIME)

    show_path_time_plot(path_pedestrians, velocity_pedestrians, position_history, time_tick, False)

def scenario_7():
    path_pedestrians = []
    velocity_pedestrians = []
    position_history = []
    for d in open("tests/scenario-7/path_pedestrians.txt", "r").read().split("], ["):
        d = d.replace('[', '')
        d = d.replace(']', '')
        path_pedestrians.append(list(map(float, d.rstrip().split(','))))
    for d in open("tests/scenario-7/velocity_pedestrians.txt", "r").read().split("], ["):
        d = d.replace('[', '')
        d = d.replace(']', '')
        velocity_pedestrians.append(list(map(float, d.rstrip().split(','))))
    """
    for d in open("tests/scenario-7/position_history.txt", "r").read().split("], ["):
        d = d.replace('[', '')
        d = d.replace(']', '')
        position_history.append(list(map(float, d.rstrip().split(','))))
    """
    time_tick = (
        list(map(int, open("tests/scenario-7/time_tick.txt", "r").read().replace('[', '').replace(']', '').rstrip().split(","))))

    p = np.array(np.split(np.array(path_pedestrians), 5))
    v = np.array(np.split(np.array(velocity_pedestrians), 5))

    min_speeds = []
    average_speeds = []
    max_speeds = []
    ages = [4, 10, 20, 30, 40, 50, 60, 70, 80]
    for i in range(10):
        min_speeds.append(np.min(v[:, i][np.nonzero(v[:, i])]) /  10.0)
        average_speeds.append(np.average(v[:, i][np.nonzero(v[:, i])]) /  10.0)
        max_speeds.append(np.max(v[:, i][np.nonzero(v[:, i])]) /  10.0)

    min_speeds.pop(2) # remove 20
    average_speeds.pop(2) # remove 20
    max_speeds.pop(2) # remove 20

    plt.cla()
    plt.plot(ages, min_speeds, label="Min")
    plt.plot(ages, average_speeds, label="Avg.")
    plt.plot(ages, max_speeds, label="Max")
    plt.xlabel('Ages')
    plt.ylabel('Speed')
    plt.title('Speed/Age Pedestrian')
    plt.legend()
    plt.show()
    plt.pause(3)


if __name__ == '__main__':
    main()
