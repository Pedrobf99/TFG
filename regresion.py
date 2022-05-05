#!/usr/bin/python
#-*- coding: utf-8 -*-

import numpy as np
import scipy.optimize as so
import matplotlib.pylab as plt

def regresionSimple(x,y):
    n=len(x)
    sx=sum(x); sy=sum(y); xx=np.dot(x,x); yy=np.dot(y,y); xy=np.dot(x,y); st=0
    denom=(n*xx-sx**2)
    b=(n*xy-sx*sy)/denom
    a=(xx*sy-sx*xy)/denom
    for i in range(0,len(x)):
        	st=st+(y[i]-a-b*x[i])**2
    s=np.sqrt(st/(n-2))
    sa=s*np.sqrt(xx/(n*xx-sx**2))
    sb=s*np.sqrt(n/(n*xx-sx**2))
    r=(n*xy-sx*sy)/np.sqrt((n*xx-sx**2)*(n*yy-sy**2))
    return [a,b,sa,sb,r,s]

def rsq(varf,varm):
    return (1-varf/varm)
# Tipo de ajuste al que sometemos nuestros datos
def simple(t,Vin,a,Vhold):
    return Vin*np.exp(-t/a)+Vhold
def luz1(t,Vin,a,Vhold,c):
    return Vin*np.exp(-t/a)+Vhold+c*t

#Realizamos el ajuste y nos permite graficar los valores y la función resultado
def ajuste(t_final,b,bounds,mem,ajust):
    
    if ajust==0:
        if bounds:
            coef,cov=so.curve_fit(simple,t_final,b,bounds=bounds)
        else:
            coef,cov=so.curve_fit(simple,t_final,b,bounds=[[0.1,0,0],[4,1.9,2]])
            
    if ajust==1:
        if bounds:
            coef,cov=so.curve_fit(luz1,t_final,b,bounds=bounds)
        else:
            coef,cov=so.curve_fit(luz1,t_final,b,bounds=[[0.1,0,0,-100],[1.2,200,2,0]])    
            
    perr = np.sqrt(np.diag(cov))
    
    '''
    cor=np.zeros([3,3])
    for j in range(0,3):
        for i in range(0,3):
            cor[i][j]=(cov[i][j]/np.sqrt(cov[i][i]*cov[j][j]))
    a=cor[0][1]**2+cor[0][2]**2+cor[1][2]**2
    print(a)
    if a<1:
        print("Memoria: "+str(mem))
    '''
    #print("La matriz de correlacion es: "+'\n'+str(cor))
    return coef,perr

def ajuste_graph(t_final,b,filename,boundes,ajust):
    hs=[]
    for j in range(0,8):
        for i in range(0,4):
            t_final1=t_final[i+j*4][1:]
            b1=b[i+j*4][1:]
            t1 = np.linspace(0, t_final1[-1]*1.1, 100)
            if ajust==0:
                if boundes:
                    coef,cov=so.curve_fit(simple,t_final1,b1,bounds=boundes)
                else:
                    coef,cov=so.curve_fit(simple,t_final1,b1,bounds=[[0.1,0,0],[4,1.9,2]])
                f=simple(t1,*coef)
            if ajust==1:
                if boundes:
                    coef,cov=so.curve_fit(luz1,t_final1,b1,bounds=boundes)
                else:
                    coef,cov=so.curve_fit(luz1,t_final1,b1,bounds=[[0.1,0,0,-100],[1.2,200,2,0]])   
                f=luz1(t1,*coef)
            
            
            
            hs.append([t1,f])
            
    colours=['r','b','g','k']
    
    fig, axs = plt.subplots(2, 4,figsize=(20,10))
    
    #############################  SELN  ###############################
    
    labels=['4','2','1','0.5']
    for i in range(0,4):
        axs[0, 0].plot(hs[i][0],hs[i][1],color=colours[i], label='Ajuste exp Ln: '+labels[i])
        axs[0, 0].plot(t_final[i],b[i],ls='',marker='o', markersize=1,color=colours[i])

    axs[0, 0].legend(loc="upper right")
    axs[0, 0].set_title('NMOS')
    
    labels=['4','2','1','6']
    for i in range(0,4):
        axs[0, 1].plot(hs[i+4][0],hs[i+4][1],color=colours[i], label='Ajuste exp Wn: '+labels[i])
        axs[0, 1].plot(t_final[i+4],b[i+4],ls='', markersize=1,marker='o',color=colours[i])
    axs[0, 1].legend(loc="upper right")
    axs[0, 1].set_title('NMOS_WIDTH')
    
    labels=['2','1','0.5','4']
    for i in range(0,4):
        axs[0, 2].plot(hs[i+8][0],hs[i+8][1],color=colours[i], label='Ajuste exp Lp: '+labels[i])
        axs[0, 2].plot(t_final[i+8],b[i+8],ls='', markersize=1,marker='o',color=colours[i])
    axs[0, 2].legend(loc="upper right")
    axs[0, 2].set_title('PMOS')
    
    labels=['0.5','1','2','4']
    for i in range(0,4):
        axs[0, 3].plot(hs[i+12][0],hs[i+12][1],color=colours[i], label='Ajuste exp Wn: '+labels[i] )
        axs[0, 3].plot(t_final[i+12],b[i+12], markersize=1,ls='',marker='o',color=colours[i])
    axs[0, 3].legend(loc="upper right")
    axs[0, 3].set_title('TG')
    
    #############################  SEL  ###############################
    
    labels=['66.32','100.8','206','35.6']
    for i in range(0,4):
        axs[1, 0].plot(hs[i+16][0],hs[i+16][1],color=colours[i], label='Ajuste exp mim: '+labels[i])
        axs[1, 0].plot(t_final[i+16],b[i+16], markersize=1,ls='',marker='o',color=colours[i])
    axs[1, 0].legend(loc="upper right")
    axs[1, 0].set_title('TG_VAR_MIN')
    
    labels=['66.32','100.8','206','35.6']
    for i in range(0,4):
        axs[1, 1].plot(hs[i+20][0],hs[i+20][1],color=colours[i], label='Ajuste exp mim: '+labels[i])
        axs[1, 1].plot(t_final[i+20],b[i+20],ls='', markersize=1,marker='o',color=colours[i])
    axs[1, 1].legend(loc="upper right")
    axs[1, 1].set_title('NMOS_VAR_MIN')
    
    labels=['0.5','1','2','4']
    for i in range(0,4):
        axs[1, 2].plot(hs[i+24][0],hs[i+24][1],color=colours[i], label='Ajuste exp Wn: '+labels[i])
        axs[1, 2].plot(t_final[i+24],b[i+24],ls='', markersize=1,marker='o',color=colours[i])
    axs[1, 2].legend(loc="upper right")
    axs[1, 2].set_title('TG_L_1u')
    
    labels=['4','2','1','6']
    for i in range(0,4):
        axs[1, 3].plot(hs[i+28][0],hs[i+28][1],color=colours[i], label='Ajuste exp Wp: '+labels[i])
        axs[1, 3].plot(t_final[i+28],b[i+28],ls='', markersize=1,marker='o',color=colours[i])
    axs[1, 3].legend(loc="upper right")
    axs[1, 3].set_title('PMOS_WIDTH')
    
    
    
    for ax in axs.flat:
        ax.set(xlabel='Tiempo (ms)', ylabel='Voltaje (V)')
    
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    
    fig.savefig(filename+'_ajustes_'+str(ajust)+'.png')

    return 'Nombre de la gráfica: '+filename+'_ajustes_'+str(ajust)+'.png'



def regs(caract,valores,ajstr):
    vari=[]
    ajstra=ajstr+3
    for j in range(0,ajstra):
        ass=[]
        bs=[]
        sas=[]
        sbs=[]
        rs=[]
        ss=[]
        for i in range(0,8):
            a,b,sa,sb,r,s=regresionSimple(caract[i], valores[i][j*2]) #regresion lineal de cada 4 valores
            
            ass.append(a)
            bs.append(b)
            sas.append(sa)
            sbs.append(sb)
            rs.append(r**2)
            ss.append(s)
            
        vari.append([ass,bs,sas,sbs,rs,ss]) 
        #recogemos todos los valores de las 
        #regresiones de cada variable vin,rc,vhold
    if ajstr==0:
        return vari[0],vari[1],vari[2]
    if ajstr==1:
        return vari[0],vari[1],vari[2],vari[3]
    
def f(x,a,b):
    return x*b+a

def plotss(cars,regres,var,ajstr):
    hs=[]
    ajstra=ajstr+3
    for j in range(0,ajstra):
        for i in range(0,8):
            if var[i]=='mim':
                x = np.linspace(0, 200, 30)
            else:
                x = np.linspace(0, 6, 30)
            a=regres[j][0][i]
            b=regres[j][1][i]
            h=f(x,a,b)
            
            hs.append([x,h])
    
    return hs
