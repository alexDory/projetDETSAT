import PySimpleGUI as sg
import numpy as np
import BeamSteer as steer
import serial
import csvWriter as csvw
import time
import predictions_positions
import grossier
from motorControl import motorCntDegReel
from motorControl import motorCntDegError

sg.theme('BlueMono') 


'''
@brief: Setter de la postion de l'metteur
Cette fonction permet d'editer la position EL de l'emetteur
pour ecriture dans les csv

@param: elem position de l'emetteur  
@return: array de la position 
'''

def setElem(elem):

    posel = [None, elem, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
            None, None, None, None]
    
    return posel


'''
@brief: Sequence de balayage raffine
Cette fonction permet de balayer de [-25,25] AZ et de [X,X] EL
afin de récolter la data pour l'estimation finale de la position
elem par le CNN

@param: anglesEL : plage d'angles EL determinee par le balayage Grossier
@param: anglesAZ : plage d'angles AZ
@param: nChannel : Nombre de canaux de l'antenne a utiliser  
'''
def startRaffine(anglesEL, anglesAZ, nChannel):

    dernierPosMoteur = motorCntDegError(0, 0, arduino)
    steer.clearCsv(filename="csv/CNNData.csv")
    for range in anglesAZ:
        aStart = range[0]
        aEnd = range[1]
        aStep = aEnd - aStart + 1
        a = np.linspace(aStart, aEnd, aStep)

        for i,az in enumerate(a):

            dernierPosMoteur = motorCntDegError(dernierPosMoteur, az, arduino)
            ps = steer.steerMain(anglesEL, nChannel)

            if i == 0:   
                csvw.writeCsvLearning(input_file="csv/CNNData.csv",output_file="csv/CNNData.csv",new_column_data=list(zip(*ps))[1], condition="append")

            else:
                csvw.writeCsvLearning(input_file="csv/CNNData.csv",output_file="csv/CNNData.csv",new_column_data=list(zip(*ps))[1])

            # Graphs.graph(ps)

    dernierPosMoteur = motorCntDegError(dernierPosMoteur, 0, arduino)


'''
@brief: Sequence de balayage de Validation
Cette fonction permet de balayer de [-25,25] AZ et de [X,X] EL
Elle permet de recolter la data de validation pour le CNN

@param: anglesEL : plage d'angles EL
@param: anglesAZ : plage d'angles AZ
@param: nChannel : Nombre de canaux de l'antenne a utiliser  
'''
def startValidation(anglesEL, anglesAZ, nChannel):

    dernierPosMoteur = motorCntDegError(0, 0, arduino)
            
    for range in anglesAZ:
        aStart = range[0]
        aEnd = range[1]
        aStep = aEnd - aStart + 1
        a = np.linspace(aStart, aEnd, aStep)
        for i,az in enumerate(a):

            dernierPosMoteur = motorCntDegError(dernierPosMoteur, az, arduino)
            ps = steer.steerMain(anglesEL, nChannel)

            if i == 0:   
                csvw.writeCsvLearning(input_file="csv/testTraining1.csv",output_file="csv/testTraining1.csv",new_column_data=list(zip(*ps))[1], condition="append")

            else:
                csvw.writeCsvLearning(input_file="csv/testTraining1.csv",output_file="csv/testTraining1.csv",new_column_data=list(zip(*ps))[1])

            # Graphs.graph(ps)
        csvw.writeCsvLearning(input_file="csv/testTraining1.csv",output_file="csv/testTraining1.csv",new_column_data=setElem(range[0]))
        csvw.writeCsvLearning(input_file="csv/testTraining1.csv",output_file="csv/testTraining1.csv",new_column_data=setElem(range[1]))


    csvw.writeCsvLearning(input_file="csv/testTraining1.csv",output_file="csv/testTraining1.csv",new_column_data=setElem(elem))

    dernierPosMoteur = motorCntDegError(dernierPosMoteur, 0, arduino)


'''
@brief: Sequence de balayage d'entrainement
Cette fonction permet de balayer de [-47,47] AZ et de [-50,49] EL
Elle permet de recolter la data d'entrainement pour le CNN

@param: anglesEL : plage d'angles EL
@param: anglesAZ : plage d'angles AZ
@param: nChannel : Nombre de canaux de l'antenne a utiliser  
'''
def startDataCollect(anglesEL, anglesAZ, nChannel):

    dernierPosMoteur = motorCntDegReel(0, 0, arduino)
            
    for range in anglesAZ:
        aStart = range[0]
        aEnd = range[1]
        aStep = aEnd - aStart + 1
        a = np.linspace(aStart, aEnd, aStep)
        for i,az in enumerate(a):

            dernierPosMoteur = motorCntDegReel(dernierPosMoteur, az, arduino)
            ps = steer.steerMain(anglesEL, nChannel)

            if i == 0:   
                csvw.writeCsvLearning(new_column_data=list(zip(*ps))[1], condition="append")

            else:
                csvw.writeCsvLearning(new_column_data=list(zip(*ps))[1])

            # Graphs.graph(ps)
    csvw.writeCsvLearning(new_column_data=setElem(elem))
    dernierPosMoteur = motorCntDegReel(dernierPosMoteur, 0, arduino)


'''
@brief: Sequence de balayage grossier
Cette fonction permet de balayer de [-180,150] AZ par incrément 
de 30 deg par rapport au zero du moteur.

Balaye a [-25,-25], [0,0], [25,25] EL.

Elle permet de recolter la data pour l'estimation grossiere
de la position de l'emetteur dans l'espace.

@param: anglesEL : plage d'angles EL
@param: anglesAZ : plage d'angles AZ
@param: nChannel : Nombre de canaux de l'antenne a utiliser

@return: grossEL : Intervalle de prediction de la pos. EL
@return: grossAZ : Intervalle de prediction de la pos. AZ
'''
def startGrossier(anglesEL, anglesAZ, nChannel):

    time_start2=time.time()
    dernierPosMoteur = motorCntDegReel(0, 0, arduino)
    val=[]

    for range in anglesAZ:
        aStart = range[0]
        aEnd = range[1]
        aStep = aEnd - aStart + 1
        a = np.linspace(aStart, aEnd, aStep)
        for i, az in enumerate(a):

            motorCntDegReel(dernierPosMoteur, az, arduino)
            print("AZ = " + str(az))
            print("Pos moteur = " + str(dernierPosMoteur))

            if az == -180:   
                time.sleep(10)
            else:
                time.sleep(5)
            
            ps1 = steer.steerMain(anglesEL, nChannel)
            temp = []
            for element in ps1:
                if element[0] in [-25, 0, 25]:
                    temp.append(element)

            if temp:
                val.append(temp)
            print("Les données ont été écrites avec succès.")

    chemin_fichier=grossier.remplir_csv(val)
    gross_EL, gross_AZ = grossier.trouver_max_dans_csv(chemin_fichier)
    motorCntDegReel(dernierPosMoteur, -150, arduino)
    time.sleep(10)
    time_stop2 = time.time()
    time_total2 = time_stop2 - time_start2
    print(f"Le temps de detection grossier est : {time_total2*1000:.3f} milliseconde")

    return gross_EL, gross_AZ


'''
@brief: Interface graphique de controle
Cette fonction permet de :
- Input la position EL de l'emetteur
- Controler le 0 AZ du recepteur
- Selectionner le mode sur lequel lancer
  le systeme (DataCollect, DataTraining, Detection)
- Commenter lignes 215-216 et decomenter ligne 220 pour afficher l'interface 
  sans etre connecter au systeme.
'''
if __name__ == "__main__" :
    global arduino
    # arduino = serial.Serial(port='COM6', baudrate=115200, timeout=.1)
    # dernierPosMoteur = motorCntDegError(0, 0, arduino)
    global ps
    global elem

    arduino = 0
 
    col1 = [[sg.Text('Select Mode : ')], [sg.Combo(['Detection',"DataCollect","DataTraining"],key='-MODE-')],[sg.Button('Go'), sg.Cancel()]]
    col2 = [[sg.Text('Pos. motor zero : ')],[sg.Input(key='-AZ-',size=(13,1))],[sg.Button('Ok',key= '-OKAZ-')]]
    col3 = [[sg.Text('EL emetteur : ')], [sg.Input(key='-ELEM-', size=(13,1))],[sg.Button('Ok',key= '-OKELEM-')]]
    layout = [[sg.Column(col1),sg.VSeparator(),sg.Column(col2),sg.VSeparator(),sg.Column(col3)]]
    steeringAngle = None
    window = sg.Window('DETSAT', layout)
    
    while True:
        event, values = window.read()

        if values['-MODE-'] == "Detection":
            steeringAngle, nChannel, anglesAZ = steer.modeGrossier()

        elif values['-MODE-'] == "DataCollect":
            steeringAngle, nChannel, anglesAZ = steer.modeFin()
        
        elif values['-MODE-'] == "DataTraining":
            steeringAngle, nChannel, anglesAZ = steer.modeFinAleatoire()

        if event == "Go" and not steeringAngle is None:
            time_start1=time.time()

            if values['-MODE-'] == "DataTraining":
                startValidation(steeringAngle, anglesAZ, nChannel)
            elif values['-MODE-'] == "DataCollect" :
                startDataCollect(steeringAngle, anglesAZ, nChannel)
            else:
                gross_EL, gross_AZ = startGrossier(steeringAngle, anglesAZ, nChannel)

                if gross_EL[0][0] == -50:
                    startRaffine([[-50,1]],gross_AZ,4)
                    predictions_positions.predPosition(0,[elem,0],0)

                elif gross_EL[0][0] == -25:
                    startRaffine([[-26,25]],gross_AZ,4)
                    predictions_positions.predPosition(50,[elem,0],0)

                else :
                    startRaffine([[-2,49]],gross_AZ,4)
                    predictions_positions.predPosition(90,[elem,0],0)

            time_stop1 = time.time()
            time_total1 = time_stop1 - time_start1
            print(f"Le temps de detection total est : {time_total1*1000:.3f} milliseconde")

        elif steeringAngle is None:
            print("You must choose a mode first !")

        if event == "-OKAZ-":
            if values['-AZ-'][-1] not in ('0123456789'):
                sg.popup("Only digits allowed")
                window['-AZ-'].update(values['-AZ-'][:-1])
            else:
                motorCntDegReel(dernierPosMoteur, float(values['-AZ-']), arduino)  
        if event == "-OKELEM-":
            if values['-ELEM-'][-1] not in ('0123456789') or values['-ELEM-'] == '':
                sg.popup("Error in ELEM input")
                window['-ELEM-'].update(values['-ELEM-'][:-1])
            else:
                elem = values['-ELEM-']
        if event == "Cancel":
            break
        