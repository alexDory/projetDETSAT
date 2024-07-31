import csv
import pandas as pd
import random
import numpy as np

def csvReadGrossier(file_path):
    try:
       
        with open(file_path, 'r', encoding='utf-8-sig', newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            tableau = list(reader)
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
        return None, None, None
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du fichier : {e}")
        return None, None, None
 
    if len(tableau) < 3:
        return None, None, None
 
    if len(tableau[0]) < 2 or len(tableau[1]) < 2 or len(tableau[2]) < 2:
        return None, None, None


    valeurs = [float(ligne[1]) for ligne in tableau]
    max_valeur = max(valeurs)
  
    if max_valeur == float(tableau[0][1]):
        val_min, val_max = -50, 0
   
    elif max_valeur == float(tableau[1][1]):
        val_min, val_max = -25, 25
    
    elif max_valeur == float(tableau[2][1]):
        val_min, val_max = 0, 50
    else:
        val_min, val_max = None, None
 
    return max_valeur, val_min, val_max

def csvReadGrossier3D(max_row_value, max_column_value):

    val_min_ele= max_row_value-25
    val_max_ele =max_row_value+25
    val_min_azi=max_column_value-25
    val_max_azi = max_column_value+25
 
    return  val_min_ele,val_max_ele,val_min_azi,val_max_azi


def remplir_csv(valeurs):
    premiere_colonne = [-25, 0, 25]
    chemin_fichier = "csv/valeurs.csv"

    with open(chemin_fichier, mode='w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        
        # Écrire la première ligne avec les valeurs
        premiere_ligne = [''] + [-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150]
        writer.writerow(premiere_ligne)
        print("La première ligne a été écrite avec succès.")
        
        for i in range(len(premiere_colonne)):
            ligne = [premiere_colonne[i]]
            for j in range(len(valeurs)):
                ligne.append(valeurs[j][i][1])
            writer.writerow(ligne)
    return chemin_fichier

def trouver_max_dans_csv(chemin_fichier):
    max_value = float('-inf')
    max_row_index = None
    max_column_index = None
    max_row_value = None
    max_column_value = None

    with open(chemin_fichier, mode='r', newline='') as fichier_csv:
        reader = csv.reader(fichier_csv)
        header_row = next(reader)  
        data_rows = list(reader)

        for row_index, row in enumerate(data_rows, start=1):
            for column_index, value in enumerate(row[1:], start=1):  # Ignorer la première colonne
                valeur = float(value)
                if valeur > max_value:
                    max_value = valeur
                    max_row_index = row_index
                    max_column_index = column_index

        max_row_value = float(data_rows[max_row_index - 1][0])  # première colonne
        max_column_value = float(header_row[max_column_index])  # première ligne
    
    a,b,c,d=csvReadGrossier3D(max_row_value,max_column_value)
    print("La valeur maximale se trouve à la ligne", max_row_index, "et à la colonne", max_column_index)
    print("La valeur correspondante dans la première colonne est :", max_row_value)
    print("La valeur correspondante dans la première ligne est :", max_column_value)
    print("La valeur maximale est :", max_value) 
    print(a,b,c,d)
    return [[int(a),int(b)]],[[int(c),int(d)]]
  
    
  
  