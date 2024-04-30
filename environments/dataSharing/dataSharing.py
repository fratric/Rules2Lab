#import gymnasium as gym
import random
from env_input.ConstraintsHandler import PrologHandler

import pandas as pd

#class Cooking(gym.Env):
class DataSharing():
    name = "Data sharing environmnet"
    rewardPenalty = -100

    def __init__(self, env_config) -> None:
        self.pathToRules = env_config['pathToRules']
        self.pathToInitialState = env_config['pathToInitialState']
        #self.handler = PrologHandler(self.name, self.pathToRules, self.pathToInitialState)

        
    
    def reset(self, init_facts = None):
        self.handler = PrologHandler(self.name, self.pathToRules, self.pathToInitialState)
        if init_facts is not None:
            for fact in init_facts:
                self.handler.safeAddFact(fact)

        state = self.handler.getState()
        observation = self._get_obs(state)
        info = self._get_info(state)
        return observation, info
    
    def step(self, action):
        
        action_name = action['action'] #string
        if action == "nullAction":
            pass
        elif action_name == 'gainAccess':
            user = action['X0']
            data = action['X1']
            self.handler.addFact("hasAccess(" + user + "," + data + ")")
            reward = self.getReward(action)
        elif action_name == 'merge':
            user = action['X0']
            data = action['X1']
            model = action['X2']
            #resuts in a creation of a new columm in dataA
        else:
            print("Warning: no action executed")
        
        reward = self.getReward(action)

        state = self.handler.getState()
        info = self._get_info(state)
        observation = self._get_obs(state)        
        terminated = self._is_done()
        truncated = self._truncate()
        return observation, reward, terminated, truncated, info


    
    def _is_done(self):
        isBreach = False
        for sol in self.handler.makeQuery('solution(insurenceCompany,X1,X2)'):
            isBreach = True
        return isBreach
    
    def _truncate(self):
        if len(self.handler.getAllowedActions()) == 0:
            return True
        return False

    def _get_obs(self, state):
        return state
    
    def _get_info(self, state):
        return {
            "prologState": self.handler.print(state),
            "state": state
        }
    
    def getReward(self, action):
        reward = 0
        action_name = action['action']
        if action_name == 'gainAccess':
            user = action['X0']
            data = action['X1']
            sol = self.handler.makeQuery("cost(" + data + ",X" + ")")
            if len(sol) == 0:
                print("Error: no dataCost found for ", data)
            if len(sol) > 1:
                print("Warning: multiple dataCost found for ", data)
            reward = -1*sol[0]["X"]
        elif action_name == 'merge':
            user = action['X0']
            dataA = action['X1']
            dataB = action['X2']
            #for now now cost on merge action
            reward = 0.0
            #sol = self.handler.makeQuery("dataCost(" + dataC + ",X" + ")")
            #if len(sol) == 0:
            #    print("Error: no dataCost found for ", dataC)
            #if len(sol) > 1:
            #    print("Warning: multiple dataCost found for ", dataC)
            #reward = sol[0]["X"]
        else:
            reward = self.rewardPenalty
            print("Warning: no action executed")
        return reward


    def randomAllowedAction(self, agent = None):
        allowedActs = self.handler.getAllowedActions()
        if agent is not None:
            tmp = []
            for action in allowedActs:
                if action['X0'] == agent:
                    tmp.append(action)
            allowedActs = tmp
        if len(allowedActs) > 0:
            randAct = random.choice(allowedActs)
            return randAct
        return {'action': "NullAction"}
    

    def getAllObservations(self):
        #predicates = ['isChildOf', 'based', 'taxResidence', 'rentsIP']
        predicates = self.handler.atomicStateFacts

        observationList = []
        for fact in predicates:
            query_string = "sc_" + fact + '(X0,X1)'
            res = self.handler.makeQuery(query_string)
            for sol in res:
                sol['fact'] = fact
            observationList = observationList + res
        return observationList
    
    def getAllActions(self):
        #actions = ['addChild', 'rentIP']
        actions = self.handler.atomicActions

        actionList = []
        for action in actions:
            if action == 'inferData':
                query_string = "sc_" + action + '(X0,X1,X2,X3)'
            else: #action == 'gainDataAccess' or action == 'gainModelAccess' or action == 'reconstructionAttack':
                query_string = "sc_" + action + '(X0,X1)'
            res = self.handler.makeQuery(query_string)
            for sol in res:
                sol['action'] = action
            actionList = actionList + res
        return actionList
    
    def getStateAsTriplets(self, state):
        head = []
        relation = []
        tail = []
        for fact in state:
            #tmp_fact = fact.copy()
            #fact_name = fact['fact']
            if len(fact) == 3:
                #print(fact)
                head.append(fact['X0'])
                relation.append(fact['fact'])
                tail.append(fact['X1'])
        return pd.DataFrame({'head': head, 'relation': relation, 'tail': tail})
    

# data(govData). %goverment
# data(healthRiskData). %hospital
# data(auditData). %consultancy
# data(electionData). %goverment
# data(geriatryData).
# data(countryHealthData).
# data(surnameMapData).
# data(ageMapData).

# model(healthRiskModel). %hospital
# model(countryHealthModel).
# model(ageMapModel).
# model(surnameMapModel).


class Data:
    def __init__(self):
        
        self.govData = pd.DataFrame(columns = ['varName', 'varAge'])

        healthRiskDict = {'varName': ['Jack', 'Amanda', 'Bob', 'Alice', 'Jeff'], 
                          'varAge': [84, 27, 33, 48, 56],
                          'varHealth': [1,0,0,1,1] #1 = risk, 0 = no risk
                          }
        self.healthRiskData = pd.DataFrame(healthRiskDict, columns = ['varName', 'varAge', 'varHealth'])
        self.auditData = pd.DataFrame()
        self.electionData = pd.DataFrame(columns = ['varAge'])
        self.geriatryData = pd.DataFrame(columns = ['varAge', 'varHealth'])
        self.countryHealthData = pd.DataFrame(columns = ['varHealth'])
        self.surnameMapData = pd.DataFrame(columns = ['varName'])
        self.ageMapData = pd.DataFrame(columns = ['ageMapData'])


from sklearn.linear_model import LogisticRegression

class Models:

    class Model:
        def __init__(self, inputVars, outputVars, model):
            self.inputVars = inputVars
            self.outputVars = outputVars
            self.allVars = inputVars + outputVars
            self.model = model

    def __init__(self):
        self.healthRiskModel = self.Model(inputVars=['varAge'], outputVars=['varHealth'], model = LogisticRegression())


# varName(govData).
# varName(healthRiskData).
# varName(surnameMapData).
# varName(surnameMapModel).

# varAge(govData).
# varAge(healthRiskData).
# varAge(electionData).
# varAge(geriatryData).
# varAge(healthRiskModel).
# varAge(ageMapData).
# varAge(ageMapModel).

# varHealth(healthRiskData).
# varHealth(geriatryData).
# varHealth(healthRiskModel).
# varHealth(countryHealthData).
# varHealth(countryHealthModel).