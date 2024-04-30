#from env_input import NLPhandler
from abc import ABC, abstractmethod
#import pandas as pd

class ConstraintsHandler(ABC):

    atomicStateFacts = {}
    atomicActions = {}

    def __init__ (self, env_name, pathToFile, pathToInitialState):
        self.env_name =  'ConstraintsHandler_' + env_name
        self.pathToFile = pathToFile
        self.pathToInitialState = pathToInitialState

    @abstractmethod
    def verifyElementaryActions(self):
        raise NotImplementedError("SubClass must override verifyElementaryActions method")
    
    @abstractmethod
    def getAllowedActions(self):
        raise NotImplementedError("SbuClass must override getAllowedActions method")
    


#translation:
# facts have python form {'fact': fact_name, 'X0': 1st_argument, 'X1': 2nd_argument, ....}
# actions have python form {'action': action_name, 'X0': 1st_argument, 'X1': 2nd_argument, ....}
#build in fact:
# isAction(X1, X2) states that X1 is action with X2 number of arguments
# isObservable states that X1 is fact with X2 number of arguments

#from pyswip import Prolog
from env_input.isolatedProlog import IsolatedProlog

class PrologHandler(ConstraintsHandler):

    def __init__(self, env_name, pathToFile, pathToInitialState):
        super().__init__(env_name, pathToFile, pathToInitialState)
        #self.prolog = Prolog()
        self.prolog = IsolatedProlog()
        
        self.loadRules(pathToFile)
        self.loadInitialState(pathToInitialState)

        
        self.atomicActions = {}
        for soln in self.prolog.query('isAction(X1,X2)'):
            self.atomicActions[soln['X1']] = int(soln['X2'])
        self.atomicStateFacts = {}
        for soln in self.prolog.query('isObservable(X1,X2)'):
            self.atomicStateFacts[soln['X1']] = int(soln['X2'])

        #print(self.atomicActions)
        #print(self.atomicStateFacts)

    def loadRules(self, pathToFile):
        if isinstance(pathToFile, str):
            self.prolog.consult(pathToFile)
        else:
            print("Warning: path to rules not provided")

    def loadInitialState(self, pathToInitialState):
        if isinstance(pathToInitialState, str):
            self.prolog.consult(self.pathToInitialState)
        elif isinstance(pathToInitialState, dict):
            pass #finish loading from fact dict
        else:
            print("Warning: initial state has unknown data type not provided")
     
    def addFact(self, term):
        self.prolog.assertz(term)

    def removeFact(self, term):
        self.prolog.retract(term)

    def safeAddFact(self, term):
        res = self.makeQuery(term)
        if len(res) == 0: #note that if query is true then makeQuery returns empty dict, thus len of result is one
            self.addFact(term)

    def safeRemoveFact(self, term):
        res = self.makeQuery(term)
        if len(res) == 1: #note that if query is true then makeQuery returns empty dict, thus len of result is one
            self.removeFact(term)

    def makeQuery(self, query_string):
        query_result = []
        for soln in self.prolog.query(query_string):
            #print(soln)
            query_result.append(soln)
        return query_result
    
    def formatPredicate(self, pred_name, pred_arguments):
        tmpstr = pred_name + '('
        for argument in pred_arguments:
            tmpstr = tmpstr + str(pred_arguments[argument]) + ','
        tmpstr = tmpstr[:-1]
        tmpstr = tmpstr + ')'
        #print(tmpstr)
        return tmpstr

    def printDict(self, input):
        tmpstr = ''
        if 'action' in input.keys():
            tmp_action = input.copy()
            action_name = tmp_action['action'] #string
            tmp_action.pop('action') #dict
            tmpstr = self.formatPredicate(action_name, tmp_action)
        elif 'fact' in input.keys():
            tmp_fact = input.copy()
            fact_name = tmp_fact['fact'] #string
            tmp_fact.pop('fact') #dict
            tmpstr = self.formatPredicate(fact_name, tmp_fact)
        else:
            print("Warning: no known <input.key()> in ConstraintHandler.printDict(<input>)")
        return tmpstr

    def print(self, input):
        output_list = []
        if isinstance(input, list):
            for expr in input:
                output_list.append(self.printDict(expr))
        elif isinstance(input, dict):
            output_list.append(self.printDict(input))
        else:
            print("Warning: unknown <input> type in ConstraintHandler.print(<input>)")
        return output_list

    def getAllowedActions(self):
        allowedActions = []
        for action in self.atomicActions:
            #print("atomic action: ", action)
            query_string = action + '('
            for x in range(self.atomicActions[action]):
                query_string = query_string + 'X' + str(x) + ','
            query_string = query_string[:-1]
            query_string = query_string + ')'
            for soln in self.prolog.query(query_string):
                #print(soln)
                soln['action'] = action #add name of allowed action to its arguemnts
                allowedActions.append(soln)
        return allowedActions

    #this method checks if all atomic actions in the environment exist in the file. Note that prolog alone cannot know what is action and what is fact
    def verifyElementaryActions(self):
        #load atomic action in the prolog file and then when doing step you can check the imput action (action_name) against loaded list of actions
        pass

    #retunrs all facts from the prolog database
    def getState(self):
        state_facts = []
        for fact in self.atomicStateFacts:
            #print("atomic action: ", action)
            query_string = fact + '('
            for x in range(self.atomicStateFacts[fact]):
                query_string = query_string + 'X' + str(x) + ','
            query_string = query_string[:-1]
            query_string = query_string + ')'
            for soln in self.prolog.query(query_string):
                #print(soln)
                soln['fact'] = fact #add name of fact to its arguemnts
                state_facts.append(soln)
        return state_facts











#implement safe remove later
#check if buyer is already renting IP and if yes, remove this fact (it would be cleaner to do this in prolog, ask Nils)
#    query_string = 'rentsIP(X,' + seller + ',' + ipName + ')'
#    removeFact = False
#    for soln in self.handler.prolog.query(query_string): #safe removal of a fact, can be done also using throw-catch
#        if soln['X'] == buyer:
#            removeFact = True
#            break
#    if removeFact:    
#        self.handler.removeFact("rentsIP(" + buyer + ','+ seller +  "," + ipName + ")")
    
        # def getActionListDict(self):
        # actionList = []

        # tmpdict = {}
        # tmpdict['action'] = 'addChild'
        # for company1 in self.companies:
        #     tmpdict['X0'] = company1
        #     for company2 in self.companies:
        #         tmpdict['X1'] = company2
        #         if company1 != company2:
        #             for country1 in self.countries:
        #                 tmpdict['X2'] = country1
        #                 if country1 == 'ireland':   
        #                     for country2 in self.countries:
        #                         tmpdict['X3'] = country2
        #                         actionList.append(tmpdict.copy())
        #                 else: #has the same based and tax residence
        #                     tmpdict['X3'] = country1
        #                     actionList.append(tmpdict.copy())

        # tmpdict = {}
        # tmpdict['action'] = 'rentIP'
        # for company1 in self.companies:
        #     tmpdict['X0'] = company1
        #     for company2 in self.companies:
        #         tmpdict['X1'] = company2
        #         if company1 != company2:
        #             actionList.append(tmpdict.copy())


        # return actionList