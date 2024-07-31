import serial
import socket
import time
from BBoard_control import SendCmdThenWaitRSP
import numpy as np
import io
import csv
from Read_txt import *
import struct


    
"""
@brief: Fonction de steering du faisceau 
Cette fonction définit l'angle de pointage du faisceau en EL

@param: angle_deg : Angle vers lequel pointer
@param: nChannel : Nombre de canaux a activer
@param: antenna_socket : Socket du Bboard
@param: filename : CSV des phases des canaux
"""
def steer(angle_deg, nChannel, antenna_socket, filename):
    if nChannel == 4 :
        ch = "0,0,0,0,"
    else:
        ch = "0,0,1,1,"
        filename = "csv/PhasesAntenneGrossier.csv"
    csv_file = open(filename, newline='')
    csv_reader = csv.reader(csv_file, delimiter=',')

    for  i, row in enumerate(csv_reader):
        if angle_deg == float(row[0]):
            SendCmdThenWaitRSP(antenna_socket,"MODULE_CTRL_ 1,2,0,"
            +ch+str(row[1])+","+str(row[2])+","+str(row[3])
            +","+str(row[4])+",0,0,0,0,0 \n\r",0)

            break
    


"""
@brief: Fonction de lecture du powerDetector 
Cette fonction lit la puissance transmise par le powerDetector

@param: power_detector : Port serie 

@return: p : Puissance mesuree
"""
def readPower(power_detector):
    try:
        p= []
        power_detector.flush()
        power_buffer = power_detector.read(64)

        for i in range(0, len(power_buffer), 4):
            float_bytes = power_buffer[i:i+4]
            float_value = struct.unpack('f', float_bytes)[0]
            p.append(float_value)

        p = np.array(p)
        p = p.mean()
        return p
    
    except:
        # print("Crashed, trying again")
        return readPower(power_detector)