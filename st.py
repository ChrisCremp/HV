import numpy as np

def st(timeseries,minfreq,maxfreq,fmm):
#function [st,t,f] = st(timeseries,minfreq,maxfreq,samplingrate,freqsamplingrate)
# Returns the Stockwell Transform of the timeseries.
# Code by Robert Glenn Stockwell.
# DO NOT DISTRIBUTE#OOPS
# BETA TEST ONLY
# Reference is "Localization of the Complex Spectrum: The S Transform"
# from IEEE Transactions on Signal Processing, vol. 44., number 4, April 1996, pages 998-1001.
#
#-------Inputs Needed------------------------------------------------
# 
#   *****All frequencies in (cycles/(time unit))!******
#	"timeseries" - vector of data to be transformed
#-------Optional Inputs ------------------------------------------------
#
#"minfreq" is the minimum frequency in the ST result(Default=0)
#"maxfreq" is the maximum frequency in the ST result (Default=Nyquist)
#"samplingrate" is the time interval between samples (Default=1)
#"freqsamplingrate" is the frequency-sampling interval you desire in the ST result (Default=1)
#Passing a negative number will give the default ex.  [s,t,f] = st(data,-1,-1,2,2)
#-------Outputs Returned------------------------------------------------
#
# st     -a complex matrix containing the Stockwell transform. 
#			 The rows of STOutput are the frequencies and the
#         columns are the time values ie each column is
#         the "local spectrum" for that point in time
#  t      - a vector containing the sampled times
#  f      - a vector containing the sampled frequencies
#--------Additional details-----------------------
#   #  There are several parameters immediately below that
#  the user may change. They are:
#[verbose]    if true prints out informational messages throughout the function.
#[removeedge] if true, removes a least squares fit parabola
#                and puts a 5# hanning taper on the edges of the time series.
#                This is usually a good idea.
#[analytic_signal]  if the timeseries is real-valued
#                      this takes the analytic signal and STs it.
#                      This is almost always a good idea.
#[factor]     the width factor of the localizing gaussian
#                ie, a sinusoid of period 10 seconds has a 
#                gaussian window of width factor*10 seconds.
#                I usually use factor=1, but sometimes factor = 3
#                to get better frequency resolution.
#   Copyright (c) by Bob Stockwell
#   $Revision: 1.2 $  $Date: 1997/07/08  $


# This is the S transform wrapper that holds default values for the function.
    TRUE = 1
    FALSE = 0
### DEFAULT PARAMETERS  [change these for your particular application]
    verbose = FALSE   
    removeedge= TRUE
    analytic_signal =  TRUE
    factor = 1
###  of DEFAULT PARAMETERS
    if verbose:
        print(' ') # i like a line left blank 
    
    timeseries=timeseries.conjugate().transpose()	   
    samplingrate=1
    freqsamplingrate=1
    	 
    if verbose:  
        print('Minfreq = #d',minfreq) 
        print(('Maxfreq = #d',maxfreq)) 
        print(('Sampling Rate (time   domain) = #d',samplingrate)) 
        print(('Sampling Rate (freq.  domain) = #d',freqsamplingrate)) 
        print(('The size of the timeseries is #d points',np.size(timeseries))) 
        print(' ') 
	 
	# OF INPUT VARIABLE CHECK 	 
	# If you want to "hardwire" minfreq & maxfreq & samplingrate & freqsamplingrate do it here  
	# calculate the sampled time and frequency values from the two sampling rates 
    t = np.arange(0,np.size(timeseries))*samplingrate 
    spe_nelements =np.ceil((maxfreq - minfreq+1)/freqsamplingrate) 
    f = (minfreq + np.arange(spe_nelements)*freqsamplingrate)/(samplingrate*np.size(timeseries)) 
    if verbose: 
        print(('The number of frequency voices is #d',spe_nelements)) 
 
	# The actual S Transform function is here: 
    st = strans(timeseries,minfreq,maxfreq,samplingrate,freqsamplingrate,verbose,removeedge,analytic_signal,factor) 
	 
    return st,t,f
 
 
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
def g_window(size,freq,factor):
    
    # Function to compute the Gaussion window for 
    # function Stransform. g_window is used by function
    # Stransform. Programmed by Eric Tittley. Ported and adapted to Python by Christian Crempien
    #
    #-----Inputs Needed--------------------------
    #
    #	size-the size of the Gaussian window
    #
    #	freq-the frequency at which to evaluate
    #		  the window.
    #	factor- the window-width factor
    #
    #-----Outputs Returned--------------------------
    #
    #	gauss-The Gaussian window
    #
    gauss=np.zeros(size)	
    vector = np.zeros((2,size))
    vector[0,]=np.arange(0,size).T
    vector[1,]=np.arange(-size,0).T
    vector = vector.T  
    vector = np.power(vector,2.)     
#    for i in range(0,size):
#        vector[i,0] = np.power(vector[i,0],2)
#        vector[i,1] = np.power(vector[i,1],2)
    vector=vector*(-factor*2*np.power(np.pi,2)/(np.power(freq,2)))
    # Compute the Gaussion window
    gauss = np.exp(vector[:,0])+np.exp(vector[:,1])
#    for i in range(size):
#    gauss[i] = np.exp(vector[i,0])+np.exp(vector[i,1])
    gauss = gauss.T      
    return gauss

def strans(timeseries,minfreq,maxfreq,samplingrate,freqsamplingrate,verbose,removeedge,analytic_signal,factor):
    # Returns the Stockwell Transform, STOutput, of the time-series 
    # Code by R.G. Stockwell. Ported to Python by Christian Crempien
    # Reference is "Localization of the Complex Spectrum: The S Transform"
    # from IEEE Transactions on Signal Processing, vol. 44., number 4,
    # April 1996, pages 998-1001. 
    # 
    #-------Inputs Returned------------------------------------------------ 
    #      http://www.geopsy.org/documentation/geopsy/images/waveform-tapertypes.png   - are all taken care of in the wrapper function above 
    # 
    #-------Outputs Returned------------------------------------------------ 
    # 
    #	ST    -a complex matrix containing the Stockwell transform. 
    #			 The rows of STOutput are the frequencies and the 
    #			 columns are the time values 
    # 
    # 
    #---------------------------------------------------------------------- 
    # Compute the size of the data. 
    n=np.size(timeseries)
    #original = timeseries 
    if removeedge:
        if verbose: 
            print('Removing tr with polynomial fit')
	     
        ind = np.arange(n).conjugate().transpose() 
        r = np.polyfit(ind,timeseries,2) 
        fit = np.polyval(r,ind)  
        timeseries = timeseries - fit 
        if verbose: 
            print('Removing edges with 5# hanning taper')     
        sh_len = np.floor(np.size(timeseries)/10) 
        wn = np.hanning(sh_len)
        if(sh_len==0):
            sh_len=np.size(timeseries)
            wn = np.logical_and(1,np.arange(1,sh_len))
	    
            # make sure wn is a column vector, because timeseries is
        wn = wn.T	   
        k = np.floor(sh_len/2)+1      
        timeseries[np.arange(1,k,dtype=int)] = timeseries[np.arange(1,k,dtype=int)]*wn[np.arange(1,k,dtype=int)]
        timeseries[np.arange(n-k,n,dtype=int)] = timeseries[np.arange(n-k,n,dtype=int)]*wn[np.arange(sh_len-k,sh_len,dtype=int)] 
    # If vector is real, do the analytic signal  
	 
    if analytic_signal: 
        if verbose: 
            print('Calculating analytic signal (using Hilbert transform)')

        ts_spe = np.fft.fft(np.real(timeseries))		
        h = np.concatenate((2*np.ones(1+np.fix((n-1)/2)),np.ones(1-np.remainder(n,2)),np.zeros(np.fix((n-1)/2))))
        ts_spe *= h     
        ts_spe[:] = ts_spe*h[:]
        timeseries = np.fft.ifft(ts_spe)   
        vector_fft=np.fft.fft(timeseries)
        vector_fft=np.concatenate((vector_fft,vector_fft)).T
	
    st=np.zeros(((np.ceil((maxfreq - minfreq+1)/freqsamplingrate)),n),dtype=object)
	# Compute S-transform value for 1 ... ceil(n/2+1)-1 frequency points
    if verbose: 
        print('Calculating S transform...')
	
    if minfreq == 0:
        st[0,] = timeseries.mean()*np.logical_and(1,(np.arange(1,n+1,1)))
    else:
        st[0,:]=np.fft.ifft(vector_fft[minfreq:minfreq+n]*g_window(n,minfreq,factor))	
	#the actual calculation of the ST 
	# Start loop to increment the frequency point 
    fruit = np.arange(freqsamplingrate,(maxfreq-minfreq)+1,freqsamplingrate)
    for banana in fruit:
        b = np.fft.ifft(vector_fft[minfreq+banana:minfreq+banana+n]*g_window(n,minfreq+banana,factor)).T   
        for apple in range(n):
            st[banana,apple]=b[apple]
	   # a fruit loop!   aaaaa ha ha ha ha ha ha ha ha ha ha
	#  loop to increment the frequency point  
	#print st              
    return st
	
	###  strans function