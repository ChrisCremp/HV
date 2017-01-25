import numpy as np
from dohvr import dohvr
from plothv import plothv
from tictoc import tic,toc
import glob
from AscToSaf import asctosaf
import os


# Este codigo fue hecho para procesar eventos sismicos de estaciones sismograficas del CSN. Si se desean otras cosas, se pueden usar los modulos facilmente.
# BUGS: en Plothv en linea 52 aveces no son compatibles las dimensiones. Cambiar tipo de los objetos de float64 a float32 para ver si mejora el tiempo de procesamiento
tic()
path='C:\Users\ccrem\Google Drive\Memoria 1\Mio\\0_Registros-Base\Evento_Sismicos\\a\\'
subdirectories = os.listdir(path)

for alpha in range(np.size(subdirectories)):
    # Parametros cambiables:
    booli = False # Verdadero si se prefiere que los graficos salgan en consola
    camino = path+subdirectories[alpha]+'/'# Ruta de los archivos a portar
    
    
    nest,fr,ln = asctosaf(camino)# Numero de archivos saf , la lista de sus respectivas frecuencias de muestreo y el nombre de la estacion
    files = glob.glob(camino+'*.saf')#Archivos saf
    fmm = 200.0 #frecuencia en Hz
    
    #==========================================================================
    # ~ ARCHIVO SAF (V N E) %%
    #==========================================================================
    
    #==========================================================================
    # ~ Ubicacion del archivo SAF
    #==========================================================================
    #==========================================================================
    #Se deben colocar en orden las componentes de aceleracion:
    # Primero Vertical
    # Segundo Norte
    # Tercero Este
    #==============================================================================
    
    
    for i in range(np.size(files)):
        TT = 10.0 #ventanas en segundos
        fmm = fr[i]
        cam = files[i].replace('\\','\\\\') 
        lines = tuple(open(cam,'r'))
        M = np.genfromtxt(cam)
        Ct = 0
    
        
        hv,f,t,Ct=dohvr(M,fmm,TT) # retorna la matriz hv y sus ejes respectivos
        med = plothv(hv,f,t,TT,'_'+str(TT),cam,booli) # Grafica y retorna la mediana de HVR
        Amp = np.amax(med) # Amp Amplitud de fo
        n = np.argmax(med)
        ext=np.zeros(np.size(med))

        ext[0]=f[n]
        ext[1]=Amp
        ext[2]=TT
        ext[3]=1/f[n]
        ext[4]=Ct

        z=zip(f,med,ext)
        np.savetxt(cam+'_'+str(TT)+'.csv',z,delimiter=",")
        if booli:
            print '------------------------------------------------------'
            print 'Estacion:            ',ln[i]
            print 'Frecuencia:          ',f[n],' [hz]'
            print 'Amplitud:            ',"%.2f"%Amp
            print 'Numero de Ventanas:  ',Ct
            print 'Duracion de Ventanas:',TT,'[s]'
            print 'Periodo de Nakamura: ',format(1/f[n],'.2f'),'[s]'
            print '------------------------------------------------------'
            toc()
            print '------------------------------------------------------'

       
toc()
print '------------------------------------------------------'