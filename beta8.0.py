# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 15:28:07 2013

@author: Administrator
"""
#如果有高音低音同一时刻出现情形只考虑高音
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 23:31:27 2013

@author: Administrator
"""
#我得添加一个循环 然后有高音就不要低音
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 23:17:40 2013

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 15:14:23 2013

@author: FengSong
"""


import math
import wave
import numpy as np
from midiutil.MidiFile import MIDIFile

infile_loc_str = r"./kiss.wav"
output = r"./kiss.mid"

x=(math.log(50))/72
z=(math.exp(10))/72
testmusic =wave.open(infile_loc_str,"rb")
music_params = testmusic.getparams()
nchannels,sampwidth,framerate,nframes = music_params[:4]

MyMIDI = MIDIFile(1,True)
# Tracks are numbered from zero. Times are measured in beats.
track = 0
time = 0
instrument = 1
        # Add track name and tempo.
MyMIDI.addTrackName(track,time,"Sample Track")
MyMIDI.addTempo(track,time,120)
MyMIDI.addProgramChange(track,0,time,instrument)

str_data = testmusic.readframes(nframes)
testmusic.close()
wave_data = np.fromstring(str_data,dtype=np.short)
wave_data.shape = -1,2
wave_data = wave_data.T
wave_datam = wave_data[0] 
nengliang = [0]*60
lengthofmusic = len(wave_data[0])
totaltimes = lengthofmusic
time_range = 441
times = totaltimes//time_range

tmp_array = [0]* times
tmp_array2 = [0]* times
freq_energy = [[0 for column in range(72)] for row in range(times)]
energy = [[0 for column in range(times)] for row in range(72)]
freq_exist  = [[0 for column in range(72)] for row in range(times)]
ene         = [[0 for column in range(72)] for row in range(times)]

#	          F 0        sF 1         G 2        sG 3         A 4        sA 5        B 6          C 7        sC 8        D 9        sD 10         E 11                 
freq_limit = [2.30868e13, 2.30868e13, 2.30868e13, 2.30868e13, 2.30868e13, 2.19012e13/32768, 2.64973e13/32768, 4.92543e13/32768, 3.65653e13/32768, 3.5178e13/32768,  5.73849e13/32768, 4.16085e13/32768,
              2.72218e13/16384, 1.48236e13/16384, 1.11237e13/16384, 6.76899e12/16384, 3.41448e12/16384, 2.68832e12/16384, 2.94328e12/16384, 7.77911e12/16384, 6.66595e12/16384, 6.03084e12/16384, 5.42931e12/16384, 2.3451e12/16384,   
              5.30009e12/8192, 4.63972e12/8192, 3.20635e12/8192, 2.56969e12/8192, 1.70587e12/8192, 7.69582e11/8192, 7.77267e11/8192, 1.48177e12/8192, 3.38261e12/8192, 2.32701e12/8192, 2.49851e12/8192, 1.31225e12/8192,
              1.57175e12/4096, 1.0511e12/4096 , 1.25977e12/4096, 9.60296e11/4096, 7.71892e11/4096, 9.05611e11/4096, 5.92198e11/4096, 1.06676e12/4096, 1.23506e12/4096, 9.50611e11/4096, 8.76779e11/4096, 4.08903e11/4096,
              7.25764e11/2048, 5.066e11/2048,   4.49367e11/2048, 4.37983e11/2048, 1.55175e11/2048, 1.47827e11/2048, 2.2997e11/2048,  1.8163e11/2048,  1.40956e11/2048, 1.92557e11/2048, 4.70372e11/2048, 2.761e11/2048,
              3.21571e11/1024, 2.61613e11/1024, 2.57987e11/1024, 2.05225e11/1024, 5.08002e10/1024, 9.12449e10/1024, 7.92388e10/1024, 8.39058e10/1024, 8.16176e10/1024, 7.68599e10/1024, 5.12188e10/1024, 2.45622e10/1024 ] 
limit = 23986523.4375              



# 0  1   2   3  4   5  6  7   8  9  10  11
# F  sF  G  sG  A  sA  B  C  sC  D  sD  E

p=[0]*1000
track = 0
channel = 0	
s=[0]*72
t=[0]*72
duration = 0.01
volume = 100
def ssqr(tempf,x):
	ssq = (abs(tempf[x])**2)+(abs(tempf[x+1])**2)
	return ssq

for ti in range(times):
     
     for i in range(6):
		fft_size = pow(2,15-i)
		temp_arr = wave_datam[ti*time_range:ti*time_range+fft_size]
		tempf=np.fft.fft(temp_arr)
		
		freq_energy[ti][i*12] = ssqr(tempf,32)/fft_size
		freq_energy[ti][i*12+1] = ssqr(tempf,34)/fft_size
		freq_energy[ti][i*12+2] = ssqr(tempf,36)/fft_size
		freq_energy[ti][i*12+3] = ssqr(tempf,38)/fft_size
		freq_energy[ti][i*12+4] = (abs(tempf[41])**2)/fft_size
		freq_energy[ti][i*12+5] = (abs(tempf[43])**2)/fft_size
		freq_energy[ti][i*12+6] = (abs(tempf[46])**2)/fft_size
		freq_energy[ti][i*12+7] = ssqr(tempf,48)/fft_size
		freq_energy[ti][i*12+8] = ssqr(tempf,51)/fft_size
		freq_energy[ti][i*12+9] = ssqr(tempf,54)/fft_size
		freq_energy[ti][i*12+10] = ssqr(tempf,57)/fft_size
		freq_energy[ti][i*12+11] = (abs(tempf[61])**2)/fft_size
	
		#for k in range(12):
                  #ft = i*12+k
                  
                  #if (freq_energy[ft][ti]>freq_limit[ft]):
				#freq_exist[ft][ti] = 1
                  #if (k>0) and (freq_energy[ft][ti] < 1.5*freq_energy[ft-7][ti]) and (freq_exist[ft-7][ti] == 1):
				#freq_exist[ft][ti] = 0
                  #if (k>1) and (freq_energy[ft][ti] < 1.5*freq_energy[ft-24][ti]) and (freq_exist[ft-24][ti] == 1):
				#freq_exist[ft][ti] = 0
                
                  #elif (ft>18) and (freq_energy[ft][ti] < 1.55*freq_energy[ft-19][ti]) and (freq_exist[ft-19][ti] == 1):
				#freq_exist[ft][ti] = 0
                  #elif (k>0) and (freq_energy[ft][ti] < 1.55*freq_energy[ft-12][ti]) and (freq_exist[ft-12][ti] == 1):
				#freq_exist[ft][ti] = 0
                  
     #for i in range(72):
         #freq_energy[ti][i]=freq_energy[ti][i]*(1+20/72*(i+1))
 #12以下的低频我不找了   
     for i in range(60):
         nengliang[i]=freq_energy[ti][i+12]
    
     m = max(nengliang)
     y = nengliang.index(max(nengliang)) + 12
     if (m>=limit):
         freq_exist[ti][y]=1
     while (y>24):
         y=y-12
         if(freq_energy[ti][y]>=0.6*freq_energy[ti][y+12]):
             freq_exist[ti][y]=1
             freq_exist[ti][y+12]=0
             if(y<=47):
                 freq_exist[ti][y+24]=0
                
        
     
     for i in range(72):
         freq_energy[ti][i]=freq_energy[ti][i]*(math.exp(i*x))
     for i in range(72):
		#if(i<=35):	
                      #freq_exist[i][ti] = 0
		if (freq_exist[ti][i] == 1):
                  if(s[i]==0):
                      s[i]=s[i]+1 
                      str_tmp = str(freq_energy[ti][i])
                      t[i]=0
                      a=s[i]
                      w=ti
                      energy[i][a]=freq_energy[ti][i]
                  else:        
                      s[i]=s[i]+1 
                      str_tmp = str(freq_energy[ti][i])
                      t[i]=0
                      a=s[i]
                      energy[i][a]=freq_energy[ti][i]
                      
                    
                   
                 
                 
		else:
                                    
                  if(t[i]<=5):
                      t[i]=t[i]+1                      
                  else:    
                      if(s[i]>=1):
                          m = max(energy[i])//freq_limit[i]
                          if(m<=0):
                              m=1
                          m=math.log(m,10)
                          volume = int (30*m)
                          if(volume>127):
                              volume=127
                          MyMIDI.addNote(track,channel,i+29,w/50,0.02*10*(ti-w),volume) #(math.log(i*z))
                          
                          t[i]=0
                          for n in range(s[i]):
                          
                              energy[i][n] = 0 
                          s[i]=0    
                      else:
                          
                          t[i]=0
                          for n in range(s[i]):
                          
                              energy[i][n] = 0 
                          s[i]=0
     


binfile = open(output, 'wb')
MyMIDI.writeFile(binfile)
binfile.close()


    
    

    
    
