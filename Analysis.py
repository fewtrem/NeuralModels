'''
Created on 4 Aug 2016

@author: s1144899
'''
import numpy as np
def pltNeuron(model1,plt,nodd,vval):
    t = []
    s = []
    for val in model1.params['neurons'][nodd]['actVals']:
        t.append(val[0])
        s.append(val[1])
    ts = []
    ss = []
    for val in model1.params['neurons'][nodd]['spikeOuts']:
        ts.append(val-0.0001)
        ss.append(0.0)
        ts.append(val)
        ss.append(vval)
        ts.append(val+0.0001)
        ss.append(0.0)
    plt.plot(t, s,label="Activity "+str(nodd))
    plt.plot(ts, ss,label="Spikes "+str(nodd))
def pltConnWeight(model1,plt,fromN,toN):
    t = []
    s = []
    for connT in model1.params['connections']:
        if connT[0] == fromN and connT[1] == toN:
            for val in connT[2]['weightStore']:
                t.append(val[0])
                s.append(val[1])
    plt.plot(t, s)
def getAvrgRate(model1,N,rangeX):
    spk = model1.params['neurons'][N]['spikeOuts']
    spk = np.asarray(spk)
    spk= spk[spk>=rangeX[0]]
    if len(spk)>0:
        spk = spk[spk<rangeX[1]]
    return len(spk)/(1.0*rangeX[1]-rangeX[0])
# +ve: From before To, -ve: To before From
def getWhatBeforeWhat(model1,FromN,ToN):
    spkF = model1.params['neurons'][FromN]['spikeOuts'] 
    spkT = model1.params['neurons'][ToN]['spikeOuts']
    ts = np.zeros(len(spkF))
    for fi in range(len(spkF)):
        ts[fi] = spkF[fi]-spkT[np.argmin(np.abs(np.subtract(spkT,spkF[fi])))]
    return np.mean(ts)
def pltV(model1,plt,nodd,whatToPlot):
    t = []
    s = []
    for val in model1.params['neurons'][nodd][whatToPlot]:
        t.append(val[0])
        s.append(val[1])
    plt.plot(t, s,label="Activity "+str(nodd))
    return plt
def pltSpikes(model1,plt,nodd,vval):
    ts = []
    ss = []
    for val in model1.params['neurons'][nodd]['spikeOuts']:
        ts.append(val-0.0001)
        ss.append(0.0)
        ts.append(val)
        ss.append(vval)
        ts.append(val+0.0001)
        ss.append(0.0)
    plt.plot(ts, ss,label="Spikes "+str(nodd))