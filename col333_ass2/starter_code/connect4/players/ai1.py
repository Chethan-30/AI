import random
import numpy as np
import copy
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

    def opponent_player(self,player):
        if player==1:
            return 2
        else :
            return 1
    
    def max_val(self,state: Tuple[np.array, Dict[int, Integer]]):
        # print("max")
        if len(get_valid_actions(self.player_number,state))==0: 
            return get_pts(self.player_number,state[0])
        val=-np.inf
        for ac in get_valid_actions(self.player_number,state):
            # l1=state[0].copy()
            # l2=state[1].copy()
            # s=(l1,l2)
            # s=state
            val=max(val,self.min_val(self.change_state(copy.deepcopy(state),ac,self.player_number)))
        return val
    def min_val(self,state: Tuple[np.array, Dict[int, Integer]]):
        # print("min")
        if len(get_valid_actions(self.opponent_player(self.player_number),state))==0: 
            return get_pts(self.player_number,state[0])
        val=np.inf
        for ac in get_valid_actions(self.opponent_player(self.player_number),state):
            # l1=state[0].copy()
            # l2=state[1].copy()
            # s=(l1,l2)
            # s=state
            val=min(val,self.max_val(self.change_state(copy.deepcopy(state),ac,self.opponent_player(self.player_number))))
        return val
    def change_state(self,state: Tuple[np.array, Dict[int, Integer]],act,play_number):
        # if reverse ==0:
            if act[1]==False:
                for i in range(len(state[0])-1,-1,-1):
                    if state[0][i][act[0]]==0:
                        state[0][i][act[0]]=play_number
                        return state
                return state
            else :
                for i in range(len(state[0])-1,0,-1):
                    state[0][i][act[0]]=state[0][i-1][act[0]]

                state[0][0][act[0]]=0
                state[1][play_number].decrement()
                
                return state
        # else :
        #     if act[1]==False:
        #         for i in range(len(state[0])):
        #             if state[0][i][act[0]]==play_number:
        #                 state[0][i][act[0]]=0
        #                 break
                
        #     else :
        #         for i in range(len(state[0])-1,0,-1):
        #             state[0][i][act[0]]=state[0][i-1][act[0]]

        #         state[0][0][act[0]]=0
        #         state[1][play_number].decrement()
                
        #         return state

    
    
    
    
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
        :return: action (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here
        # moves=get_valid_actions(self.player_number,state)
        # d={}
        
        # for move in moves:
           
        #     d[move]=self.min_val(copy.deepcopy(state))
            
        # v=list(d.values())
        # k=list(d.keys())    

        # return k[v.index(max(v))]
        return
    def expectimax_change_state(self,state,action,play_number):
        if action[1]==False:
            n=0
            for i in range(len(state[0])):
                if state[0][i][action[0]]==0:
                    n=i
            state[0][n][action[0]]=play_number
                   
        else:
            for i in range(len(state[0])-1,0,-1):
                state[0][i][action[0]]=state[0][i-1][action[0]]

            state[0][0][action[0]]=0
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
        :return: action (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here
        # var2=len(state[0][0])
        k=0
        if self.player_number==1:
            k=2
        else :
            k=1
        moves=get_valid_actions(self.player_number,state)
        v=-np.inf
        action=None
        if get_pts(self.player_number,state[0])==0 and get_pts(k,state[0])==0 and state[0][len(state[0])-1][len(moves)//2]==0:
            var1=len(moves)//2

            print(moves[var1])
            return moves[var1]
        if get_pts(self.player_number,state[0])==0 and get_pts(k,state[0])==0:
            var1=len(state[0][0])//2
            if state[0][len(state[0])-2][var1]!=0:
                var1=var1-1
            return moves[var1]

        

        for act in moves:
            # print("##############################")
            
            s=self.expectimax_change_state(copy.deepcopy(state),act,self.player_number)
            # print(act)
            # print(s)
            z1=get_pts(k,state[0])-get_pts(k,s[0])
            z2=get_pts(self.player_number,s[0])-get_pts(k,s[0])
            z3=get_pts(self.player_number,s[0])-get_pts(self.player_number,state[0])

            
            if z1+z2+z3>v:
                v=z1+z2+z3
                action=act
        # if v<0:
        #     print(moves)
        #     print(v)
        #     print(state)
        #     print(action)
            # if v<0:
            #     z=get_pts(self.player_number,s[0])


        
        # print(v)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        return action


            

