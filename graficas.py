# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 20:51:07 2022

@author: Admin
"""
import matplotlib.pylab as plt
import pandas as pd

#filename='Datos_definitivo18_NCAP_sinluz.csv'

def graf(filename):
    
    graf="graficas/"
    folder="Datos/"
    
    dts=[]
    times=[]
    
    #Leemos todos el archivo filename para representar los datos
    dft=pd.read_csv(folder+filename)
    arrt=dft.to_numpy()
    n=int(arrt[-1,0]) #numero de medidas por memoria
    
    for data in arrt[:-1,0]:
        dts.append(data)
    for data in arrt[:-1,1]:
        times.append(data)
    
    a=[] #Matriz auxiliar
    b=[] #Datos de cada memoria ordenados fila a fila
    t1=[] #Matriz auxiliar
    t_final=[] #Tiempos de cada memoria ordenados fila a fila
    
    for j in range(0,32):
        for i in range(0,n):
            a.append(dts[i*32+j]*3.3/1024)
            t1.append(times[i*32+j])
        b.append(a[j*n:j*n+n])
        t_final.append(t1[j*n:j*n+n])
    
    colours=['r','b','g','k']
    
    fig, axs = plt.subplots(2, 4,figsize=(20,10))
    
    #############################  SELN  ###############################
    
    labels=['4','2','1','0.5']
    for i in range(0,4):
        axs[0, 0].plot(t_final[i],b[i],color=colours[i], label='Ln= '+labels[i])
    axs[0, 0].legend(loc="upper right")
    axs[0, 0].set_title('NMOS')
    
    labels=['4','2','1','6']
    for i in range(0,4):
        axs[0, 1].plot(t_final[i+4],b[i+4],color=colours[i], label='Wn= '+labels[i])
    axs[0, 1].legend(loc="upper right")
    axs[0, 1].set_title('NMOS_WIDTH')
    
    labels=['2','1','0.5','4']
    for i in range(0,4):
        axs[0, 2].plot(t_final[i+8],b[i+8],color=colours[i], label='Lp= '+labels[i])
    axs[0, 2].legend(loc="upper right")
    axs[0, 2].set_title('PMOS')
    
    labels=['0.5','1','2','4']
    for i in range(0,4):
        axs[0, 3].plot(t_final[i+12],b[i+12],color=colours[i], label='Wn= '+labels[i])
    axs[0, 3].legend(loc="upper right")
    axs[0, 3].set_title('TG')
    
    #############################  SEL  ###############################
    
    labels=['66.32','100.8','206','35.6']
    for i in range(0,4):
        axs[1, 0].plot(t_final[i+16],b[i+16],color=colours[i], label='mim= '+labels[i])
    axs[1, 0].legend(loc="upper right")
    axs[1, 0].set_title('TG_VAR_MIM')
    
    labels=['66.32','100.8','206','35.6']
    for i in range(0,4):
        axs[1, 1].plot(t_final[i+20],b[i+20],color=colours[i], label='mim= '+labels[i])
    axs[1, 1].legend(loc="upper right")
    axs[1, 1].set_title('NMOS_VAR_MIM')
    
    labels=['0.5','1','2','4']
    for i in range(0,4):
        axs[1, 2].plot(t_final[i+24],b[i+24],color=colours[i], label='Wn= '+labels[i])
    axs[1, 2].legend(loc="upper right")
    axs[1, 2].set_title('TG_L_1u')
    
    labels=['4','2','1','6']
    for i in range(0,4):
        axs[1, 3].plot(t_final[i+28],b[i+28],color=colours[i], label='Wp= '+labels[i])
    axs[1, 3].legend(loc="upper right")
    axs[1, 3].set_title('PMOS_WIDTH')
    
    
    
    for ax in axs.flat:
        ax.set(xlabel='Tiempo (ms)', ylabel='Voltaje (V)')
    
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    
    plt.savefig(folder+graf+filename[:-4]+".png")
    plt.savefig(folder+graf+filename[:-4]+".eps",format='eps')

    return "Gráfica guardada"