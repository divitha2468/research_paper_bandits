import random


class environment():
    def __init__(self, k, m, avail, mean_reward):
        self.k = k  # no.of arms
        self.m = m  # maximum arms that can be pulled
        self.avail = avail  # available probability
        self.mean_reward = mean_reward
        self.mean_max = mean_reward.index(max(mean_reward))
        self.counter = [0]*self.k

    def available_arms(self, unavail=0):
        if unavail == 0:
            return [i for i in range(self.k) if random.random() < self.avail[i]]
        else:
            arr = []
            for i in range(self.k):
                if i == self.mean_max:
                    continue
                if i == 4 or i == 1:
                    continue
                elif random.random() < self.avail[i]:
                    arr.append(i)
            return arr

    def get_reward(self, arms_lfg, available_arms):
        rewards_sample = {}
        for i in available_arms:
            if(random.random() < self.mean_reward[i]):
                rewards_sample[i] = 1

            else:
                rewards_sample[i] = 0
        mean_rewards = []
        for i in available_arms:
            mean_rewards.append((i, self.mean_reward[i]))
        mean_rewards = sorted(mean_rewards, key=lambda x: x[1], reverse=True)

        reward_greedy = 0
        reward_lfg = 0
        reward_array_lfg = []
        for i in range(self.m):
            if(i >= len(available_arms)):
                break
            reward_greedy += rewards_sample[mean_rewards[0][0]]
            del mean_rewards[0]
        for i in arms_lfg:
            reward_array_lfg.append((i, rewards_sample[i]))
            reward_lfg += rewards_sample[i]
            self.counter[i] += 1
        # if(reward_greedy - reward_lfg > 0):
        #    print(reward_greedy - reward_lfg)

        return(reward_array_lfg, reward_greedy-reward_lfg)