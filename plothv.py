import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def plothv(hv,f,t,TT,l,way,booli):
    
    #med=plothv(hv,f,t),rangos fijos de 0.1 Hz a 10 Hz con 0 a 10 de amplitud
    # se retorna la mediana y graficos 
    # Autor Luis Podesta (2014)
    # Co-autores Felipe Leyton & Esteban Saez
    # editado y portado a Python por Christian Crempien
    
    plt.close("all")
    n = hv.size/hv.shape[1]
    
    plt.figure().set_size_inches([10,16],forward=True)
    plt.subplot(4,1,1)
    im = plt.imshow(hv.T, interpolation="none",aspect='auto',cmap='Greys_r'); 
    plt.xscale('log')
    plt.xlim(0.1, 10)
    plt.ylim(0, TT)
    plt.pcolormesh(f,t,(hv.T),cmap=cm.gray)
    plt.colorbar(im,orientation='horizontal',fraction=0.07)
    plt.title('HVR',fontname="Times New Roman")
    plt.xticks([0.1,0.2,0.3,0.5,0.7,1,2,3,4,5,6,7,8,10],['0.1','0.2','0.3','0.5','0.7','1','2','3','4','5','6','7','8','10'],rotation='horizontal') 
    plt.ylabel('Tiempo Ventanas [s]',fontname="Times New Roman")
    plt.xlabel('Frecuencia [Hz]',fontname="Times New Roman")
	
    Q=np.zeros((n,9))
    pp=np.zeros((n,3))
    for j in range(0,n):
        vt=hv[j,:].T
        Q[j,0]=np.percentile(vt,10)
        Q[j,1]=np.percentile(vt,20)
        Q[j,2]=np.percentile(vt,40)
        Q[j,3]=np.percentile(vt,50) #med
        Q[j,4]=np.percentile(vt,60)
        Q[j,5]=np.percentile(vt,80)
        Q[j,6]=np.percentile(vt,90)
        Q[j,7]=np.percentile(vt,0) #min
        Q[j,8]=np.percentile(vt,100) #max
        pp[j,0]=np.mean(vt) #Promedio
        pp[j,1]=np.std(vt[vt>pp[j,0]])# DesStandar sobre el promedio
        pp[j,2]=np.std(vt[vt<pp[j,0]])# DesStandar bajo el promedio
        
    med=Q[:,3]
    nn = np.argmax(med) 
       
    plt.subplot(4,1,2)
    
    plt.title('MEDIANA Y PERCENTILES (min-10-20-40-60-80-90-max)',fontname="Times New Roman")
    plt.xscale('log')
    plt.xticks([0.1,0.2,0.3,0.5,0.7,1,2,3,4,5,6,7,8,10],['0.1','0.2','0.3','0.5','0.7','1','2','3','4','5','6','7','8','10'],rotation='horizontal') 
    plt.xlabel('Frecuencia [Hz]',fontname="Times New Roman")
    plt.ylabel('Amplitud HVR',fontname="Times New Roman")
    plt.xlim(0.1, 10)
    plt.ylim(0, 10)
    plt.fill_between(f,Q[:,7],Q[:,8],facecolor='0.8',label="min-max")
    plt.fill_between(f,Q[:,6],Q[:,0],facecolor='0.6',label="10-90") 
    plt.fill_between(f,Q[:,5],Q[:,1],facecolor='0.4',label="20-80")
    plt.fill_between(f,Q[:,4],Q[:,2],facecolor='0.2',label="40-60")
    plt.legend(bbox_to_anchor=(9, 1), loc=2, borderaxespad=0.)

    plt.subplot(4,1,3)
    
    plt.title('PROMEDIO Y DESVIACION ESTANDAR',fontname="Times New Roman")
    plt.xticks([0.1,0.2,0.3,0.5,0.7,1,2,3,4,5,6,7,8,10],['0.1','0.2','0.3','0.5','0.7','1','2','3','4','5','6','7','8','10'],rotation='horizontal') 
    plt.xlabel('Frecuencia [Hz]',fontname="Times New Roman")
    plt.ylabel('Amplitud HVR',fontname="Times New Roman")
    plt.xscale('log')
    plt.xticks([0.1,0.2,0.3,0.5,0.7,1,2,3,4,5,6,7,8,10],['0.1','0.2','0.3','0.5','0.7','1','2','3','4','5','6','7','8','10'],rotation='horizontal') 
    plt.ylim(0, 10)
    plt.fill_between(f,pp[:,0]+pp[:,1],pp[:,0]-pp[:,2]  ,facecolor='0.5',label="Devst")
    plt.plot(f,pp[:,0],color='black',label="Media")
    plt.tight_layout(pad=1, w_pad=5, h_pad=2)
    plt.legend(bbox_to_anchor=(9, 1), loc=2, borderaxespad=0.)
    plt.annotate('F0 = '+str("%.2f"%f[nn])+'Hz ; Amp = '+str("%.2f"%med[nn]),xy=(f[nn],med[nn]+1))
    
    plt.subplot(4,1,4)
    
    plt.title('VENTANAS',fontname="Times New Roman")
    plt.xticks([0.1,0.2,0.3,0.5,0.7,1,2,3,4,5,6,7,8,10],['0.1','0.2','0.3','0.5','0.7','1','2','3','4','5','6','7','8','10'],rotation='horizontal') 
    plt.xlabel('Frecuencia [Hz]',fontname="Times New Roman")
    plt.ylabel('Amplitud HVR',fontname="Times New Roman")
    plt.xscale('log')
    plt.xticks([0.1,0.2,0.3,0.5,0.7,1,2,3,4,5,6,7,8,10],['0.1','0.2','0.3','0.5','0.7','1','2','3','4','5','6','7','8','10'],rotation='horizontal') 
    plt.ylim(0, 10)
    for i in range(n):
        plt.plot(f,hv[:,i],linewidth=0.1)
    plt.gcf().subplots_adjust(bottom=0.03)
    plt.savefig(way+l+'.png',dpi=300)
    
    if booli:
        plt.show()
    plt.close('all')
    plt.clf()
    return med