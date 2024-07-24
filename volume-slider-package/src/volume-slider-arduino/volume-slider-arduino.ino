const byte slider1_pin = A0;
const byte slider2_pin = A1;
const byte slider3_pin = A2;
const byte slider4_pin = A3;

long slider1_value = 0.0;
long slider2_value = 0.0;
long slider3_value = 0.0;
long slider4_value = 0.0;

char buf[16];


void setup() {
  Serial.begin(115200);
  pinMode(slider1_pin, INPUT);
  pinMode(slider2_pin, INPUT);
  pinMode(slider3_pin, INPUT);
  pinMode(slider4_pin, INPUT);

}

void loop() {
  slider1_value = analogRead(slider1_pin);

  slider2_value = analogRead(slider2_pin);

  slider3_value = analogRead(slider3_pin);

  slider4_value = analogRead(slider4_pin);

  ltoa(slider1_value, buf, 10);
  Serial.print(buf);
  Serial.print("|");

  ltoa(slider2_value, buf, 10);
  Serial.print(buf);
  Serial.print("|");

  ltoa(slider3_value, buf, 10);
  Serial.print(buf);
  Serial.print("|");

  ltoa(slider4_value, buf, 10);
  Serial.println(buf);


  delay(10);                         
}                                          
