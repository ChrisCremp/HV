
import plothv
import dohvr



#==============================================================================
# ~ ARCHIVO SAF (V N E) %%
#==============================================================================
M=load('C:\Users\ccrem\Desktop\Matlab Nak\SI\C10O SI.saf',' ',19,0)
#==============================================================================
# ~ Ubicación del archivo SAF
#==============================================================================
#==============================================================================
# % Se debe colocar la el valor de la primera fila con datos, en el ejemplo
# % 19
#
#==============================================================================

TT = 10 #ventanas en segundos
fmm = 200 #frecuencia en Hz
[hv,f,t,Ct]=dohvr(M,fmm,TT) # retorna la matriz hv y sus ejes respectivos
med=plothv(hv,f,t) # Grafica y retorna la mediana de HVR
[Amp,n]=max(med) # Amp Amplitud de fo
print('Frecuencia %2.2f [Hz], Amplitud HVR %2.2f \n, Cantidad de Ventanas',f(n),Amp,Ct)