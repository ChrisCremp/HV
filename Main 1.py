import numpy as np
from dohvr import dohvr
from plothv import plothv
import time
#from Konno_Ohmachi import smooth_spectra
from untitled1 import butter_lowpass,butter_highpass
import scipy as sp

def tic():
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    if 'startTime_for_tictoc' in globals():
        print "Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds."
    else:
        print "Toc: start time not set"

#BUGS: en Plothv en linea 52 aveces no son compatibles las dimensiones. En funhv se cambia el tipo de los arreglos y no se pueden realizar operaciones "element wise" lo que hace que el codigo sea mucho mas lento 
tic()

order = 4 # Orden del ButterWorth
cutoff1 = 50 # Frecuencia de corte en Hz
cutoff2 = 0.5#Frecuencia corte en Hz
count = 1
######################PARAMETOS CAMBIABLES:
booli = True # Verdadero si se prefiere que los graficos salgan en consola
verb = False # Verdadero si queremos que haga mas de un archivo iterando sobre el tiempo de ventana. Falso si queremos solo un archivo   
l = 'Pudahuel'   #Nombre de los archivos
skip = 15# Lineas saltadas del archivo
camino = r'C:\Users\ccrem\Desktop\Nakamuras\Aeropuerto FACH, Pudahuel R21M\15350 20 min_001part1\EqualizedFile.saf'# Ruta del archivo saf
fmm = 128.0 #frecuencia en Hz
TT = 60.0 #ventanas en segundos
band = 100 # Pasabanda del filtro Konno Ohmachi

# ~ ARCHIVO SAF (V N E) %%
lines = tuple(open(camino,'r'))
M = np.genfromtxt(camino,skip_header=skip)





###############################################################################
#Filtro butter high

##
#b, a = butter_lowpass(cutoff1, fmm, order)
#M[:,0] = sp.signal.filtfilt(b,a,M[:,0])
#M[:,1] = sp.signal.filtfilt(b,a,M[:,1])
#M[:,2] = sp.signal.filtfilt(b,a,M[:,2])
##
#b, a = butter_highpass(cutoff2, fmm, order)
###
#M[:,0] = sp.signal.filtfilt(b,a,M[:,0])
#M[:,1] = sp.signal.filtfilt(b,a,M[:,1])
#M[:,2] = sp.signal.filtfilt(b,a,M[:,2])
################################################################################

if verb==True:
    Ct = 0  
    while (Ct!=20 and Ct!=19 and Ct!=18 and Ct!=17 and Ct!=16 and Ct!=15 and Ct!=14):#Ver forma de hacer esto mas elegante
        hv,f,t,Ct=dohvr(M,fmm,TT) # retorna la matriz hv y sus ejes respectivos

#        hv = smooth_spectra(hv.T,f,band,count).T
        
        med = plothv(hv,f,t,TT,'_'+str(TT),camino,booli) # Grafica y retorna la mediana de HVR
        Amp = np.amax(med) # Amp Amplitud de fo
        n = np.argmax(med)
        ext = np.zeros(np.size(med))

        ext[0]=f[n]
        ext[1]=Amp
        ext[2]=TT
        ext[3]=1/f[n]
        ext[4]=Ct

        z=zip(f,med,ext)
        np.savetxt(camino+'_'+str(TT)+'.csv',z,delimiter=",")

        if booli:
            print '-----------------------------------------------------'
            print 'Frecuencia:          ',f[n],' [hz]'
            print 'Amplitud:            ',"%.2f"%Amp
            print 'Numero de Ventanas:  ',Ct
            print 'Periodo de Nakamura: ',format(1/f[n],'.2f'),'[s]'
            print '-----------------------------------------------------'
            toc()
            print '-----------------------------------------------------'
        TT+=2        

else:
    hv,f,t,Ct=dohvr(M,fmm,TT) # retorna la matriz hv y sus ejes respectivos
    toc()
#    hv = smooth_spectra(hv.T,f,band,count = 1).T
    
    med = plothv(hv,f,t,TT,l+'_'+str(TT),camino,booli) # Grafica y retorna la mediana de HVR
    Amp = np.amax(med) # Amp Amplitud de fo
    n = np.argmax(med)
    ext=np.zeros(np.size(med))

    ext[0]=f[n]
    ext[1]=Amp
    ext[2]=TT
    ext[3]=1/f[n]
    ext[4]=Ct

    z=zip(f,med,ext)
    np.savetxt(camino+'_'+str(TT)+'.csv',z,delimiter=",")
    if booli:
        print '-----------------------------------------------------'
        print 'Frecuencia:          ',f[n],' [hz]'
        print 'Amplitud:            ',"%.2f"%Amp
        print 'Numero de Ventanas:  ',Ct
        print 'Periodo de Nakamura: ',format(1/f[n],'.2f'),'[s]'
        print '-----------------------------------------------------'
    
toc()
print '-----------------------------------------------------'