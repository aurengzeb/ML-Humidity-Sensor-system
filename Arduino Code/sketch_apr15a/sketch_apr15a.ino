float myBuffA[100];
float myBuffB[100];
float *pointerX;
float *pointerY;
float current = 0.0;
float before = 0.0;
float A = 0.0;
float B = 0.0;
float Aprime = 0.0;
float Bprime = 0.0;
float cosine_similiarity = 0.0;
int sensorValue = 0;  // variable to store the value read
int looping = 100;
int debug = 0;
void setup() {
  // put your setup code here, to run once:
       // debug value
  Serial.begin(9600);
  pointerX = myBuffA;
  pointerY = myBuffB;
}

void CosineSimiliaritySum(){

  for (int i = 0; i <= looping; i++) {
    before = pointerY[i]*pointerX[i];
    current +=before;

    Aprime = pointerX[i]*pointerX[i];
    Bprime = pointerY[i]*pointerY[i];
    A +=Aprime;
    B +=Bprime;
    if (debug == 1){
    Serial.print(pointerY[i]);
    Serial.print(",");
    Serial.print(pointerX[i]);
    Serial.print(",");
    Serial.print(before);
    Serial.print(",");
    Serial.print(current);
    Serial.print(",");
    Serial.print(A);
    Serial.print(",");
    Serial.print(B);
    Serial.println();
    delay(100);
    }
    
  }
  //return Aprime,Bprime,A,B;  
}


void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Doing for A1...");
  int analogPin = A0;
  for (int i = 0; i <= looping; i++) {
    sensorValue = analogRead(analogPin);  // read the input pin
    float val = sensorValue * (5.0 / 1023.0);
    //Serial.println(val);
    pointerX[i] = val;
    //delay(100);
  }  
   
  Serial.println("Doing for A2...");
  int analogPin2 = A5;
  for (int i = 0; i <= looping; i++) {
    sensorValue = analogRead(analogPin2);  // read the input pin
    float val= sensorValue * (5.0 / 1023.0);
    pointerY[i] = val;
  //Serial.println(val); 
  } 

  
  CosineSimiliaritySum();
  float Asq = sqrt(A);
  float Bsq = sqrt(B);
  if (debug == 1){
  Serial.print(current);
  Serial.print(",");
  Serial.print(Asq);
  Serial.print(",");
  Serial.print(Bsq);
  Serial.print(",");
  }
  cosine_similiarity = current/(Asq*Bsq);
  Serial.println(cosine_similiarity);
  delay(1000);


  

  

  

}
