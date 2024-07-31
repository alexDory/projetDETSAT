# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 14:43:24 2023

@author: DETSAT
"""
import socket 
import time
from Read_txt import *
import re

    
def SendCmdThenWaitRSP(sock, cmd, user_delay):
    BUF_SIZE = 1024
    try:
        sock.sendall(cmd.encode('utf-8'))
        recv_data = sock.recv(BUF_SIZE)
        time.sleep(user_delay)
        return recv_data
    except socket.error as msg:
        print('[SendCmdThenWaitRSP]Exception : % s' % (msg))
        return None
    
if __name__ == '__main__':
    RECV_TIMEOUT = 15
    IP = "192.168.100.111"
    PORT = 5025
    filename = 'Antenna_control_phase_steps_1deg_resolution.txt'
    somme = Read_txt(filename)
    try:
        TCPsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPsocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        TCPsocket.settimeout(RECV_TIMEOUT)
        TCPsocket.connect((IP, PORT))
        SendCmdThenWaitRSP(TCPsocket,"INIT 0 \n\r",0)
        SendCmdThenWaitRSP(TCPsocket,"TDD 2 \n\r",0) # TDD 1 in TX, 2 in RX
        SendCmdThenWaitRSP(TCPsocket,"TC_MODULE_CTRL_ 1,0,8,6,2,11 \n\r",0)
        for ps_step in range(64):
            SendCmdThenWaitRSP(TCPsocket,"MODULE_CTRL_ 1,2,0,0,0,0,0,0,0,"+str(ps_step)+",0,0,0,0,0,0 \n\r",0)
    except socket.error as msg:
                    print('[Init_TCP_client]Exception : %s' % (msg))
 
    