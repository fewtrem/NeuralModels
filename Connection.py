'''
Created on 19 Jan 2016

@author: s1144899
'''
import ResponseKernel, numpy as np

# A place to store connection info more than anything else!

class Connection:
    # REF to Model class
    networkC = None
    # REF to Neuron class
    inN = None
    # REF to Neuron class
    outN = None
    # REF to responseKernel class
    responseKernel = None
    # REF to Connection Dictionary
    params = None
    # Params:
    '''
        'name' - String
        'responseKernel' - responseKernel Dictionary
        'learn' - Boolean - True for learning
        'learnRate' - Double
        'weightStore' - store of weights
    '''
    def __init__(self,networkC,params,inN,outN):
        # note that the params are just from the changing array that we can pickle out!
        self.params = params
        self.networkC = networkC
        self.inN = inN
        self.outN = outN
        try:
            self.params['name'] = params['name']
        except:
            self.params['name'] = str("Untitled Connection")
        try:
            self.params['active'] = params['active']
        except:
            self.params['active'] = True
        try:
            self.params['learn'] = params['learn']
        except:
            self.params['learn'] = False
        if self.params['learn'] == True:
            self.weightResponseKernel = ResponseKernel.setResponseKernel(networkC,params['learnKernel'])
            self.params['weightStore'] = []
        # Set response kernel:
        self.responseKernel = ResponseKernel.setResponseKernel(networkC,params['responseKernel'])
        inN.addOutput(self)
        outN.addInput(self)
        self.checkConns()
    def getIn(self):
        return self.inN
    def getOut(self):
        return self.outN
    def checkConns(self):
        foundOne = False
        for Conn in self.networkC.listOfConnections:
            if self.inN is Conn.inN and self.outN is Conn.outN and self is not Conn:
                print "Warning: Multiple connections between same neurons in same direction"
                print "--- Neuron From:",self.inN.params['name']," (id:",self.inN.params['id'],")"
                print "--- Neuron To:",self.outN.params['name']," (id:",self.outN.params['id'],")"
                foundOne = True
        return foundOne
    def getCurEx(self,curT):
        #TODO:
        # list iterator:
        i = 0
        # get the excitability from the incoming neuron by getting it's spikelist
        thisInputL = self.inN.getParams()['spikeOuts']
        curVal = 0
        while i < len(thisInputL):
            spikeT = thisInputL[i]
            diffInVal = curT-spikeT
            # check is positive for influence: *** NOT EQUAL TO as may be just made! ***
            if diffInVal>0:
                if diffInVal < self.responseKernel.responseLimit:
                    curVal += self.inN.params['exScale']*self.params['postScale']*self.responseKernel.getVal(diffInVal)
            i+=1
        return curVal
    def getCurExVec(self,curT,extraLimitBool,extraLimit):
        if self.params['active']==True:
            # get the excitability from the incoming neuron by getting it's spikelist
            thisInputL = self.inN.getParams()['spikeOuts']
            diffInVal = curT-np.asarray(thisInputL)
            diffInVal = diffInVal[diffInVal>0]
            diffInVal = diffInVal[diffInVal < self.responseKernel.responseLimit]
            if extraLimitBool == True:
                diffInVal = diffInVal[diffInVal < (curT-extraLimit)]
            if len(diffInVal) > 0:
                curVal = self.inN.params['exScale']*self.params['postScale']*np.sum(self.responseKernel.getVectorFunc(diffInVal))
            else:
                curVal = 0.0
        else:
            curVal = 0.0
        return curVal
        # get the self post     
    def updateWeights(self,curT,preBool):
        if self.params['learn'] == True:
            # If pre neuron spikes:
            if preBool == True:
                multDiff = -1
                thisInputL = self.outN.getParams()['spikeOuts']
                outP = str(self.inN.getParams()['id'])
            else:
                multDiff = 1
                thisInputL = self.inN.getParams()['spikeOuts']
                outP = str(self.outN.getParams()['id'])
            diffInVal = curT-np.asarray(thisInputL)
            diffInVal = diffInVal[diffInVal>0]
            diffInVal = diffInVal[diffInVal < self.weightResponseKernel.responseLimit]
            diffInVal = diffInVal[-diffInVal < self.weightResponseKernel.responseLimit]
            if len(diffInVal) > 0:
                curVal = self.params['learnScale']*multDiff*np.sum(self.weightResponseKernel.getVectorFunc(diffInVal))
            else:
                curVal = 0.0
            self.params['postScale'] += curVal
            if self.params['postScale']<0:
                self.params['postScale']=0
            print "Adjusting weight due to spike at ",curT," in ",outP," with ",curVal, " to get ",self.params['postScale']
            self.params['weightStore'].append([curT,self.params['postScale']])