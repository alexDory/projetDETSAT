double slope = 0.0291; // slope in Volts per dB @28GHz
double xint = -37.1; //log intercept in dBm @28GHz
double solution = 0.0049; // LSB Size, refer to dn1050
double voltage = 0;
double power = 0;
int inputPin = A0;
int i = 0;
byte * b = 0 ;
int buffer_size = 16;
float buffer[16];

void setup() {
Serial.begin(9600);
pinMode(7,OUTPUT);
digitalWrite(7,HIGH);
}

void loop() {
voltage = analogRead(inputPin) * solution;
power = (voltage / slope) + xint;

if (abs(power) <= 40) {
  buffer[i] = power;
  i = i + 1;
}
// send it to the computer as ASCII digits
if (i == buffer_size) {
  i = 0;
  b = (byte *) &buffer;
  Serial.write(b, 4*buffer_size);
}
delay(6); // delay in between reads for stability
}
