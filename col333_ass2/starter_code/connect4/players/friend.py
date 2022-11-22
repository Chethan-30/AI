import random
import numpy as np
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer
import copy


class AIPlayer:
    def __init__(self, player_number: int, time: int):
        """
        :param player_number: Current player number
        :param time: Time per move (seconds)
        """
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.time = time
        # Do the rest of your implementation here

    # Functions used by alpha_beta
    def change_state(self,state: Tuple[np.array, Dict[int, Integer]],action,play_number):
        # if action[1]==False:
        #     num=0
        #     for i in range(len(state[0])-1):
        #         if state[0][i][action[0]]==0:
        #             num=i
        #     state[0][num][action[0]]=play_number
        #     return state
        # else:
        #     for i in range(len(state[0])-1,0,-1):
        #         state[0][i][action[0]]=state[0][i-1][action[0]]

        #     state[0][0][action[0]]=0
        #     state[1][play_number].decrement()
        #     return state
        if action[1]==False:
            n=0
            for i in range(len(state[0])-1):
                if state[0][i][action[0]]==0:
                    n=i
            state[0][i][action[0]]=play_number
                    # return state
                    
            # return state
        else:
            for i in range(len(state[0])-1,0,-1):
                state[0][i][action[0]]=state[0][i-1][action[0]]

            state[0][0][action[0]]=0
            state[1][play_number].decrement()
            # return state
        return state
    
    def turn_action_to_result(self,state,action,player_number):
        row=0
        # print("xxxxxx")
        if(action[1]=="True"):
            # print("Entered the pop out loop",state[1][player_number])
            for i in range(len(state[0])-1,0,-1):
                state[0][i][action[0]]= state[0][i-1][action[0]]
            
            state[0][0][action[0]]=0
            state[1][player_number].decrement()
            # print("Exit the pop out loop",state[1][player_number])
            # print("Hello world55")

        else:
            for i in range(0,len(state[0])):
                if(state[0][i][action[0]]==0):
                    row=i

            
            state[0][row][action[0]]=player_number

                   
        
        # print("exittttt")
        return state

    
  
    def max_value(self,state, alpha, beta,depth):
       
        # print("Yes3333")
        # print("Hello world")
        valid_moves=get_valid_actions(self.player_number,state)
          

        # print("Len1:",(valid_moves))
        
        
        if len(valid_moves)==0 or depth==0:
             
              if(self.player_number==1):
                return  get_pts(self.player_number,state[0])-get_pts(2,state[0])
              
              else:
                   return  get_pts(self.player_number,state[0])-get_pts(1,state[0])
                

        v = -np.inf
        for a in valid_moves:
           
            if(self.player_number==1):
               v = max(v,self.min_value(self.change_state(copy.deepcopy(state),a,1), alpha,beta,depth-1))
            
            else:
                 v = max(v,self.min_value(self.change_state(copy.deepcopy(state),a,2), alpha, beta,depth-1))
            
           
            #    v = max(v,self.min_value(self.turn_action_to_result(state,a,self.player_number), alpha, beta))
            
            # v = max(v, self.min_value(self.turn_action_to_result(copy.copy(state),a,self.player_number), alpha, beta))
            if v >= beta:
                   return v
            alpha = max(alpha, v)
           
        return v

    def min_value(self,state, alpha, beta,depth):
        # print("Yedsssss444")
        # print("Hello world1")
        
        
        if(self.player_number==1):
             valid_moves=get_valid_actions(2,state)
            
        else:
             valid_moves=get_valid_actions(1,state)
        
        if len(valid_moves)==0 or depth==0:
                
                if(self.player_number==1):
                        return  get_pts(self.player_number,state[0])-get_pts(2,state[0])
               
                else:
                   return  get_pts(self.player_number,state[0])-get_pts(1,state[0])
            

        
        v = np.inf
        # print("Len2:",(valid_moves))
        
        for a in valid_moves:
            

            if(self.player_number==1):
               v = min(v,self.max_value(self.change_state(copy.deepcopy(state),a,2), alpha, beta,depth-1))
            
            else:
                 v = min(v,self.max_value(self.change_state(copy.deepcopy(state),a,1), alpha, beta,depth-1))
            
           
            # v = min(v, self.max_value(self.turn_action_to_result(copy.copy(state),a,self.player_number), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
            # print("Yedsssss444")
        return v

    # Body of alpha_beta_search:
    
    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:

        #  print("Yes1")
         valid_moves=get_valid_actions(self.player_number,state)
         depth=6
         
        #  print("Valid moves:",(valid_moves))
         alpha = -np.inf
         v=-np.inf
        #  temp_state=state.copy()
         beta = np.inf
         best_action = None
         for a in valid_moves:
                 
            if(self.player_number==1):
               v = max(v,self.min_value(self.change_state(copy.deepcopy(state),a,1), alpha, beta,depth-1))
            
            else:
                 v = max(v,self.min_value(self.change_state(copy.deepcopy(state),a,2), alpha, beta,depth-1))
                 
                
            if v > alpha:
                   alpha = v
                   best_action = a
            
        #  print("Yes2")

         return best_action
            
         
         """
           Given the current state of the board, return the next move
          This will play against either itself or a human player
          :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
           :return: action (0 based index of the column and if it is a popout move)
         """
        # Do the rest of your implementation here
        #  raise NotImplementedError('Whoops I don\'t know what to do')

    def get_expectimax_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move based on
        the Expecti max algorithm.
        This will play against the random player, who chooses any valid move
        with equal probability
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here
        raise NotImplementedError('Whoops I don\'t know what to do')
