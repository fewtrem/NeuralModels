'''
Created on 30 June 2016

@author: s1144899

The aim is to get the weight to increase and so the rate will also increase in demo up to the point that the rate in demo is such that it now pairs with the NEXT spike in the input neuron and as a result will be diminished!

'''
import Model,datetime, numpy as np
# Set up some poisson Neurons:
'''
Neurons
'''
inputNeuronCR = {'type':"constantrate",
          'name':"Very active input neuron with a target rate of up to 20Hz",
          'spikeSep':0.1,#10Hz, seems reasonable.
          'recordAct':True,
          'thresh':15.0,
          'exScale':1}
demoNeuron = {'type':"poisson",
          'name':"Second neuron, with the weight into it in question",
          'inateProb':0,
          'recordAct':True,
          'thresh':15.0,
          'exScale':1}
'''
Connections
'''
learningConn = {'responseKernel':{'type':'PSD',
                             'average':0.042,
                             'theta':5},
            'postScale':2.0,
            'learn':True,
            'active':True,
            'learnKernel':{'type':'STDP',
                           'beta':20},
            'learnScale':0.0001}
'''
Network
'''
# This way we can add lots of the same neurons!
neuronsList = {1:inputNeuronCR,
               2:demoNeuron}
# [From,To,Type]
connectionsList = [[1,2,learningConn]]
# Save
params={'neurons':neuronsList,
        'connections':connectionsList,
        'dt':0.001,
        'normFactorDX':0.001,
        'responseLimitCDF':0.99,
        'pickleOutFilePath':"/home/s1144899/Downloads/testPythonNeurons.pkl",
        'jsonOutFilePath':"/home/s1144899/Downloads/testPythonNeurons.jso"
        }
'''
Model Run
'''
print "Setting up..."
model1 = Model.Model(params)
print "Running model..."
runLength = 100
model1.run(runLength)
a = datetime.datetime.now()
model1.run(1)
b = datetime.datetime.now()
print b-a

'''
Analysis
'''
import matplotlib.pyplot as plt
def pltNeuron(plt,nodd,vval):
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
def pltConnWeight(plt,fromN,toN):
    t = []
    s = []
    for connT in model1.params['connections']:
        if connT[0] == fromN and connT[1] == toN:
            for val in connT[2]['weightStore']:
                t.append(val[0])
                s.append(val[1])
    plt.plot(t, s)
def getAvrgRate(N,rangeX):
    spk = model1.params['neurons'][N]['spikeOuts']
    spk = np.asarray(spk)
    spk= spk[spk>=rangeX[0]]
    if len(spk)>0:
        spk = spk[spk<rangeX[1]]
    return len(spk)/(1.0*rangeX[1]-rangeX[0])
# +ve: From before To, -ve: To before From
def getWhatBeforeWhat(FromN,ToN):
    spkF = model1.params['neurons'][FromN]['spikeOuts'] 
    spkT = model1.params['neurons'][ToN]['spikeOuts']
    ts = np.zeros(len(spkF))
    for fi in range(len(spkF)):
        ts[fi] = spkF[fi]-spkT[np.argmin(np.abs(np.subtract(spkT,spkF[fi])))]
    return np.mean(ts)
            

print getWhatBeforeWhat(1,2)
print "1's avg. rate: ",getAvrgRate(1,(0,runLength))
print "2's avg. rate: ",getAvrgRate(2,(0,runLength))
#print "3's avg. rate: ",getAvrgRate(3,(0,runLength))
#print "4's avg. rate: ",getAvrgRate(4,(0,runLength))
pltNeuron(plt,2,60)
pltNeuron(plt,1,40)
plt.legend()
plt.show()
pltConnWeight(plt,1,2)
#pltConnWeight(plt,2,3)
plt.show()
