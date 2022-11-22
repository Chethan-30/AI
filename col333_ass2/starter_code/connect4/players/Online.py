from time import sleep
from typing import Tuple, Dict
import numpy as np
from connect4.utils import get_valid_actions, Integer
from socket import *

class OnlinePlayer:
    def __init__(self, port):
        self.player_number = None
        self.type = 'online'
        self.socket = socket(AF_INET, SOCK_STREAM)
        # self.socket.connect(('127.0.0.1', 8000))
        self.socket.connect(('0.tcp.in.ngrok.io', port))
        self.socket.send("c".encode())
        self.message = None
        print("Waiting for Player...")
        self.message = self.socket.recv(1024).decode().split(" ")
        print("Ready!!!")
        for i in range(len(self.message)):
            self.message[i] = int(self.message[i])
        self.player_number = self.message[0]
        self.player_string = 'Player {}:online'.format(self.player_number)
        print("#MNPT :", self.message)
        print("You are player", 3 - self.player_number)

    def get_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        server_message = self.socket.recv(1024).decode()
        l = server_message.split(' ')
        if len(l)>1:
            return int(l[0]), l[1]=="True"
        elif (not l[0]) or l[0][0] == 'l':
            self.send_move(("e", True))
            print("Player Left")
        return None
    
    def send_move(self, move):
        try:
            if move == None:
                self.socket.send("None".encode())
            else:
                self.socket.send((str(move[0])+" "+str(move[1])).encode())
        except:
            return True

