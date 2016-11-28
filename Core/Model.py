'''
Created on 19 Jan 2016

@author: s1144899
'''
import Connection, Neuron, copy, pickle, json
globalsM = {}

class Model:
    # COPIED dictionary of Model
    params = None
    '''
    'curTime' Current Time (Double)
    'neurons' Dictionary of neurons in form {id:neuron params dictionary}
    'connections' List of connections
    'dt' Time step (Double)
    'responseLimitCDF' CDF limit of response kernel to determine when to disregard spikes after.
    'pickleOutFilePath' Path to save pickled file (String)
    'jsonOutFilePath' Path to save JSON file (String)
    '''
    def __init__(self,params):
        # Dictionary of Neuron classes, id is neuron id
        self.listOfNeurons = {} # Dictionary!
        # LIST of Connection classes
        self.listOfConnections = []
        # Turns params into the network with objects etc....
        self.params = self.copyParams(params)
        self.params['curTime'] = 0.0
        #Add Neurons before connections!
        for neuronToAddi in self.params['neurons']:
            print "Adding neuron ", neuronToAddi
            # is a dictionary so get params
            neuronToAddP = self.params['neurons'][neuronToAddi]
            # set ID as specified:
            neuronToAddP['id'] = neuronToAddi
            # add it:
            # strings in dict because of JSON storing!
            self.listOfNeurons[str(neuronToAddi)] = Neuron.addNeuron(self,neuronToAddP)
        # Add Connections after neurons:
        for connToAdd in self.params['connections']:
            print "Adding connection from ",connToAdd[0]," to ",connToAdd[1]
            inNC = self.listOfNeurons[str(connToAdd[0])]
            outNC = self.listOfNeurons[str(connToAdd[1])]
            self.listOfConnections.append(Connection.Connection(self,connToAdd[2],inNC,outNC))
    # Run the model for a set amount of time:
    def run(self,runTime):
        noTimeStepsToDo = int(runTime/self.params['dt'])
        for ti in range(noTimeStepsToDo):
            # Now go through and adjust excitations and add spikes if appropriate:
            for neuroni in self.listOfNeurons:
                neuron = self.listOfNeurons[neuroni]
                neuron.update(self.params['curTime'])
            self.params['curTime'] += self.params['dt']
            #TODO: current time printout:
            #print self.params['curTime']
    def copyParams(self,params):
        # remove any internal referencing as we don't want that!!
        if isinstance(params, dict):
            newParams = dict()
            for thisval in params:
                newParams[thisval] = self.copyParams(params[thisval])
        elif isinstance(params, list):
            newParams = list()
            for i in range(len(params)):
                newParams.append(self.copyParams(params[i]))  
        elif isinstance(params, tuple):
            newParams = tuple()
            for i in range(len(params)):
                newParams.append(self.copyParams(params[i]))  
        else:
            newParams = copy.deepcopy(params)
        return newParams

            
    def getConn(self,inN,outN):
        for conn in self.listOfConnections:
            if conn.inN.params['id']==inN and conn.outN.params['id']==outN:
                return conn
    def pickle(self):
        f = open(self.params['pickleOutFilePath'],'w')
        pickle.dump(self.params,f)
        f.close()
    def json(self):
        f = open(self.params['jsonOutFilePath'],'w')
        json.dump(self.params,f)
        f.close()
        
def modelFromPickle(filePath):
    f = open(filePath)
    params = pickle.load(f)
    f.close()
    return Model(params)

def modelFromJSON(filePath):
    f = open(filePath)
    params = json.load(f)
    f.close()
    return Model(params)
    