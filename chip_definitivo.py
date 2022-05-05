# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 17:28:28 2022

@author: Admin
"""
import serial
import time
from graficas import graf
from analisis2 import an

folder="Datos/"

port="COM19" #nombre del puerto al que se conecta el arduino
baud=115200 #ratio del arduino

ser=serial.Serial(port,baud) #conexion con el arduino


#Preguntas para guardar los datos de forma ordenada
chip=input("¿Que chip estamos midiendo? ")
condiciones=input("¿Bajo iluminación? (Y/N) ")
estructura=input("¿NCAP, MIM, PCAP? (Out en 1,2,11) ")

#Construir el nombre del archivo donde guardar los datos

num = input("Período de medida T: ") #Período de lectura de memorias
ser.write(bytes(num, 'utf-8'))    

if condiciones=="Y" or condiciones=="Si" or condiciones=="si":
    luz=input("Alguna característica de la luz: ")
    filename="Datos_"+chip+"_"+estructura+"_T"+num+"_lux"+luz+".csv" #Archivo guardar datos
    ajstr=1

    if estructura=="1":
        estructura="NCAP"
        boundes=[[0.1,0,0,-100],[1.2,200,2,0]]
    elif estructura=="2":
        estructura="MIM"
        boundes=[[0.001,300,0.1],[1.2,4000,1.6]]
    elif estructura=="11":
        estructura="PCAP"
        boundes=[[0.001,300,0.1],[1.2,4000,1.6]]
        
else:
    filename="Datos_"+chip+"_"+estructura+"_T"+num+"_sinluz.csv"  #Archivo guardar datos
    ajstr=0
    
    if estructura=="1":
        estructura="NCAP"
        boundes=[[0.2,100,0.2],[0.9,400,0.9]]
    elif estructura=="2":
        estructura="MIM"
        boundes=[[0.001,300,0.1],[1.2,4000,1.6]]
    elif estructura=="11":
        estructura="PCAP"
        boundes=[[0.001,300,0.1],[1.2,4000,1.6]]
    

file=open(folder+filename,"w")

t_measures=0
measures=0
fallito=0
fallos=[]
filas=[]
dts=[]
times=[]


file = open(folder+filename, "a") #añadimos informacion al archivo
file.write("Lectura analógica,Tiempo\n")

#siguiente mensaje será el comienzo de datos de la primera medida
start=str(ser.readline().decode())
while "Inicio" not in start:
    start=str(ser.readline().decode())
print(start[0:-2])

time_start=time.time()

tiempos=0
n_filas=10000 #Límite en el caso de que el tiempo del Arduino sea demasiado largo
#Ahora almacenamos los valores que el arduino envía durante un ciclo completo    
while t_measures<n_filas:

    getData=ser.readline()
    #print(getData)
    fila=getData.decode()[0:][0:-2]
    #print(fila)  
    

    if str(getData).find('Final')==-1:
        #Cada fila representa el valor de una MEMORIA 
        
        filas.append(fila)
        if t_measures%33==0:
            #print(fila)
            
            try:
                times.append(float(filas[t_measures]))    #en esta matriz almacenamos los valores de tiempo
            except:
                times.append(2*float(filas[t_measures-33])-float(filas[t_measures-65])) #en el caso de que haya un error tomamos aprox del tiempo
                fallito=fallito+1
                fallos.append(t_measures)
                
            tiempos=tiempos+1
            t_measures=t_measures+1
            
        else:
            try:
                dts.append(float(filas[t_measures]))    #en esta matriz almacenamos los valores de todas las memorias (cada memoria esta separada por 32 valores)
            except:
                dts.append(float(filas[t_measures-33]))    #en el caso de que haya un error tomamos el último valor que hayamos medido de esa memoria
                fallito=fallito+1
                fallos.append(t_measures)
            #print(str(dts[t_measures-tiempos])+","+str(times[int(t_measures/33)])+"\n")
            file.write(str(dts[t_measures-tiempos])+","+str(times[int(t_measures/33)])+"\n") #escribimos cada linea
            t_measures=t_measures+1
            
    else: 
        t_measures=n_filas
    

n=len(dts)/32
print("Medidas para cada set de memorias: "+str(n))
print("Total de medidas: "+str(len(dts)))
print("Hubo "+str(fallito)+" fallito(s) en la(s) posicion(es): "+ str(fallos))
print("El archivo de datos es: " + filename)

file.write(str(n)+","+str(n) + "\n") #escribimos numero de medidas por memoria

file.close() #cerramos el archivo
ser.close() #cerramos el puerto

grafi=input("Ver las graficas: (Y/N) ")
if grafi=='Y' or grafi=='Yes' or grafi=='si' or grafi=='y' or grafi=='Si' or grafi=='yes':
    graf(filename)

    ajust=input("Ver los ajustes: (Y/N) ")
    if ajust=='Y' or ajust=='Yes' or ajust=='si' or ajust=='y' or ajust=='Si' or ajust=='yes':
        b=input("Cambiar límites de los ajustes: (Y/N) ")
        if b=='Y' or b=='Yes' or b=='si' or b=='y' or b=='Si' or b=='yes':
            bound=input('Límites: ')
            an(filename,bound,ajstr)
        else:
            bound=boundes
            an(filename,bound,ajstr)


