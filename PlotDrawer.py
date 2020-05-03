import matplotlib.pyplot as plt
import numpy as np


def main():
    scenario_7()


def scenario_7():
    path_pedestrians = []
    velocity_pedestrians = []
    for d in open("tests/scenario-7/path_pedestrians.txt", "r").read().split("], ["):
        d = d.replace('[', '')
        d = d.replace(']', '')
        path_pedestrians.append(list(map(float, d.rstrip().split(','))))
    for d in open("tests/scenario-7/velocity_pedestrians.txt", "r").read().split("], ["):
        d = d.replace('[', '')
        d = d.replace(']', '')
        velocity_pedestrians.append(list(map(float, d.rstrip().split(','))))

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
