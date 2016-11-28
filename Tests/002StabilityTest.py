'''
Created on 30 June 2016

@author: s1144899

To test an E>I connection for stabilisation using a common input neuron and a large difference in input weights.

'''
import Model,datetime, numpy as np
# Set up some poisson Neurons:
'''
Neurons
'''
inputNeuronA = {'type':"poisson",
          'name':"Standard poisson Neuron Input Noise A",
          'inateProb':10.0,
          'recordAct':True,
          'thresh':15.0,
          'exScale':1}
INeuron = {'type':"poisson",
          'name':"Standard poisson Neuron",
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
inputConn12 = {'responseKernel':{'type':'gamma',
                             'average':0.055,
                             'theta':0.05},
            'postScale':0.3,
            'learn':False,
            'learnKernel':{'type':'STDP',
                           'beta':5},
            'learnScale':0.005}
inputConn13 = {'responseKernel':{'type':'gamma',
                             'average':0.505,
                             'theta':0.05},
            'postScale':3.0,
            'learn':False,
            'learnKernel':{'type':'STDP',
                           'beta':5},
            'learnScale':0.005}
inhibConn23 = {'responseKernel':{'type':'gamma',
                             'average':0.505,
                             'theta':0.5},
            'postScale':2.0,
            'learn':False,
            'learnKernel':{'type':'STDP',
                           'beta':5},
            'learnScale':0.005}
'''
Network
'''
# This way we can add lots of the same neurons!
neuronsList = {1:inputNeuronA,
               2:INeuron,
               3:IENeuron}
# [From,To,Type]
connectionsList = [[1,2,inputConn12],
                   [1,3,inputConn13]]#,
                    #[2,3,inhibConn23]]
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
model1.run(10)
model1.params['neurons'][1]['inateProb'] = 0.0
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
    plt.plot(t, s,label="Neuron "+str(nodd))
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
def getAvrgRate(N):
    spk = model1.params['neurons'][N]['spikeOuts']
    diffs = np.subtract(spk[1:],spk[:-1])
    diffs = np.divide(1,diffs)
    return [np.mean(diffs),np.std(diffs)]
def getWhatBeforeWhat(FromN,ToN):
    spkF = model1.params['neurons'][FromN]['spikeOuts'] 
    spkT = model1.params['neurons'][ToN]['spikeOuts']
    ts = np.zeros(len(spkF))
    for fi in range(len(spkF)):
        ts[fi] = spkF[fi]-spkT[np.argmin(np.abs(np.subtract(spkT,spkF[fi])))]
    return np.mean(ts)
            

print getWhatBeforeWhat(2,3)
print "2's avg. rate: ",getAvrgRate(2)
print "3's avg. rate: ",getAvrgRate(3)
pltNeuron(plt,2,40)
pltNeuron(plt,3,60)
plt.legend()
plt.show()

'''
pltConnWeight(plt,1,2)
#pltConnWeight(plt,2,3)
plt.show()
'''