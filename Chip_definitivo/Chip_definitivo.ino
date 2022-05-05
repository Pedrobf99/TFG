//Nombramos cada pin con lo que representan
int row_0=4;
int row_1=5;
int col_0=6;
int col_1=7;
int sel_pin=3;
int wrt=8;
int index=0;

// período de medidas /matriz con los valores analógicos /tiempos auxiliares

float T;
float values[32]={};
unsigned long to;
unsigned long tr;

#include "functions.h"

void setup() { 
  
Serial.begin(115200); 
pinMode(sel_pin, OUTPUT); //sel o seln
pinMode(row_0, OUTPUT);   //primer bite de la row
pinMode(row_1, OUTPUT);   //segundo bite de la row
pinMode(col_0, OUTPUT);   //primer bite de la col
pinMode(col_1, OUTPUT);   //segundo bite de la col
pinMode(wrt, OUTPUT);     //write pin
pinMode(A0, INPUT);

/*
writerh(); // Función para escribir en todas las memorias

while (!Serial.available());
T = Serial.readString().toFloat();
tr = millis(); //Inicio de las medidas para tener una referencia

writerl(); // Función para escribir en todas las memorias*/
}

void loop() {
//writerh(); // Función para escribir en todas las memorias

while (!Serial.available());
writerh(); // Función para escribir en todas las memorias
T = Serial.readString().toFloat();
tr = millis(); //Inicio de las medidas para tener una referencia

writerl(); // Función para escribir en todas las memorias
Serial.println("SuperInicio"); //Escribimos para saber cuando empieza el loop
while(millis()-tr<T){

//Asignamos un valor de tiempo para cada set de memorias (aprox mismo para todos)
Serial.println(millis()-tr); //Este tiempo es válido ya que solo necesitamos una referencia, no el momento exacto
//Con esta funcion leemos en orden el valor de cada memoria
reader();

}

Serial.println("Final");

}
