# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 00:04:34 2022

@author: Admin
"""
import matplotlib.pylab as plt
import os
import pandas as pd
import regresion as r

#filename="Datos_casita_python6_NCAP_sinluz.csv"

def an(filename,boundes,ajstr):
    dts=[]
    times=[]
    
    folder="Datos/"
    ajust="Ajustes/"
        
    # CARACTERISTICAS MEMORIAS
    caract=[[4,2,1,0.5],[4,2,1,6],[2,1,0.5,4],[0.5,1,2,4],
            [66.32,100.8,206,35.6],[66.32,100.8,206,35.6],[0.5,1,2,4],[4,2,1,6]]
    #Variable que cambia en cada caso
    var=['Ln','Wn','Lp','Wn','mim','mim','Wn','Wp']
    
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
    
    #matriz donde almacenaremos todos los datos ordenados
    valores=[]
    #Matrices auxiliares para recoger los datos
    Vin=[]
    sVin=[]
    a=[]
    sa=[]
    Vhold=[]
    sVhold=[]
    c=[]
    sc=[]
    for j in range(0,8):
        Vin=[]
        sVin=[]
        a=[]
        sa=[]
        Vhold=[]
        sVhold=[]
        c=[]
        sc=[]
        for i in range(0,4):
            if ajstr==0:
                #Ajustamos cada memoria a una exponencial decreciente
                coefs,scoef=r.ajuste(t_final[i+j*4][1:], b[i+j*4][1:], boundes,i+j*4,ajstr)
            if ajstr==1:
                #Ajustamos cada memoria a una exponencial decreciente + una recta
                coefs,scoef=r.ajuste(t_final[i+j*4][1:], b[i+j*4][1:], boundes,i+j*4,ajstr)
                c.append(coefs[3])
                sc.append(scoef[3])

            #Recogemos los valores obtenidos
            Vin.append(coefs[0])
            a.append(coefs[1])
            Vhold.append(coefs[2])
            
            sVin.append(scoef[0])
            sa.append(scoef[1])
            sVhold.append(scoef[2])
        if ajstr==0:
            valores.append([Vin,sVin,a,sa,Vhold,sVhold])
        if ajstr==1:
            valores.append([Vin,sVin,a,sa,Vhold,sVhold,c,sc])
    #comparamos las caract de las memorias con los valores obtenidos del ajuste
    regres=r.regs(caract,valores,ajstr)    
    #Esta función nos da las rectas del ajuste anterior para representarlas
    plots=r.plotss(caract,regres,var,ajstr)
    
    
    ### GRAFICAR ###
    
    ajstra=ajstr+3    
    fig, axs = plt.subplots(1, ajstra)
    if ajstr==0:
        labels=['$V_{in}$','RC','$V_{hold}$']
        ylabels=['$V (V)$','tiempo (ms)','$V (V)$']
    if ajstr==1:
        labels=['$V_{in}$','RC','$V_{hold}$', 'C']
        ylabels=['$V (V)$','tiempo (ms)','$V (V)$', 'V/s']    
    
    colores=['g','b','k','gray','r','gold','lime','violet']
    
    for j in range(0,ajstra):
        
        axs[j].set(ylabel=ylabels[j])
        axs[j].set_title(labels[j],loc='left')
        
        h=0
        k=[]
        for i in range(0,8):
            if var[i]!='mim':
                if h==0:
                    axs[j].set(xlabel='Ln, Lp, Wn, Wp')
                    h=1
                axs[j].errorbar(caract[i],valores[i][j*2],valores[i][j*2+1],0,
                                ls='',marker='o',c=colores[i], label=var[i], capsize=3,)
                if regres[j][4][i]>0:
                    axs[j].plot(plots[j*8+i][0],plots[j*8+i][1], ls='--',c=colores[i])
            else:
                k.append(i)
        if j==3:        
            axs[j].legend(bbox_to_anchor=(1.04,1), loc="upper left")
        
        axs[j]=axs[j].twiny()
        for i in k:
            axs[j].errorbar(caract[i],valores[i][j*2],valores[i][j*2+1],0,
                            ls='',marker='o',c=colores[i], label=var[i], capsize=3)
            if regres[j][4][i]>0:
                axs[j].plot(plots[j*8+i][0],plots[j*8+i][1], ls='--',c=colores[i])
            
        #axs[j].spines['bottom'].set_position(('outward',60))
        axs[j].set(xlabel='mim')
        if j==ajstr+2:        
            axs[j].legend(bbox_to_anchor=(1.04,0.5), loc="center left") 
    
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    fig.set_size_inches(15, 6)
    
    path=ajust+filename[:-4]+"/"
    if not os.path.exists(path):
        os.makedirs(path)
    fig.savefig(path+filename[:-4]+'_ajuste_'+str(ajstr)+'.png')
    
    #plt.close(fig)
    
    r.ajuste_graph(t_final, b, path+filename[:-4],boundes,ajstr)
