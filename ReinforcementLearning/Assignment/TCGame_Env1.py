from gym import spaces
import numpy as np
import random
from itertools import groupby
from itertools import product



class TicTacToe():

    def __init__(self):
        """initialise the board"""
        
        # initialise state as an array
        self.state = [np.nan for _ in range(9)]  # initialises the board position, can initialise to an array or matrix
        print('States initialized---',self.state)
        
        # all possible numbers
        self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)] # , can initialise to an array or matrix
        print('Initialize all states---',self.all_possible_numbers)
        
        self.reset()



    def is_winning(self, curr_state):
        """Takes state as an input and returns whether any row, column or diagonal has winning sum
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan]
        Output = False"""
        
        #print('Current State---', curr_state)
        if self.checkrow(curr_state) or self.checkcol(curr_state) or self.checkdiag(curr_state):
            print ('current state is a winning position')
            return True
        else:
            print ('current state is not a winning position')
            return False
 

    def is_terminal(self, curr_state):
        # Terminal state could be winning state or when the board is filled up

        if self.is_winning(curr_state) == True:
            return True, 'Win'

        elif len(self.allowed_positions(curr_state)) ==0:
            return True, 'Tie'

        else:
            return False, 'Resume'


    def allowed_positions(self, curr_state):
        """Takes state as an input and returns all indexes that are blank"""
        return [i for i, val in enumerate(curr_state) if np.isnan(val)]


    def allowed_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""

        used_values = [val for val in curr_state if not np.isnan(val)]
        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 !=0]
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 ==0]

        return (agent_values, env_values)


    def action_space(self, state):
        """Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""
        
        agent_actions = product(self.allowed_positions(state), self.allowed_values(state)[0])
        env_actions = product(self.allowed_positions(state), self.allowed_values(state)[1])
        #print('Action space: env ---',list(env_actions))
        return (agent_actions, env_actions)



    def state_transition(self, state, curr_action):
        """Takes current state and action and returns the board position just after agent's move.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """
        #print('Current state-->',state, '   curr_action--->',curr_action)
        if np.isnan(state[curr_action[0]]):
            #print('In if')
            state[curr_action[0]]=curr_action[1] ### TODO: need to add +1
        print('After state transition-->',state)
        return state


    def step(self, curr_state, curr_action):
        """Takes current state and action and returns the next state, reward and whether the state is terminal. Hint: First, check the board position after
        agent's move, whether the game is won/loss/tied. Then incorporate environment's move and again check the board status.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = ([1, 2, 3, 4, nan, nan, nan, 9, nan], -1, False)"""
        reward=0
        stateTerm=False
        curr_state1=curr_state.copy()
        #print ('In step---curr_state->', curr_state, '   curr_state1->',curr_state1)
        result, result_val = self.is_terminal(curr_state1)
        print ('In step: initially - After state transition check state terminal-->',result, '  result_val-->',result_val)
        if result == False and result_val == 'Resume':
            new_state = self.state_transition(curr_state1, curr_action)
            result, result_val = self.is_terminal(new_state)
            print ('In step: after agent action - After state transition check state terminal-->',result, '  result_val-->',result_val)
            if result == True and result_val == 'Win':
                reward = 10
                stateTerm = True
            elif result == True and result_val == 'Tie':
                reward = 0
                stateTerm = True
            else:
                reward = -1
                stateTerm = False
                
            if stateTerm == False:
                agent_actions, env_actions = self.action_space(new_state)
                agent_actions_list = list(agent_actions) 
                env_actions_list = list(env_actions)
                #print('Environment - action space---->',env_actions_list)
                new_env_action = env_actions_list[random.randrange(len(env_actions_list))]
                print ('Current action of Environment->', new_env_action)
                new_state = self.state_transition(new_state, new_env_action)
                result, result_val = self.is_terminal(new_state)
                print ('In step - after env action -  After state transition check state terminal-->',result, '  result_val-->',result_val)
                if result == True and result_val == 'Win':
                    reward = -10  ## Here env wins, agent loses
                    stateTerm = True
                elif result == True and result_val == 'Tie':
                    reward = 0
                    stateTerm = True
                else:
                    stateTerm = False
        #print('new state->', new_state,'  reward->', reward, '   state terminal->',stateTerm, '  current_state->',curr_state)
        return (new_state, reward, stateTerm)

    def reset(self):
        return self.state
    
    """ New methods added """
    def checkrow(self, state):
        if (state[0]+state[1]+state[2] == 15) or (state[3]+state[4]+state[5] == 15) or (state[6]+state[7]+state[8] == 15):
            return True
        else:
            return False
    
    def checkcol(self, state):
        if (state[0]+state[3]+state[6] == 15) or (state[1]+state[4]+state[7] == 15) or (state[2]+state[5]+state[8] == 15):
            return True
        else:
            return False
        
    def checkdiag(self, state):
        if (state[0]+state[4]+state[8] == 15) or (state[2]+state[4]+state[6] == 15):
            return True
        else:
            return False