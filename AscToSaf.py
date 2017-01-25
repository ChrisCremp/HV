import glob
import numpy as np
import os

def asctosaf(way):
    
    tipo ='*.ASC'
    files = glob.glob(way+tipo)# Arreglo de strings de los archivos
    if files==[]:
        tipo='*.txt'
    files = glob.glob(way+tipo)# Arreglo de strings de los archivos
    n = np.size(files)
    for f in range(n):
        a=str(files[f])
        a=a.replace('\\','/').replace('\\\\','/')
        if files[f]!=files[f].replace('\\','/').replace('\\\\','/'):
            os.rename(files[f],a)
        files[f]=a
        a=a.split('-',1)
        if np.size(a)==2:
            if files[f]!=files[f].split('-',1)[1]:
#                os.rename(files[f],way+a[1])
                d=[]
            files[f]=a


    files = glob.glob(way+tipo)# Arreglo de strings de los archivos

    l = [None]*(n/3)
    l1=[None]*n
    h=5# Desde que linea empieza a leer los archivos
    f=0# Iniciar Indice
    frec1 =np.zeros(n)
    frec=np.zeros(n/3)
    while (f!=n):
        line1 = tuple(open(files[f],'r'))
        l1[f]=str(line1[3]).replace('# Estacion: ','').replace(' Componente: HNZ','').replace('Componente: HNE','').replace('Componente: HNN','').replace(' \n','').replace('Componente: HLZ','').replace(' Componente: HLE','')#Obiente el nombre de la estacion
        frec1[f]=float(str(line1[1]).replace('# Tasa de muestreo: ','').replace(' muestras/seg','').replace('\n',''))# Obtiene la frecuencia de muestreo para guardarla y entregarla al main
        mE = np.genfromtxt(files[f],skip_header=h)# Arreglo de Aceleraciones en Direccion Este
        mN = np.genfromtxt(files[f+1],skip_header=h)# Arreglo de Aceleraciones en Direccion Norte
        mV = np.genfromtxt(files[f+2],skip_header=h)# Arreglo de Aceleraciones en Direccion Vertical
        

        z=zip(mV,mN,mE)# Arreglo con las componentes en orden
        np.savetxt(way+str(line1[3]).replace('#','').replace('Componente: HNE','').replace('Componente: HNZ','').replace('Componente: HNN','').replace(':','_').replace('Componente: HLZ','').replace(' Componente: HLE','').replace(' ','').replace('\n','')+'.saf',z,delimiter=" ")#Guarda el archivo saf
        f+=3# Actualizar Indice
    for i in range(n/3):
        frec[i]=frec1[i*3]
        l[i]=l1[i*3]     
    return(n/3,frec,l)