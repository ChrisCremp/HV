import numpy as np
from dohvr import dohvr
from plothv import plothv
from tictoc import tic,toc

#####Parametros Programa
skip = 1# Lineas saltadas del archivo
camino = r'C:\Users\ccrem\Desktop\New folder (2)\Valparaiso\Valparaiso2010.saf'# Ruta del archivo saf
fmm = 200. #frecuencia de muestreo en Hz
TT = 10.0 #tiempo ventanas en segundos

booli = True#Verdadero muestra imagenes, falso no hace nada
#####

lines = tuple(open(camino,'r'))
M = np.genfromtxt(camino,skip_header=skip)#Matriz con las componentes de registro aceleraciones(V,N,E)
# a M se le puede usar filtros como Butterworth o Konno Omachi
tic()
hv,f,t,Ct=dohvr(M,fmm,TT)
med = plothv(hv,f,t,TT,'_'+str(TT),camino,booli) # Grafica y retorna la mediana de HVR
Amp = np.amax(med) # Amp Amplitud de fo
n = np.argmax(med)
ext = np.zeros(np.size(med))

ext[0]=f[n]#Guardando Frecuencia Fundamental
ext[1]=Amp#Guardando Amplitud
ext[2]=TT#Guardando tiempo de ventanas
ext[3]=1/f[n]#Guardando Periodo Fundamental
ext[4]=Ct#Guardando Cantidad de Ventanas

z=zip(f,med,ext)#Guarda el Dominio de Frecuencias, la amplitud media y los datos anteriores
np.savetxt(camino+'_'+str(TT)+'.csv',z,delimiter=",")#Guarda archivo csv con la media del espectro HV

if booli:
    print '-----------------------------------------------------'
    print 'Frecuencia:          ',f[n],' [hz]'
    print 'Amplitud:            ',"%.2f"%Amp
    print 'Numero de Ventanas:  ',Ct
    print 'Periodo de Nakamura: ',format(1/f[n],'.2f'),'[s]'
    print '-----------------------------------------------------'
    toc()
    print '-----------------------------------------------------'