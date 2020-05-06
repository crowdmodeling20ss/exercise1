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

    return path_pedestrians, velocity_pedestrians, position_history, time_tick


def scenario_4():
    directory = "test-3-density"
    PATH = "tests/scenario-4/" + directory + "/path_pedestrians.txt"
    VELOCITY = "tests/scenario-4/" + directory + "/velocity_pedestrians.txt"
    POSITION = "tests/scenario-4/" + directory + "/position_history.txt"
    TIME = "tests/scenario-4/" + directory + "/time_tick.txt"

    # 15 x 175
    # M1 Measuring pont 1 top-left
    """
    MEASURING_POINT_X1 = 6
    MEASURING_POINT_X2 = 10
    MEASURING_POINT_Y1 = 32
    MEASURING_POINT_Y2 = 36
    """
    # M2 Measuring point 2 top-right
    """
    MEASURING_POINT_X1 = 6
    MEASURING_POINT_X2 = 10
    MEASURING_POINT_Y1 = 138
    MEASURING_POINT_Y2 = 142
    """

    # M3 Measuring pont 1 bottom-right
    #"""
    MEASURING_POINT_X1 = 11
    MEASURING_POINT_X2 = 15
    MEASURING_POINT_Y1 = 138
    MEASURING_POINT_Y2 = 142
    #"""

    MESAUREMENT_START_TICK = 10
    MESAUREMENT_END_TICK = 70

    """
    # 0.5 Density test-05-density
        - M1 25 speeds are found. Average speed for the density:2.9694427190999915 
        - M2 1402 speeds are found. Average speed for the density:2.9772245960823795 
        - M3 1042 speeds are found. Average speed for the density:3.0 
    # colab-dense-1
        - M1 1128 speeds are found. Average speed for the density:1.347634358311136
        - M2 2948 speeds are found. Average speed for the density:2.4767237153688786
        - M3 2107 speeds are found. Average speed for the density:2.812024183697182
    # colab-dense-2
        - M1 4929 speeds are found. Average speed for the density:1.0611357693847558
        - M2 4888 speeds are found. Average speed for the density:1.5387609558577051
        - M3 3758 speeds are found. Average speed for the density:2.016961733018219
        
        # M1 Measuring point 2 top-left
        MEASURING_POINT_X1 = 3
        MEASURING_POINT_X2 = 7
        MEASURING_POINT_Y1 = 13
        MEASURING_POINT_Y2 = 37
        
        # M2 Measuring point 2 top-right
        MEASURING_POINT_X1 = 3
        MEASURING_POINT_X2 = 7
        MEASURING_POINT_Y1 = 138
        MEASURING_POINT_Y2 = 162
        
        # M3 Measuring pont 1 bottom-right
        MEASURING_POINT_X1 = 8
        MEASURING_POINT_X2 = 12
        MEASURING_POINT_Y1 = 138
        MEASURING_POINT_Y2 = 162
    """

    """
    # 0.5 Density test-05-density
        - M1  0
        - M2  248 speeds are found. Average speed for the density:3.0
        - M3  191 speeds are found. Average speed for the density:3.0
    # colab-dense-1
        - M1 123 speeds are found. Average speed for the density:1.527096062845508
        - M2 621 speeds are found. Average speed for the density:2.301254321586118
        - M3 434 speeds are found. Average speed for the density:2.8958300535886954
    # colab-dense-2
        - M1 442 speeds are found. Average speed for the density:1.0471330672624377
        - M2 1307 speeds are found. Average speed for the density:1.2785607755967683
        - M3 983 speeds are found. Average speed for the density:1.5905911186774953
        
        # M1 Measuring point 2 top-left
        MEASURING_POINT_X1 = 3
        MEASURING_POINT_X2 = 7
        MEASURING_POINT_Y1 = 13
        MEASURING_POINT_Y2 = 17
    
        # M2 Measuring point 2 top-right
        MEASURING_POINT_X1 = 3
        MEASURING_POINT_X2 = 7
        MEASURING_POINT_Y1 = 138
        MEASURING_POINT_Y2 = 142
    
        # M3 Measuring pont 1 bottom-right
        MEASURING_POINT_X1 = 8
        MEASURING_POINT_X2 = 12
        MEASURING_POINT_Y1 = 138
        MEASURING_POINT_Y2 = 142
    """

    """
        # 0.5 Density test-05-density
            - M1  14 speeds are found. Average speed for the density:3.0
            - M2  190 speeds are found. Average speed for the density:3.0
            - M3  136 speeds are found. Average speed for the density:3.0
        # colab-dense-1
            - M1 204 speeds are found. Average speed for the density:1.8612350132107232
            - M2 503 speeds are found. Average speed for the density:2.723019457410518
            - M3 243 speeds are found. Average speed for the density:2.9622749618518416
        # colab-dense-2
            - M1 1171 speeds are found. Average speed for the density:1.0449385644641258
            - M2 1116 speeds are found. Average speed for the density:1.448460740100788
            - M3 697 speeds are found. Average speed for the density:1.8249596762984002
        # test-3-density
            - M1 2126 speeds are found. Average speed for the density:1.055619058313724
            - M2 1696 speeds are found. Average speed for the density:1.0899069492644329
            - M3 1134 speeds are found. Average speed for the density:1.0637841824691272
                        
            # M1 Measuring point 2 top-left
            MEASURING_POINT_X1 = 6
            MEASURING_POINT_X2 = 10
            MEASURING_POINT_Y1 = 32
            MEASURING_POINT_Y2 = 36
            
            # M2 Measuring point 2 top-right
            MEASURING_POINT_X1 = 6
            MEASURING_POINT_X2 = 10
            MEASURING_POINT_Y1 = 138
            MEASURING_POINT_Y2 = 142
        
            # M3 Measuring pont 1 bottom-right
            MEASURING_POINT_X1 = 11
            MEASURING_POINT_X2 = 15
            MEASURING_POINT_Y1 = 138
            MEASURING_POINT_Y2 = 142
        """





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


    ped_speeds = []
    for p_id, pedestrian in enumerate(position_history):
        for tp in pedestrian:
            tick = tp[0]
            position = tp[1]
            if MEASURING_POINT_X1 <= position[0] <= MEASURING_POINT_X2 and MEASURING_POINT_Y1 <= position[1] <= MEASURING_POINT_Y2\
                    and MESAUREMENT_START_TICK <= tick <= MESAUREMENT_END_TICK:
                ped_speeds.append(velocity_pedestrians[p_id][tick])

    print(str(len(ped_speeds))+" speeds are found. Average speed for the density:" + str(sum(ped_speeds)/float(len(ped_speeds))))
    #show_path_time_plot(path_pedestrians, velocity_pedestrians, position_history, time_tick, False)

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
