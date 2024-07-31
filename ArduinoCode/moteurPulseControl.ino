#define LED 13    //allume LED sur Arduino pour vérifier réception du nombre 2 du code python.
#define pulse 6
#define direction 4
//int nb_pas = 0;
// ajouter variable du nbr de pas à tourner 
// variable s'Appele nbr_steps

void setup() { 
	Serial.begin(115200); 
  pinMode(LED, OUTPUT);
  pinMode(pulse, OUTPUT);
  pinMode(direction, OUTPUT);
} 
void loop() { 
                
  int nb_pas = Serial.readString().toInt();
  if(nb_pas >= 0) {
    genererPulseHoraire(nb_pas);
  }
  else if(nb_pas <0) {
    genetatePulseAntiHoraire(nb_pas);
  }
}
 void genererPulseHoraire(int nbr_pulse) {
    digitalWrite(direction, HIGH);
    digitalWrite(LED, HIGH);
    for(int i = 0; i < abs(nbr_pulse) ; i++)
    {
      digitalWrite(pulse, HIGH);
      digitalWrite(pulse, LOW);
    }
 }
  void genetatePulseAntiHoraire(int nbr_pulse){
    digitalWrite(LED, HIGH);
    digitalWrite(direction, LOW);
    for(int i = 0; i < abs(nbr_pulse) ; i++)
    {
      digitalWrite(pulse, HIGH);
      digitalWrite(pulse, LOW);
 
    }
  }
