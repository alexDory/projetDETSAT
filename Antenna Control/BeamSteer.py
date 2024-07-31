from IntegratedDetection import *
from BBoard_control import SendCmdThenWaitRSP
import matplotlib as plt
import numpy as np
import random
from grossier import *
import serial

'''
@brief: Pointe le faisceau en EL et collecte la puissance
Cette fonction permet de mesurer la puissance pour une pos. EL 
donnée.

@return: ele : EL
@return: power : Puissance mesuree

'''
def partialGetPower(ele, power_detector, antenna_socket, nChannel, filename):
    power_detector.flushInput()
    steer(ele, nChannel, antenna_socket, filename)
    power = readPower(power_detector)

    return [ele, power]


'''
@brief: Initialisation de la connexion
Cette fonction permet d'initialiser la communication TCP
Ethernet avec le BeamFormer (Bboard)
'''
def initTCP():
    #Commande de l'antenne
    RECV_TIMEOUT = 15
    IP = "192.168.100.112"
    PORT = 5025
    try:
        TCPsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPsocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        TCPsocket.settimeout(RECV_TIMEOUT)
        TCPsocket.connect((IP, PORT))
        SendCmdThenWaitRSP(TCPsocket,"INIT 0 \n\r",0)
        SendCmdThenWaitRSP(TCPsocket,"TDD 2 \n\r",0) # TDD 1 in TX, 2 in RX
        return TCPsocket
    except socket.error as msg:
            print('[Init_TCP_client]Exception : %s' % (msg))


'''
@brief: Setter parametres Grossier
Cette fonction permet de regler les parametres permettant
d'effectuer un balayage grossier.

@return: anglesEL : Intervalles EL
@return: canaux : Nombre de channels du BeamFormer utilises
@return: anglesAZ : Intervalles AZ
'''
def modeGrossier():

    anglesEL = [[-26,-26],[-25,-25],[-24,-24], [-1,-1], [0,0], [1,1], [24, 24],[25,25],[26,26]]
    anglesAZ = [[-180,-180],[30,30],[30,30],[30,30],[30,30],[30,30],[30,30],[30,30],[30,30],[30,30],[30,30],[30,30]]
    canaux = 2
    return anglesEL, canaux, anglesAZ

'''
@brief: Setter parametres DataCollect
Cette fonction permet de regler les parametres permettant
d'effectuer une collect de data pour le mode training.

@return: anglesEL : Intervalles EL
@return: canaux : Nombre de channels du BeamFormer utilises
@return: anglesAZ : Intervalles AZ
'''   
def modeFin():
    anglesAZ = [[-47, 47]]
    anglesEL = [[-50, 49]]
    canaux = 4

    return anglesEL, canaux, anglesAZ

'''
@brief: Setter parametres DataValidation
Cette fonction permet de regler les parametres permettant
d'effectuer une collect de data pour le mode validation.

@return: anglesEL : Intervalles EL
@return: canaux : Nombre de channels du BeamFormer utilises
@return: anglesAZ : Intervalles AZ
''' 
def modeFinAleatoire():

    anglesAZ = [[-25, 25]]
    anglesEL = [[-2,49]] #Depend de la pos de l'emetteur, a ameliorer.
    canaux = 4

    return anglesEL, canaux, anglesAZ


def clearCsv(filename):
     f = open(filename, 'w+')
     f.close()

def writeCsv(ps, f):
    power_writer = csv.writer(f, delimiter=',')
    for row in ps: 
        f.write(f"{row[0]},{row[1]}\n")
        

def writeCsvTrain(ps, elem):
    all = []
    with open('csv/testTraining.csv', 'r') as f:
        power_reader = csv.reader(f, delimiter=',')
        for index,row in enumerate(power_reader):
            row.append(ps[index])
            all[index]= row
    with open('csv/testTraining.csv', 'w') as f:
        power_writer = csv.writer(f, delimiter=',')
        power_writer.writerows(all)
    

'''
@brief: Main de la fonction de balayage EL
Cette fonction permet pour une plage d'angles EL
de balayer sur toute cette plage

@return: ps : vecteur des puissances sur l'intervalle
'''
def steerMain(steeringAngle, nChannel) :
    ps = []
    
    # print("Starting")
    power_detector = serial.Serial(port = 'COM4', baudrate = 9600)
    TCPsocket = initTCP()

    for range in steeringAngle:
        aStart = range[0]
        aEnd = range[1]
        aStep = aEnd - aStart + 1
        a = np.linspace(aStart, aEnd, aStep)
        
        for i, ai in enumerate(a):
            ps.append(partialGetPower(ai, power_detector, TCPsocket, nChannel, filename = 'csv/PhasesAntenne.csv'))
            
    # print('Ending')
    return ps

 