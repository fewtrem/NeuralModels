'''
Created on 30 June 2016

@author: s1144899

To test an E>I connection for stabilisation using a common input neuron and a large difference in input weights.

Trying to use our knowledge of the parameters for the uncorrelated learning to help us determine correlated learning!

'''
import Model,datetime, numpy as np
# Set up some poisson Neurons:
'''
Neurons
'''
sourceNeuron = {'type':"constantrate",
          'name':"Standard poisson Neuron Input Noise A",
          'spikeSep':0.2,#10Hz, seems reasonable.
          'recordAct':True,
          'thresh':15.0,
          'exScale':1}
inputNeuronA = {'type':"poisson",
          'name':"Standard poisson Neuron Input Noise A",
          'inateProb':0,
          'recordAct':True,
          'thresh':15.0,
          'exScale':-1}
IENeuron = {'type':"poisson",
          'name':"Standard poisson Neuron",
          'inateProb':0,
          'recordAct':True,
          'thresh':15.0,
          'exScale':1}
'''
Connections
'''
learningConn = {'responseKernel':{'type':'gamma',
                             'average':0.505,
                             'theta':0.05},
            'postScale':5.0,
            'learn':True,
            'active':False,
            'learnKernel':{'type':'STDP',
                           'beta':5},
            'learnScale':0.01}
inputConnNo1 = {'responseKernel':{'type':'gamma',
                             'average':0.01,
                             'theta':0.004},
            'postScale':1.0,
            'learn':False}
inputConnNo2 = {'responseKernel':{'type':'gamma',
                             'average':0.02,
                             'theta':0.005},
            'postScale':1.0,
            'learn':False}
'''
Network
'''
# This way we can add lots of the same neurons!
neuronsList = {1:inputNeuronA,
               2:IENeuron,
               3:sourceNeuron}
# [From,To,Type]
connectionsList = [[1,2,learningConn],
                   [3,1,inputConnNo1],
                   [3,2,inputConnNo2]]
# Save
params={'neurons':neuronsList,
        'connections':connectionsList,
        'dt':0.001,
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
model1.params['neurons'][3]['spikeSep'] = 1000.0
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
pltNeuron(plt,2,60)
pltNeuron(plt,1,40)
plt.legend()
plt.show()
pltConnWeight(plt,1,2)
#pltConnWeight(plt,2,3)
plt.show()
