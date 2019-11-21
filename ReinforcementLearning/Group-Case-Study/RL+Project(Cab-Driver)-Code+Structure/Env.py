# Import routines

import numpy as np
import math
import random

# Defining hyperparameters
m = 5 # number of cities, ranges from 1 ..... m
t = 24 # number of hours, ranges from 0 .... t-1
d = 7  # number of days, ranges from 0 ... d-1
C = 5 # Per hour fuel and other costs
R = 9 # per hour revenue from a passenger


class CabDriver():

    def __init__(self):
        """initialise your state and define your action space and state space"""
        self.action_space = [[i,j] for i in range(0,m) for j in range(0,m) if i != j]
        self.state_space = list(np.zeros((m+t+d)))
        self.state_init = list(np.zeros((m+t+d)))

        # Start the first round
        self.reset()


    ## Encoding state (or state-action) for NN input

    def state_encod_arch1(self, state):
        """convert the state into a vector so that it can be fed to the NN. This method converts a given state into a vector format. Hint: The vector is of size m + t + d."""

        state_encod = list(np.zeros((m+d+t)))
        state_encod[state[0]]=1
        state_encod[m+np.int(state[1])]=1
        state_encod[m+t+np.int(state[2])]=1  
        print ('In state_encod_arch1()::::After encoding: state is::', state_encod)
        return state_encod


    # Use this function if you are using architecture-2 
    # def state_encod_arch2(self, state, action):
    #     """convert the (state-action) into a vector so that it can be fed to the NN. This method converts a given state-action pair into a vector format. Hint: The vector is of size m + t + d + m + m."""

        
    #     return state_encod


    ## Getting number of requests

    def requests(self, state):
        """Determining the number of requests basis the location. 
        Use the table specified in the MDP and complete for rest of the locations"""
        location = state[0]
        if location == 0:
            requests = np.random.poisson(2)
        elif location == 1:
            requests = np.random.poisson(12)
        elif location == 2:
            requests = np.random.poisson(4)
        elif location == 3:
            requests = np.random.poisson(7)
        elif location == 4:
            requests = np.random.poisson(8)
     
        if requests >15:
            requests =15
        
        print ('In requests():::: requests:', requests)
        possible_actions_index = random.sample(range(1, (m-1)*m +1), requests) # (0,0) is not considered as customer request
        print ('In requests()::::possible_actions_index=',possible_actions_index)
        actions = [self.action_space[i] for i in possible_actions_index]

        
        actions.append([0,0])
        print ('In requests()::::actions=',actions) 
        return possible_actions_index,actions   



    def reward_func(self, state, action, Time_matrix):
        """Takes in state, action and Time-matrix and returns the reward"""
        cur_loc = state[0]
        time = state[1]
        day_of_week = state[2]
        
        start_loc = action[0]
        end_loc = action[1]
        
        if start_loc == 0 and end_loc == 0:
            reward = -C
        else:
            reward = R *  Time_matrix[start_loc][end_loc][time][day_of_week] - C * (Time_matrix[start_loc][end_loc][time][day_of_week] + Time_matrix[cur_loc][start_loc][time][day_of_week])
        
        print ("In reward_func():::: reward for state:(", cur_loc, " , ",time, " , ", day_of_week,") action:( ", start_loc, " , ",end_loc,") is", reward) 
        return reward




    def next_state_func(self, state, action, Time_matrix):
        """Takes state and action as input and returns next state"""
        cur_loc = state[0]
        time = state[1]
        day_of_week = state[2]        
        start_loc = action[0]
        end_loc = action[1]
        
        print ('In next_state_func:::: cur_loc=',cur_loc,' time=',time,' day_of_week=',day_of_week,'  start_loc=',start_loc,'   end_loc=',end_loc)
        if start_loc == 0 and end_loc == 0:
            new_loc = start_loc
        else:
            if cur_loc != start_loc:
                new_loc = start_loc
                hrs_cur_loc_to_start_loc = Time_matrix[cur_loc][start_loc][time][day_of_week]
                new_time = np.int(time + hrs_cur_loc_to_start_loc)
                new_day_of_week = day_of_week
                if new_time >= 24 :
                    new_time = new_time - 24
                    new_day_of_week = (day_of_week + 1)% d
            else:
                new_loc = start_loc
                new_time = time
                new_day_of_week = day_of_week
            print ('In next_state_func:::: new_loc=',new_loc,' new_time=',new_time,' new_day_of_week=',new_day_of_week)   
            
            new_loc2 = end_loc
            hrs_start_loc_to_end_loc = Time_matrix[start_loc][end_loc][new_time][new_day_of_week]
            new_time2 = np.int(new_time + hrs_start_loc_to_end_loc)
            new_day_of_week2 = new_day_of_week
            if new_time2 >= 24 :
                new_time2 = new_time2 - 24
                new_day_of_week2 = (new_day_of_week2 + 1)% d
            print ('In next_state_func:::: new_loc2=',new_loc2,' new_time2=',new_time2,' new_day_of_week2=',new_day_of_week2)    
        next_state = [new_loc2,new_time2,new_day_of_week2]
        
        print ('In next_state_func:::: next_state===', next_state)
        
        return next_state




    def reset(self):
        return self.action_space, self.state_space, self.state_init
