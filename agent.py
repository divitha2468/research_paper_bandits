import random
import math
import numpy as np


class agent():
    def __init__(self, n, m, r):
        # number of arms
        self.n = n
        # max number arms that can be pulled
        self.m = m
        # mean reward
        #self.mean_reward_greedy = [1]*n
        self.mean_reward = [1]*n
        self.h = [0]*self.n
        self.r = r
        self.Q = [0]*self.n
        self.d = [0]*self.n
        self.t = 0
        self.w = [1]*self.n
        self.eta = 1
        self.beta_max = 0
        self.bandit = 0
        self.alpha = [1]*self.n
        self.beta = [1]*self.n
        self.availability = [1]*self.n
        self.iter = 0

    def greedy_pick_arms(self, available_arms):
        greedy_selection = []
        mean_list = []
        for i in available_arms:
            mean_list.append((i, self.mean_reward[i]))
        mean_list = sorted(mean_list, key=lambda x: x[1], reverse=True)
        for i in range(self.m):
            if(i >= len(available_arms)):
                break
            greedy_selection.append(mean_list[0][0])
            del mean_list[0]
        return greedy_selection

    def LFG_pick_arms(self, available_arms):
        local_mean_reward = [0]*self.n
        for i in range(self.n):
            if self.h[i] > 0:
                local_mean_reward[i] = min(
                    self.mean_reward[i]+math.sqrt((3*math.log(self.t))/(2*self.h[i])), 1)
            else:
                local_mean_reward[i] = 1
            self.Q[i] = max((self.Q[i]+self.r[i]-self.d[i]), 0)
        super_arm_dict = []
        count = 0
        for j in available_arms:
            super_arm_dict.append(
                (j, self.Q[j]+self.eta*self.w[j]*local_mean_reward[j]))
        super_arm_dict = sorted(
            super_arm_dict, key=lambda x: x[1], reverse=True)
        LFG_selection = []
        # print(super_arm_dict)
        self.d = [0]*self.n
        for i in range(self.m):
            if count >= len(available_arms):
                break
            LFG_selection.append(super_arm_dict[0][0])
            self.d[super_arm_dict[0][0]] = 1
            del super_arm_dict[0]
            count += 1
        self.t += 1
        return LFG_selection

    def TS_pick_arms(self, available_arms):
        beta_distrib_list = []
        for i in range(self.n):
            beta_distrib_list.append(
                np.random.beta(self.alpha[i], self.beta[i]))
        available_arms_dict = []
        for i in available_arms:
            available_arms_dict.append(
                (i, (1/self.eta)*self.Q[i]+self.w[i]*beta_distrib_list[i]))
        available_arms_dict = sorted(
            available_arms_dict, key=lambda x: x[1], reverse=True)

        count = 0
        TS_selection = []
        for i in range(self.m):
            if count >= len(available_arms):
                break
            TS_selection.append(available_arms_dict[0][0])
            self.d[available_arms_dict[0][0]] = 1
            del available_arms_dict[0]
            count += 1
        # d_sum = []
        # for i in range(self.n):
        #     d_sum[] += d[i]
        for i in range(self.n):
            self.Q[i] = max((self.t*self.r[i]-self.h[i]), 0)
        self.t += 1

        return TS_selection

    def improved_LFG_pick_arms(self, available_arms):
        local_mean_reward = [0]*self.n
        self.iter += 1

        for i in range(self.n):
            if self.h[i] > 0:
                local_mean_reward[i] = min(
                    self.mean_reward[i]+math.sqrt((3*math.log(self.t))/(2*self.h[i])), 1)
            else:
                local_mean_reward[i] = 1
        super_arm_dict = []
        count = 0
        for j in available_arms:
            a = self.r[j]
            if(self.availability[j]/self.iter > a):
                a = self.availability[j]/self.iter
            super_arm_dict.append(
                (j, (self.Q[j]/a)+self.eta*self.w[j]*local_mean_reward[j]))
        super_arm_dict = sorted(
            super_arm_dict, key=lambda x: x[1], reverse=True)
        LFG_selection = []
        # print(super_arm_dict)
        self.d = [0]*self.n
        for i in range(self.m):
            if count >= len(available_arms):
                break
            LFG_selection.append(super_arm_dict[0][0])
            self.d[super_arm_dict[0][0]] = 1
            del super_arm_dict[0]
            count += 1
        self.t += 1
        for i in available_arms:
            self.Q[i] = max((self.Q[i]+(self.r[i]-self.d[i])), 0)

        for i in range(self.n):
            if(i in available_arms):
                self.availability[i] += 1
        return LFG_selection

    def improved_TS_pick_arms(self, available_arms):
        beta_distrib_list = []
        self.iter += 1

        for i in range(self.n):
            if(i in available_arms):
                self.availability[i] += 1
        for i in range(self.n):
            beta_distrib_list.append(
                np.random.beta(self.alpha[i], self.beta[i]))
        available_arms_dict = []
        for i in available_arms:
            a = self.r[i]
            if(self.availability[i]/self.iter > a):
                a = self.availability[i]/self.iter
            available_arms_dict.append(
                (i, (self.Q[i]/a+self.eta*self.w[i]*beta_distrib_list[i])))
        available_arms_dict = sorted(
            available_arms_dict, key=lambda x: x[1], reverse=True)

        count = 0
        TS_selection = []
        h = [0]*self.n
        for i in range(self.m):
            if count >= len(available_arms):
                break
            TS_selection.append(available_arms_dict[0][0])
            h[available_arms_dict[0][0]] = 1
            self.d[available_arms_dict[0][0]] = 1
            del available_arms_dict[0]
            count += 1
        for i in available_arms:
            self.Q[i] = max((self.Q[i]+(self.r[i]-self.d[i])), 0)

        # for i in available_arms:
        #     self.Q[i] = max((self.t*self.r[i]-h[i]), 0)
        # self.t += 1

        return TS_selection

    def pick_arms(self, available_arms, algo):
        if algo == 0:
            return self.greedy_pick_arms(available_arms)
        elif algo == 1:
            return self.LFG_pick_arms(available_arms)
        elif algo == 2:
            return self.TS_pick_arms(available_arms)
        elif algo == 3:
            return self.improved_LFG_pick_arms(available_arms)
        elif algo == 4:
            return self.improved_TS_pick_arms(available_arms)

    def update_mean(self, reward):
        for i in reward:
            self.mean_reward[i[0]] = (
                self.mean_reward[i[0]]*self.h[i[0]]+i[1])/(self.h[i[0]]+1)
            self.h[i[0]] += 1
            self.alpha[i[0]] += i[1]
            self.beta[i[0]] += 1-i[1]