
void configu(int n){

pinMode(sel_pin, OUTPUT); //sel o seln
pinMode(row_0, OUTPUT);   //primer bite de la row
pinMode(row_1, OUTPUT);   //segundo bite de la row
pinMode(col_0, OUTPUT);   //primer bite de la col
pinMode(col_1, OUTPUT);   //segundo bite de la col
pinMode(wrt, OUTPUT);     //write pin
pinMode(A0, INPUT);
Serial.println("Medidas");
Serial.println(n);

}

void selector(int col, int row, int sel) {

//Encendemos el 1º Led o el 2º en función del 1º y 2º bite de col
digitalWrite(col_0,bitRead(col,0));
digitalWrite(col_1,bitRead(col,1));

//Igual con row
digitalWrite(row_0,bitRead(row,0));
digitalWrite(row_1,bitRead(row,1));

//Serial.print(sel);
digitalWrite(sel_pin, sel);

}

void writerh(){

//Recorremos todas las memorias FILA tras FILA
int k = 0; // Para escribir sel y seln funcionan simultánemaente

for (int j = 0; j <= 3; j++){ 
for (int i = 0; i <= 3; i++){ 

selector(i,j,k); //Elegimos que memoria escribimos
//Escribimos 
digitalWrite(wrt,HIGH);
}
}
  
}

void writerl(){

//Recorremos todas las memorias FILA tras FILA
int k = 0; // Para escribir sel y seln funcionan simultánemaente

for (int j = 0; j <= 3; j++){ 
for (int i = 0; i <= 3; i++){ 

selector(i,j,k); //Elegimos que memoria escribimos
//Escribimos 
digitalWrite(wrt,LOW);
}
}
  
}

void reader(){

//Recorremos todas las memorias FILA tras FILA
for (int k = 0; k <= 1; k++){
for (int j = 0; j <= 3; j++){ 
for (int i = 0; i <= 3; i++){
selector(i,j,k); //Elegimos que memoria escribimos

index=i+(j*4)+(k*16);
values[index]=analogRead(A0);   //valores de la memoria i j k convirtiendo a un valor decimal

}
}
}

//Escribimos los valores de la matriz de voltaje 
for (int k = 0; k <= 1; k++){
for (int j = 0; j <= 3; j++){ 
for (int i = 0; i <= 3; i++){
index=i+(j*4)+(k*16);
Serial.println((String)values[index]);

}
}
}


}
