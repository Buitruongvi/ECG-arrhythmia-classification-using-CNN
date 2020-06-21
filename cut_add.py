"""
Created on Tue Mar 31 10:15:18 2020

@author: vibuitruong
"""
def clear_all():
    from IPython import get_ipython
    get_ipython().magic('reset -sf')
clear_all()
import wfdb
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def wavelet_denoise(S,lev,wavename): #trong dau () la inputdata, lev: level
    import pywt as pw #thu vien wavelet
    Cf=pw.wavedec(S,wavename,level=lev) #ptich tin hieu roi rac cho tin hieu vao
    m=len(S)
    An=pw.upcoef('a',Cf[0],wavename,level=lev,take=m)
    return An
#record1 = wfdb.Record(recordname='100.dat', fs=360, nsig=1, siglen=1000, filename=['100.dat'])
#data = np.genfromtxt('/Users/vibuitruong/Desktop/LV_2020/MIT_BIH_DATABASE/mit-bih-arrhythmia-database-1.0.0/100.dat',delimiter=',') 
NN = list() #Normal beat
LL = list() #Left bundle branch block beat
RR = list() #Right bundle branch block beat
AA = list() #Atrial premature beat
a = list() #Aberrated atrial premature beat
J = list() #Nodal (junctional) premature beat
S = list() #Supraventricular premature beat
VV = list() #Premature ventricular contraction
F = list() #Fusion of ventricular and normal beat
s = list() #Start of ventricular flutter/fibrillation
v = list() #Ventricular flutter wave
K = list() #End of ventricular flutter/fibrillation
e = list() #Atrial escape beat
n = list() #Nodal (junctional) escape beat
E = list() #Ventricular escape beat
PP = list() #Paced beat
f = list() #Fusion of paced and normal beat
x = list() #Non-conducted P-wave (blocked APB)
QQ = list() #Unclassifiable beat
I = list() #Isolated QRS-like artifact

N_record=list(); N_nb=list()
NOR = list()  
LBB = list()
RBB	= list()
APC = list()
PVC = list()
PAB = list()
QQQ = list()
CC = []
DD = []


name=list(['100','104','108','113','117','122','201','207','212','217','222','231','101','105','109','118','123',
               '202','208','213','219','223','232','102','106','111','115','119','124','209','214','220','228','233',
               '103','107','112','116','121','200','205','210','221','230','234'])


   
for i in range(len(name)):
    annn = wfdb.rdann(name[i], 'atr')
    ecgrecord = wfdb.rdsamp(name[i], channels = [0])
    ann=annn.sample
    anntype=annn.symbol
    ann = np.array(ann)[:]
    anntype = list(anntype)[1:-1]
    data=ecgrecord[0]
    data=np.array(data).reshape(650000,)
    wavename='sym8'
    level=2
    data=wavelet_denoise(data,level,wavename) - wavelet_denoise(data,12,wavename) 
    
    ecg_signal=[]
    ecg=[]
    signals = []
    r_peak=[]
    count = 1
    for j in (ann[1:-1]):
        x1 = (ann[count - 1] + j)//2
        x1=int(math.floor(x1))
        x2 = (ann[count + 1] + j)//2
        x2=int(math.ceil(x2))
        x0=j-x1-1
        r_peak.append(x0)
        signal = data[x1:x2]
        ecg_signal.append(signal)
        count += 1

    for j in range(len(ecg_signal)):
        sig=np.lib.pad(ecg_signal[j], (1500-r_peak[j],1500 - (len(ecg_signal[j]) - r_peak[j])), 'constant', constant_values=(0,0))
        ecg.append(sig)

    for j in range(len(ecg)):
        signals.append(ecg[j][1250:1750])
        
    for j in range(len(anntype)):
        if anntype[j] == 'N':
            NN.append(signals[j])
        elif anntype[j] == 'L':
            LL.append(signals[j])
        elif anntype[j] == 'R':
            RR.append(signals[j])
        elif anntype[j] == 'A':
            AA.append(signals[j])
        elif anntype[j] == 'a':
            QQ.append(signals[j])        
        elif anntype[j] == 'J':
            QQ.append(signals[j])
        elif anntype[j] == 'S':
            QQ.append(signals[j])        
        elif anntype[j] == 'V':
            VV.append(signals[j])        
        elif anntype[j] == 'F':
            QQ.append(signals[j])        
        elif anntype[j] == '[':
            QQ.append(signals[j])        
        elif anntype[j] == '!':
            QQ.append(signals[j])        
        elif anntype[j] == ']':
            QQ.append(signals[j])       
        elif anntype[j] == 'e':
            QQ.append(signals[j])        
        elif anntype[j] == 'j':
            QQ.append(signals[j])        
        elif anntype[j] == 'E':
            QQ.append(signals[j])        
        elif anntype[j] == '/':
            PP.append(signals[j])        
        elif anntype[j] == 'f':
            QQ.append(signals[j])        
        elif anntype[j] == 'x':
            QQ.append(signals[j])        
        elif anntype[j] == 'Q':
            QQ.append(signals[j])        
        elif anntype[j] == '|':
            QQ.append(signals[j])     
        elif anntype[j] == '~':
            QQ.append(signals[j])
        elif anntype[j] == '+':
            QQ.append(signals[j])
N=list()
L=list()
R=list()
P=list()
V=list()
A=list()
Q=list()

k=500

for i in range(len(NN)):
    if len(NN[i]) <= k:
        N.append(NN[i])
    else:
        N=N

for i in range(len(AA)):
    if len(AA[i]) <= k:
        A.append(AA[i])
    else:
        A=A
        
for i in range(len(LL)):
    if len(LL[i]) <= k:
        L.append(LL[i])
    else:
        L=L

for i in range(len(RR)):
    if len(RR[i]) <= k:
        R.append(RR[i])
    else:
        R=R
        
for i in range(len(PP)):
    if len(PP[i]) <= k:
        P.append(PP[i])
    else:
        P=P

for i in range(len(VV)):
    if len(VV[i]) <= k:
        V.append(VV[i])
    else:
        V=V

for i in range(len(QQ)):
    if len(QQ[i]) <= k:
        Q.append(QQ[i])
    else:
        Q=Q
 
dnn=np.asarray(N)
dnor = pd.DataFrame(data=dnn[0:,0:]) 
export_csv = dnor.to_csv (r'/Users/vibuitruong/Desktop/LV_2020/MIT_BIH_DATABASE/giua_500n/NOR.csv', index = None, header=None)

dnn=np.asarray(L)
dnor = pd.DataFrame(data=dnn[0:,0:]) 
export_csv = dnor.to_csv (r'/Users/vibuitruong/Desktop/LV_2020/MIT_BIH_DATABASE/giua_500n/LBB.csv', index = None, header=None)

dnn=np.asarray(R)
dnor = pd.DataFrame(data=dnn[0:,0:]) 
export_csv = dnor.to_csv (r'/Users/vibuitruong/Desktop/LV_2020/MIT_BIH_DATABASE/giua_500n/RBB.csv', index = None, header=None)

dnn=np.asarray(A)
dnor = pd.DataFrame(data=dnn[0:,0:]) 
export_csv = dnor.to_csv (r'/Users/vibuitruong/Desktop/LV_2020/MIT_BIH_DATABASE/giua_500n/APC.csv', index = None, header=None)

dnn=np.asarray(V)
dnor = pd.DataFrame(data=dnn[0:,0:]) 
export_csv = dnor.to_csv (r'/Users/vibuitruong/Desktop/LV_2020/MIT_BIH_DATABASE/giua_500n/PVC.csv', index = None, header=None)

dnn=np.asarray(P)
dnor = pd.DataFrame(data=dnn[0:,0:]) 
export_csv = dnor.to_csv (r'/Users/vibuitruong/Desktop/LV_2020/MIT_BIH_DATABASE/giua_500n/PAB.csv', index = None, header=None)

dnn=np.asarray(Q)
dnor = pd.DataFrame(data=dnn[0:,0:]) 
export_csv = dnor.to_csv (r'/Users/vibuitruong/Desktop/LV_2020/MIT_BIH_DATABASE/giua_500n/QQQ.csv', index = None, header=None)
