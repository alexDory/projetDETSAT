from tensorflow.keras.models import load_model
import numpy as np
import csv
import pandas as pd

# Anglegrossier=0 #Ceci est le input du grossier en EL, faire attention la variable est plus bas au calcul de prédictions
# AngleGrossierAZ=0
# REALangle=[22,0] #Vrai valeur


def predPosition(Anglegrossier, emet, grossAZ):
    PwR=[]

    #Faire en sorte que le choix du CNN se fait selon l'angle du grossier(je connais pas le reste du code alors changer conditions if si nécessaire)
    if Anglegrossier==0:
        #CNN1: Entrainé avec les patrons [0,48], balayage EL de [1,-49]
        model = load_model('modelsCNN/CNN1_10.keras') 
        model2 = load_model('modelsCNN/CNN1_neg49_7.keras') 
        model3 = load_model('modelsCNN/CNN1_0050_div4_1.keras')
        model4 = load_model('modelsCNN/CNN1_0050_div8.keras') 
        model5 = load_model('modelsCNN/CNN1_0050_div4.keras') 
        
    elif Anglegrossier==50:
        #CNN2: Entrainé avec les patrons [74,22], balayage EL de [25,-25]
        model = load_model('modelsCNN/CNN2_2525_8.keras') 
        model2 = load_model('modelsCNN/CNN2_2525_6.keras')
        model3 = load_model('modelsCNN/CNN2_8.keras')
        model4 = load_model('modelsCNN/CNN2_11.keras')
        model5 = load_model('modelsCNN/CNN2_10.keras')

    elif Anglegrossier==90:
        #CNN3: Entrainé avec les patrons [90,50], balayage EL de [49,-1]
        model =load_model('modelsCNN/CNN3_5090_2.keras') 
        model2 = load_model('modelsCNN/CNN3_5090_3.keras')
        model3 = load_model('modelsCNN/CNN3_11.keras')
        model4 = load_model('modelsCNN/CNN3_9.keras')
        model5 = load_model('modelsCNN/CNN3_10.keras')

    else:
        print("Aucun CNN choisi")


    #Fichier du patron+ouverture du patron
    patron_csv = 'csv/CNNData.csv' #mettre le fichier du patron

    with open(patron_csv, 'r') as file:
        # Create a CSV reader
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            #print(row)
            rowfloat=[float(row[k]) for k in range(len(row))]
            PwR.append(rowfloat)
            #print(PwR) #Valider que toutes les lignes sont la


    patron=np.zeros([1,51,51])
    patron[0]=PwR[:]

    predictions = model.predict(patron)
    predictions1 = model2.predict(patron)
    predictions2 = model3.predict(patron)
    predictions3 = model4.predict(patron)
    predictions4=model5.predict(patron)

    print(predictions,predictions1,predictions2,predictions3,predictions4)
    if Anglegrossier==0:
        predArrayEL = [predictions[0][0],predictions3[0][0],predictions1[0][0],predictions2[0][0],predictions4[0][0]]   
        predArrayAZ = [predictions[0][1], predictions1[0][1],predictions3[0][1],predictions2[0][1],predictions4[0][1]] #predictions2[0][1]
        predArrayEL.sort()
        predArrayAZ.sort()
        
        EL=predictions4[0][0]
        AZ = np.mean(predArrayAZ[:3])


    elif Anglegrossier==50:
        predArrayEL = [predictions[0][0],predictions3[0][0],predictions1[0][0],predictions2[0][0],predictions4[0][0]]   
        predArrayAZ = [predictions[0][1], predictions1[0][1],predictions3[0][1],predictions2[0][1],predictions4[0][1]] #predictions2[0][1]
        predArrayEL.sort()
        predArrayAZ.sort()

        EL = predictions4[0][0]
        AZ=np.mean(predArrayAZ[3:])
        
    elif Anglegrossier==90:
        predArrayEL = [predictions[0][0], predictions1[0][0], predictions2[0][0],predictions3[0][0],predictions4[0][0]]
        predArrayAZ = [predictions[0][1], predictions1[0][1], predictions3[0][1],predictions4[0][1],predictions2[0][1]]
        predArrayEL.sort()
        predArrayAZ.sort()
        EL = predArrayEL[4]
        AZ= np.mean(predArrayAZ[2:])

    AZ += grossAZ[0]-25 
    print("Predicted Positions zero (EL, AZ):")
    print(EL,AZ)
    print(f"real:{emet[0]}")
    print(f"erreur EL:{abs(float(emet[0])-EL)}")
    print(f"erreur AZ:{abs(float(emet[1])-AZ)}")

# predPosition(50, [30,0], [-25,25])