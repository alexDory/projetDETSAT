import numpy as np
import csv
import pandas as pd

# Replace 'your_file.csv' with the actual path to your CSV file
file_path = 'D:/python/testTraining2.csv'   #Patrons de train
file_path5='D:/python/aleatoire47472.csv'   #Patrons de validation
file_path6='D:/python/2222DATA.csv'         #Patron simple pour prédiciton
file_path7='D:/python/0neg22DATA.csv'       #Patron simple pour prédiciton
file_path2='D:/python/90neg22DATA.csv'      #Patron simple pour prédiciton

PwR=[]
PwRDATA=[]
data6220=[]
aleatoiresoloX=[]
aleatoiresoloY=[]
aleatoire4747=[]
data7009=[]
# Open the CSV file and read its contents
with open(file_path, 'r') as file:
    # Create a CSV reader
    csv_reader = csv.reader(file)
        
    # Iterate over each row in the CSV file
    for row in csv_reader:
        #print(row)
        rowfloat=[float(row[k]) for k in range(len(row)-1)]
        try:
            rowfloat.append(float(row[-1]))
        except:
            pass
        PwR.append(rowfloat)
    

with open(file_path2, 'r') as file2:
    # Create a CSV reader
    csv_reader = csv.reader(file2)
    headers = next(csv_reader)
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        rowfloat=[float(row[k]) for k in range(len(row)-1)]
        try:
            rowfloat.append(float(row[-1]))
        except:
            pass
        PwRDATA.append(rowfloat)
        

with open(file_path5, 'r') as file2:
    # Create a CSV reader
    csv_reader = csv.reader(file2)
    headers = next(csv_reader)
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        rowfloat=[float(row[k]) for k in range(len(row)-1)]
        try:
            rowfloat.append(float(row[-1]))
        except:
            pass
        aleatoire4747.append(rowfloat)

        
with open(file_path6, 'r') as file2:
    # Create a CSV reader
    csv_reader = csv.reader(file2)
    headers = next(csv_reader)
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        rowfloat=[float(row[k]) for k in range(len(row)-1)]
        data6220.append(rowfloat)

with open(file_path7, 'r') as file2:
    # Create a CSV reader
    csv_reader = csv.reader(file2)
    headers = next(csv_reader)
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        rowfloat=[float(row[k]) for k in range(len(row)-1)]
        data7009.append(rowfloat)
    
#PARAMÈTRES(To modify accordingly)
REL=99                  #Size of patron EL complet
anglesEL=[49,-49]       #Range complet du balayage EL
RAZ=51                  #Size of patron AZ voulu (impair)
EAZ=4                   #steps position of Emitter
rangeCNN1=[1,-49]       #Choix du range balayage EL pour CNN1
rangeCNN2=[25,-25]      #Choix du range balayage EL pour CNN1
rangeCNN3=[49,-1]       #Choix du range balayage EL pour CNN1

#SortingData functions
def CheckIfInRange(debut,fin,angle):
    """
    In: 
        Début/fin:range de balayage voulu
        angle: angle du balayage
    Out: 
        1: in range
        0: out of range
    """
    if angle<=debut and angle>=fin:
        return 1
    else:
        return 0

def SelectionPatron(Matrice):
    """
    Enleve les patrons nul de la matrice en entrée
    """   
    # Check if any element in each matrix is non-zero
    try:
        non_zero_matrices = np.any(Matrice, axis=(1, 2))
    except:
        non_zero_matrices = np.any(Matrice, axis=(1))
    # Filter out matrices with all zeros
    result = Matrice[non_zero_matrices]
    return result

def Sortedmatrix(PwR,REL,RAZ,EAZ):
    """
    In: Raw Data
    Outputs: Matrice du Data pour un CNN et matrice de réponse de la position de l'émetteur
    """

    #Settings
    hRAZ=int((RAZ-1)/2)                                                        #Moitié d'un patron
    npatron=int((len(PwR)/REL)*((len(PwR[1])-2*hRAZ)//EAZ+1))                  #Calcule le nombre de patrons
    matrices = np.zeros([npatron,REL,RAZ])                                      #initialisation de la matrice avec tout les patrons
    m=0                                                                         #itérateur patrons
    bound=int((len(PwR[1])-1)/2)
    AngleAZ= list(range(-bound, bound + 1))                                     #angles AZ (le centre est fixé à 0)
    angles=np.zeros([npatron,2])                                                #Vecteur qui sauvegarde les angles[EL,AZ] de chaque patron

    # Iterate over rows with a step size of 3
    for i in range(0, len(PwR), REL):
        # Extract 3 rows to create a matrix
        matrix = PwR[i:i+REL]
        # Create a 3x3 matrix with repeated columns
        for j in range(hRAZ, len(PwR[1])-hRAZ, EAZ):
            angles[m][0]=float(matrix[0][-1])
            angles[m][1]=AngleAZ[-(j+1)] 
            patron= [matrix[k][j-hRAZ:j+hRAZ+1] for k in range(0,len(matrix))]
            # Append the matrix to the list
            matrices[m]=patron[:]
            m+=1
        
    return angles, matrices
    

def selectCNN(matricePatron,anglesEL,rangeCNN):
    """
    Choix des patrons dans le range du CNN voulu
    """
    nPatron,rows,col=matricePatron.shape
    CNN = np.zeros((nPatron,abs(rangeCNN[0])+1+abs(rangeCNN[-1]),col))
    listanglesEL=list(range(anglesEL[-1], anglesEL[0]+1))
    end=rows

    for i in range(nPatron):
        start=0
        
        for j in range(rows-1):
            InRange=CheckIfInRange(rangeCNN[0],rangeCNN[-1], listanglesEL[j])
            if InRange==1 and start==0:
                init=j
                start=1
            elif InRange==0 and start==1:
                end=j
                start=0

        CNN[i]=matricePatron[i][init:end]
                
    CNN=SelectionPatron(CNN)
    return CNN

Matriceangles,matricePatron=Sortedmatrix(PwR,REL,RAZ,EAZ)


DATAangle,TESTDATA=Sortedmatrix(PwRDATA,REL,RAZ,EAZ=25)
DATAangle2,TESTDATA62=Sortedmatrix(data6220,REL,RAZ,EAZ=25)
DATAangle3,TESTDATA70=Sortedmatrix(data7009,REL,RAZ,EAZ=25)

TESTDATA=selectCNN(TESTDATA,anglesEL,rangeCNN3)
DATAangle=[[46,22]]
TESTDATA62=selectCNN(TESTDATA62,anglesEL,rangeCNN3)
DATAangle2=[[22, 22]]
TESTDATA70=selectCNN(TESTDATA70,anglesEL,rangeCNN3)
DATAangle3=[[0,-22]]
CNN1=selectCNN(matricePatron,anglesEL,rangeCNN1)
CNN2=selectCNN(matricePatron,anglesEL,rangeCNN2)
CNN3=selectCNN(matricePatron,anglesEL,rangeCNN3)




anglesValidation,PatronValidation=Sortedmatrix(aleatoire4747,REL,RAZ,EAZ=4)
patronsaleatoire=selectCNN(PatronValidation,anglesEL,rangeCNN3)

#Choix des patrons pour entrainement et validation: À modifier
print(Matriceangles[:168])
Matriceangles=Matriceangles[:168]
CNN3=CNN3[:168]
print((anglesValidation[0:24],anglesValidation[132:]))
anglesValidation=np.concatenate((anglesValidation[0:24],anglesValidation[132:]))
patronsaleatoire=np.concatenate((patronsaleatoire[0:24],patronsaleatoire[132:]))

Y=np.concatenate((Matriceangles,anglesValidation))
X=np.concatenate((CNN3,patronsaleatoire))


print(f"CNN1:{CNN1.shape}")
print(f"data:{TESTDATA.shape}")
print(f"dataangle:{DATAangle}")
print(f"CNN2:{len(CNN2)}")
print(f"CNN3:{len(CNN3)}")
print(f"angles Emetteur:{Matriceangles.shape}")

