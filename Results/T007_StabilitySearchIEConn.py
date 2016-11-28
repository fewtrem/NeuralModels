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
noiseNeuron = {'type':"constantrate",
          'name':"Very active input neuron with a target rate of up to 20Hz",
          'spikeSep':0.1,#10Hz, seems reasonable.
          'recordAct':True,
          'thresh':15.0,
          'exScale':1}
sourceNeuron = {'type':"constantrate",
          'name':"Very active input neuron with a target rate of up to 3Hz",
          'spikeSep':0.83,#10Hz, seems reasonable.
          'recordAct':True,
          'thresh':15.0,
          'exScale':1}
INeuron = {'type':"poisson",
          'name':"Less active input neuron to spike the with a more or less constant rate",
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
                             'average':0.05,
                             'theta':0.005},
            'postScale':1.0,
            'learn':True,
            'active':True,
            'learnKernel':{'type':'STDP',
                           'beta':20},
            'learnScale':0.0001}
noiseInput = {'responseKernel':{'type':'gamma',
                             'average':0.01,
                             'theta':0.004},
            'postScale':1.0,
            'active':True,
            'learn':False}
sourceConnNo3 = {'responseKernel':{'type':'gamma',
                             'average':0.01,
                             'theta':0.004},
            'postScale':1.0,
            'learn':False}
sourceConnNo4 = {'responseKernel':{'type':'gamma',
                             'average':0.05,
                             'theta':0.02},
            'postScale':1.0,
            'learn':False}
'''
Network
'''
# This way we can add lots of the same neurons!
neuronsList = {1:noiseNeuron,
               2:sourceNeuron,
               3:INeuron,
               4:IENeuron}
# [From,To,Type]
connectionsList = [[3,4,learningConn],
                   [1,4,noiseInput],
                   [2,3,sourceConnNo3],
                   [2,4,sourceConnNo4]]
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
runLength = 10
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
# +ve: From before To, -ve: To before From
def getWhatBeforeWhat(FromN,ToN):
    spkF = model1.params['neurons'][FromN]['spikeOuts'] 
    spkT = model1.params['neurons'][ToN]['spikeOuts']
    ts = np.zeros(len(spkF))
    for fi in range(len(spkF)):
        ts[fi] = spkF[fi]-spkT[np.argmin(np.abs(np.subtract(spkT,spkF[fi])))]
    return np.mean(ts)
            

print getWhatBeforeWhat(3,4)
print "1's avg. rate: ",getAvrgRate(1,(0,runLength))
print "2's avg. rate: ",getAvrgRate(2,(0,runLength))
print "3's avg. rate: ",getAvrgRate(3,(0,runLength))
print "4's avg. rate: ",getAvrgRate(4,(0,runLength))
pltNeuron(plt,4,60)
pltNeuron(plt,3,40)
plt.legend()
plt.show()
pltConnWeight(plt,3,4)
#pltConnWeight(plt,2,3)
plt.show()
