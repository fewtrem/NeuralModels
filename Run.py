'''
Created on 19 Jan 2016

@author: s1144899
'''
import Model
# Set up some poisson Neurons:

inputConnA = {'responseKernel':{'type':'gamma',
                             'average':0.1,
                             'theta':0.05},
            'postScale':1.0}

exConn14 = {'responseKernel':{'type':'gamma',
                             'average':0.6,
                             'theta':0.5},
            'postScale':1.0}
exConn35 = {'responseKernel':{'type':'gamma',
                             'average':0.2,
                             'theta':0.1},
            'postScale':0.95}
inConn45 = {'responseKernel':{'type':'gamma',
                             'average':0.2,
                             'theta':0.1},
            'postScale':-0.4}

inputNeuronA = {'type':"poisson",
          'name':"Standard Poisson Neuron Input Noise A",
          'inateProb':100.0,
          'recordAct':True}
inputNeuronB = {'type':"poisson",
          'name':"Standard Poisson Neuron Input Noise B",
          'inateProb':100.0,
          'recordAct':True}
excitatoryNeuronA = {'type':"poisson",
          'name':"Standard Poisson Neuron Excitatiory A",
          'inateProb':0.0,
          'recordAct':True}
inhibitoryNeuronA = {'type':"poisson",
          'name':"Standard Poisson Neuron Inhibitory A",
          'inateProb':0.0,
          'recordAct':True}

# This way we can add lots of the same neurons!
neuronsList = {1:inputNeuronA,
               2:inputNeuronB,
               3:excitatoryNeuronA,
               4:inhibitoryNeuronA,
               5:excitatoryNeuronA}
# [From,To]
connectionsList = [[1,3,inputConnA],
                   [1,2,exConn14],
                   [4,2,inConn45],
                   [3,5,exConn35]]

# Save
params={'neurons':neuronsList,
        'connections':connectionsList,
        'dt':0.001,
        'responseLimitCDF':0.99,
        'pickleOutFilePath':"/home/s1144899/Downloads/testPythonNeurons.pkl",
        'jsonOutFilePath':"/home/s1144899/Downloads/testPythonNeurons.jso"
        }

model1 = Model.Model(params)
model1.run(1)
model1.params['neurons'][1]['inateProb'] = 0.0
model1.run(3)
'''
#TEST OF PICKLE+JSON
model1.pickle()
model1.json()
model2 = Model.modelFromJSON("/home/s1144899/Downloads/testPythonNeurons.jso")
model2.run(0.002)
print model2.params
'''
'''
# TEST OF WHAT IS WHERE
for nn in model1.listOfNeurons:
    n = model1.listOfNeurons[nn]
    print n.params['name']
    for c in n.connectionsIn:
        print "IN"
        print c.inN.params['name'], " to ",c.outN.params['name']
    for c in n.connectionsOut:
        print "OUT"
        print c.inN.params['name'], " to ",c.outN.params['name']
'''

import matplotlib.pyplot as plt


def pltNeuron(plt,nodd,vval):
    t = []
    s = []
    for val in model1.params['neurons'][nodd]['actVals']:
        t.append(val[0])
        s.append(val[1])
    plt.plot(t, s)
    '''
    ts = []
    ss = []
    for val in model1.params['neurons'][nodd]['spikeOuts']:
        ts.append(val-0.0001)
        ss.append(0.0)
        ts.append(val)
        ss.append(vval)
        ts.append(val+0.0001)
        ss.append(0.0)
        plt.plot(ts, ss)
    '''

def pltSpikes(plt,nodd,vval):
    ts = []
    ss = []
    for val in model1.params['neurons'][nodd]['spikeOuts']:
        ts.append(val-0.0001)
        ss.append(0.0)
        ts.append(val)
        ss.append(vval)
        ts.append(val+0.0001)
        ss.append(0.0)
    plt.plot(ts, ss)

pltNeuron(plt,3,500)
pltNeuron(plt,4,-500)
pltNeuron(plt,5,-500)
pltSpikes(plt,5,-500)
plt.show()
'''
import numpy as np
t = np.arange(0.0, 0.1, 0.001)
tRK = model1.getConn(1,2).responseKernel
s = map(tRK.getVal,t)
plt.plot(t, s)
plt.show()
'''

