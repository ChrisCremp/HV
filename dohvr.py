import numpy as np
from funhv import funhv
import scipy.signal


def dohvr(M,fmm,TT):
    # M (V N E)
    # frecuencia de muestreo 'fm' HZ, ventana de 'TT' segundos
    # Autor Luis Podesta (2014)
    # Co-autores Felipe Leyton & Esteban Saez
    # Editado y portado a Python por Christian Crempien
    
    m = M.size/M.shape[1]
    fm=fmm # Frecuencia de muestreo [Hz]
    sint=2 # Salto del intervalo (1 toma todos los datos, 2 toma uno por medio)
    fmin = 0.1 #Fruencia minima [Hz]
    fmax = 10.0 #Frecuecia maxima [Hz]
    T = TT # Tiempo de la ventana [s]
    fi=np.ceil(fmin*T) #
    ff=np.ceil(fmax*T) #
    Ct=int(np.fix(m/(fm*T))) #Cantidad de ventanas
    
    f = np.arange(fmin,fmax+0.001,1./T)#####+1./T

    t = np.arange(2/fm,T+2/fm,2/fm)############
    T = int(T)
    fm = int(fmm)       

    for i in range(Ct):
        intt = np.arange(T*fm*(i)+1,T*fm*(i+1)+1,sint)
        Mv=scipy.signal.detrend(M[intt,0]) # se saca la tendencia lineal
        Mn=scipy.signal.detrend(M[intt,1]) # se saca la tendencia lineal
        Me=scipy.signal.detrend(M[intt,2]) # se saca la tendencia lineal
        hvw=funhv(Mv,Mn,Me,fi,ff,fmm)#Calcula hvr de cada ventana
        hvw = hvw.astype(float)
        if i==0:
            hv=hvw*0. 
        hv=hv+np.log(hvw) #Promedio geometrico

    hv=(hv.T)
    hv=np.exp(hv/Ct) #Promedio geometrico

    return (hv, f, t, Ct)