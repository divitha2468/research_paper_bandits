# This is the common runtime file
from agent import agent
from environ import environment
from tqdm import tqdm
import math
import matplotlib.pyplot as plt



def call(debug):
    f = open("config.txt", 'r')
    algo = int(f.readline())
    N = int(f.readline())
    m = int(f.readline())
    actual_mean = [float(i) for i in f.readline().split(',')]
    availability = [float(i) for i in f.readline().split(',')]
    fairness = [float(i) for i in f.readline().split(',')]
    iterations = int(f.readline())
    curr_agent = agent(N, m, fairness)
    curr_env = environment(N, m, availability, actual_mean)
    print("Actual mean ", actual_mean)
    print("before running mean = ", curr_agent.mean_reward)
    regret_array = []
    avail_counter = [0]*N
    arr1 = []
    arr2 = []
    arr3 = []
    arr4 = []
    arr5 = []
    arr6 = []
    counter_after_pause = [0]*N
    available_after_pause = [0]*N
    avail_counter_arr = [[] for i in range(N)]
    pick_counter_arr = [[] for i in range(N)]
    total_regret = 0
    time = []
    counter = 0
    fairness_arr = [[] for i in range(N)]
    # print(selection_after_pause)
    for i in tqdm(range(iterations)):
        if i > 100 and i < 10000:
            available_arms = curr_env.available_arms(1)
        else:
            available_arms = curr_env.available_arms()
        for j in available_arms:
            avail_counter[j] += 1
        arms_LFG = curr_agent.pick_arms(available_arms, algo)
        if i > 10000 and i < 11000:
            for j in available_arms:
                available_after_pause[j] += 1
                avail_counter_arr[j].append(available_after_pause[j])
            for j in arms_LFG:
                counter_after_pause[j] += 1
                pick_counter_arr[j].append(counter_after_pause[j])
            arr1.append(counter_after_pause[0]/(i-10000))
            arr2.append(counter_after_pause[1]/(i-10000))
            arr3.append(counter_after_pause[2]/(i-10000))
            arr4.append(counter_after_pause[3]/(i-10000))
            arr5.append(counter_after_pause[4]/(i-10000))
            arr6.append(counter_after_pause[5]/(i-10000))
            for i in range(N):
                if(available_after_pause[i] != 0):
                    fairness_arr[i].append(
                        counter_after_pause[i]/available_after_pause[i])
                else:
                    fairness_arr[i].append(0)
        (LFG_reward, regret) = curr_env.get_reward(arms_LFG, available_arms)
        curr_agent.update_mean(LFG_reward)
        total_regret += regret
        if((i % 1000 == 0 and i != 0) or (i == 100)):
            time.append(i)
            regret_array.append(total_regret/i)
            #total_regret = 0
    print([len(i) for i in avail_counter_arr])
    print("counter ", counter)
    if debug == '1':
        print("expected selection fraction ", fairness)
        print("achieved selection fraction ", [
              i/iterations for i in curr_env.counter])
        print("achieved selection fraction after 10k ", [
              counter_after_pause[i]/10000 for i in range(N)])
        print("actual selection fraction ", [
              curr_env.counter[i]/avail_counter[i] for i in range(N)])

        print("after running mean = ", curr_agent.mean_reward)
        #plt.ylim(-0.01, 0.2)
        #plt.scatter(time, regret_array)
        # plt.title("title")
        # plt.xlabel("Time")
        # plt.ylabel("Regret")
        # plt.show()
        # plt.scatter([math.log(i) for i in time], [math.log(i)
        #                                           for i in regret_array])
        # plt.ylim(-7.0, 10)
        # plt.xlabel("logT")
        # plt.ylabel("log(Regret)")
        # plt.show()
        count = 0
        # print(len(selection_after_pause[0]))
        color = ['r.', 'g.', 'b.', 'k.', 'y.', 'm.']

        # for i in range(N):
        #     plt.plot(range(len(fairness_arr[i])), fairness_arr[i], color[i])
        # plt.xlim(0,1000)
        # plt.show()
        plt.plot(range(len(arr1)), arr1, 'r.')
        plt.plot(range(len(arr2)), arr2, 'g.')
        plt.plot(range(len(arr3)), arr3, 'b.')
        plt.plot(range(len(arr4)), arr4, 'k.')
        plt.plot(range(len(arr5)), arr5, 'y.')
        plt.plot(range(len(arr6)), arr6, 'm.')
        plt.show()
    return regret_array, fairness_arr, time

    print("fairness_ar", result_f)

