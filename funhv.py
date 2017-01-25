#Editado y portado a Python por Christian Crempien
from st import st
import numpy as np

def funhv(Mv,Mn,Me,fi,ff,fmm):
    stV,t,f=st(Mv.transpose(),fi,ff,fmm)# S-transform de V
    stN,t,f=st(Mn.transpose(),fi,ff,fmm)# S-transform de N
    stE,t,f=st(Me.transpose(),fi,ff,fmm)# S-transform de E

    a = np.absolute(stN)
    b = np.absolute(stE)
    c = np.absolute(stV)
    a = np.power(a,2)
    b = np.power(b,2)
    hv = np.power((a+b)/2,0.5)
    hv = hv/c

    return hv.T