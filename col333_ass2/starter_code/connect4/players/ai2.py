import random
import numpy as np
import copy
import time
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer


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
    def max_val(self,state: Tuple[np.array, Dict[int, Integer]],a,b,height):
        k=0
        if self.player_number==1:
            k=2
        else :
            k=1
        moves=get_valid_actions(self.player_number,state)
        if  height==0: 
            return get_pts(self.player_number,state[0])-get_pts(k,state[0])
        if len(moves)==0: 
            return get_pts(self.player_number,state[0])-get_pts(k,state[0])
        parameter=-np.inf
        for act in get_valid_actions(self.player_number,state):
            parameter=max(parameter,self.min_val(self.change_state(self.player_number,copy.deepcopy(state),act),a,b,height-1))
            if parameter>=b :
                return parameter
            a=max(a,parameter)
        return parameter

    def min_val(self,state: Tuple[np.array, Dict[int, Integer]],a,b,height):
        k=0
        if self.player_number==1:
            k=2
        else :
            k=1
        moves=get_valid_actions(k,state)
        if  height==0: 
            return get_pts(self.player_number,state[0])-get_pts(k,state[0])
        if len(moves)==0: 
            return get_pts(self.player_number,state[0])-get_pts(k,state[0])
        parameter=+np.inf
        for act in moves:
            parameter=min(parameter,self.max_val(self.change_state(k,copy.deepcopy(state),act),a,b,height-1))
            if parameter<=a :
                return parameter
            b=min(b,parameter)
        return parameter
    def change_state(self,play_number,state: Tuple[np.array, Dict[int, Integer]],step):
        if step[1]==False:
            n=0
            for i in range(len(state[0])):
                if state[0][i][step[0]]==0:
                    n=i
            state[0][n][step[0]]=play_number
        else:
            for i in range(len(state[0])-1,0,-1):
                state[0][i][step[0]]=state[0][i-1][step[0]]

            state[0][0][step[0]]=0
            state[1][play_number].decrement()
        return state
        
    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
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
        :return: step (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here
        k=0
        if self.player_number==1:
            k=2
        else :
            k=1
        height=4
        moves=get_valid_actions(self.player_number,state)
        a=-np.inf
        b=np.inf
        if len(moves)==0: 
            return get_pts(self.player_number,state[0])-get_pts(k,state[0])
        parameter=-np.inf
        step=moves[0]
        for act in moves:
            parameter=max(parameter,self.min_val(self.change_state(self.player_number,copy.deepcopy(state),act),a,b,height-1))
            if parameter>a :
                a=parameter
                step=act
        return step 
             
    def expectimax_max_val(self,state,initial,height):
        k=0
        if self.player_number==1:
            k=2
        else :
            k=1
        moves=get_valid_actions(self.player_number,state)
        pressure=((time.time())-initial)-(self.time-3)
        if  height==0 or pressure>0:
            print(height) 
            # return get_pts(self.player_number,state[0])-get_pts(k,state[0])
            
            return get_pts(self.player_number,state[0])-get_pts(k,state[0])
            
        
        if len(moves)==0: 
            return get_pts(self.player_number,state[0])-get_pts(k,state[0])
        parameter=-np.inf
        for act in moves:
            parameter=max(parameter,self.expectimax_val(self.expectimax_change_state(copy.deepcopy(state),act,self.player_number),initial,height-1))
        return parameter
    def expectimax_val(self,state,initial,height):
        k=0
        if self.player_number==1:
            k=2
        else :
            k=1
        moves=get_valid_actions(k,state)
        pressure=((time.time())-initial)-(self.time-3)
        if  height==0 or pressure>0: 
            print(height) 
            return get_pts(self.player_number,state[0])-get_pts(k,state[0])
            
        
        if len(moves)==0: 
            return get_pts(self.player_number,state[0])-get_pts(k,state[0])
        parameter=0
        # moves=get_valid_actions(k,state)
        p=1/len(moves)
        for act in moves:
            parameter=parameter+(p*self.expectimax_max_val(self.expectimax_change_state(copy.deepcopy(state),act,k),initial,height-1))
        return parameter

    def expectimax_change_state(self,state,step,play_number):
        if step[1]==False:
            n=0
            for i in range(len(state[0])):
                if state[0][i][step[0]]==0:
                    n=i
            state[0][n][step[0]]=play_number
        else:
            for i in range(len(state[0])-1,0,-1):
                state[0][i][step[0]]=state[0][i-1][step[0]]
            state[0][0][step[0]]=0
            state[1][play_number].decrement()
        return state
    

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
        :return: step (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here
        k=0
        if self.player_number==1:
            k=2
        else :
            k=1
        height=100
        moves=get_valid_actions(self.player_number,state)
        if len(moves)==0: 
            return get_pts(self.player_number,state[0])-get_pts(k,state[0])
        parameter=-np.inf
        step=moves[0]
        initial=time.time()
        for act in moves:
            z=self.expectimax_val(self.expectimax_change_state(copy.deepcopy(state),act,self.player_number),initial,height-1)
            if z>parameter:
                parameter=z
                step=act

        return step
