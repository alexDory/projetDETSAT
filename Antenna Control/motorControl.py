import serial
import time



def sendVariableArduino(variable_value, arduino):
    msg = str(variable_value)
    arduino.write(bytes(msg, 'utf-8'))
    time.sleep(0.05)


def motorCntDegReel(position_actu, cnt_deg_exact, arduino):  
      
    deg_exact = round(cnt_deg_exact * 6400 / 360)
    envoyer = deg_exact - position_actu
    position_actu = position_actu + envoyer
    sendVariableArduino(envoyer, arduino)  
    print("Moteur"+str(position_actu))  
    time.sleep(1)
    return position_actu

    
# Fonction pour trouver le nombre de pas à bouger le moteur pour lui positionner à la position cnt_deg_exact (en degrés)
def motorCntDegError(dernier_position_deg_exact, cnt_deg_exact, arduino):
    # global dernier_position_deg_exact                 # dernier_position_deg_exact doit commencer à 0 au tout début
    nb_pas = 18
    cnt_pas_reel = 0
    cnt_deg_reel = 0
    erreur_cnt_deg = 0
    cnt_deg_exact_calcul_erreur = 0
    current_cnt_deg_exact = cnt_deg_exact - dernier_position_deg_exact

    if current_cnt_deg_exact >= 0:
        cnt_pas_reel = cnt_pas_reel + nb_pas*current_cnt_deg_exact
        cnt_deg_reel = cnt_pas_reel * 360 / 6400
        cnt_deg_exact_calcul_erreur += 1*current_cnt_deg_exact
        erreur_cnt_deg = cnt_deg_exact_calcul_erreur - cnt_deg_reel

        while abs(erreur_cnt_deg) >= 0.05625 :
            if erreur_cnt_deg >= 0.05625:  # under 1 degree
                nb_pas = nb_pas + 1
                cnt_pas_reel = cnt_pas_reel + 1
                cnt_deg_reel = cnt_pas_reel * 360 / 6400
                # cnt_deg_exact_calcul_erreur += 1
                erreur_cnt_deg = cnt_deg_exact_calcul_erreur - cnt_deg_reel
            
            elif erreur_cnt_deg <= -0.05625:  # over 1 degree
                nb_pas = nb_pas - 1
                cnt_pas_reel = cnt_pas_reel - 1
                cnt_deg_reel = cnt_pas_reel * 360 / 6400
                # cnt_deg_exact_calcul_erreur += 1
                erreur_cnt_deg = cnt_deg_exact_calcul_erreur - cnt_deg_reel

        print(f"current_cnt_deg_exact: {cnt_deg_exact_calcul_erreur}, cnt_deg_reel: {cnt_deg_reel}, exact: {current_cnt_deg_exact}, erreur: {erreur_cnt_deg}, pas: {nb_pas}, cnt_pas: {cnt_pas_reel} ")
    elif current_cnt_deg_exact < 0 :
        cnt_pas_reel = cnt_pas_reel + nb_pas*current_cnt_deg_exact
        cnt_deg_reel = cnt_pas_reel * 360 / 6400
        cnt_deg_exact_calcul_erreur += 1*current_cnt_deg_exact
        erreur_cnt_deg = cnt_deg_exact_calcul_erreur - cnt_deg_reel

        while abs(erreur_cnt_deg) >= 0.05625 :
            if erreur_cnt_deg >= 0.05625:  # under 1 degree
                nb_pas = nb_pas + 1
                cnt_pas_reel = cnt_pas_reel + 1
                cnt_deg_reel = cnt_pas_reel * 360 / 6400
                erreur_cnt_deg = cnt_deg_exact_calcul_erreur - cnt_deg_reel
            
            elif erreur_cnt_deg <= -0.05625:  # over 1 degree
                nb_pas = nb_pas - 1
                cnt_pas_reel = cnt_pas_reel - 1
                cnt_deg_reel = cnt_pas_reel * 360 / 6400
                erreur_cnt_deg = cnt_deg_exact_calcul_erreur - cnt_deg_reel

        print(f"deg exact à bouger: {cnt_deg_exact_calcul_erreur}, deg réel à bouger: {cnt_deg_reel}, erreur: {erreur_cnt_deg}, cnt pas à envoyer: {cnt_pas_reel} ")

    sendVariableArduino(cnt_pas_reel, arduino)    #  Commenter pour run sans Arduino
    time.sleep(1)

    dernier_position_deg_exact = cnt_deg_exact
    return dernier_position_deg_exact