#import gymnasium as gym
from env_input.ConstraintsHandler import PrologHandler

import random
import pandas as pd
import gymnasium as gym
from  gymnasium import spaces
from gymnasium.spaces import Dict
import string
import numpy as np
import numbers

class DataSharing(gym.Env):
#class DataSharing():
    name = "Data sharing environmnet"
    rewardPenalty = -100

    def __init__(self, env_config) -> None:
        self.pathToRules = env_config['pathToRules']
        self.pathToInitialState = env_config['pathToInitialState']
        self.spaceType = env_config['spaceType']
        self.agentRL = env_config['agentRL']
        self.simThr = 0.90
        
        self.tau = 0.8

        if self.spaceType == 'encoded':
            self.handler = PrologHandler(self.name, self.pathToRules, self.pathToInitialState)
            self.allActions = self.handler.getAllActions()
            if self.agentRL is not None: #later check if agent a valid agent
                tmp = []
                for action in self.allActions:
                    if action["X0"] == self.agentRL:
                        tmp.append(action)
                self.allActions = tmp.copy()
            self.action_space = spaces.Discrete(len(self.allActions))
            self.allObservations = self.handler.getAllObservations()
            self.allObservations = [obs for obs in self.allObservations if not (obs['observable'] == 'hasAccess' and obs['X0'] != 'insurenceCompany')]
            self.observation_space_size = len(self.allObservations)
            self.observation_space = spaces.Dict(
                {
                    "action_mask": spaces.MultiBinary(self.action_space.n),
                    "observations": spaces.MultiBinary(self.observation_space_size),
                }
            )
        elif self.spaceType == 'symbolic':
            self.action_space = spaces.Text(min_length = 1, max_length = 5000, charset = string.printable)
            self.observation_space = spaces.Text(min_length = 1, max_length = 5000, charset = string.printable)
        else:
            print("warning: unknown space type")
            self.action_space = None
            self.observation_space = None

    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.nStep = 0
        self.handler = PrologHandler(self.name, self.pathToRules, self.pathToInitialState)
        if options is not None:
            for fact in options:
                self.handler.safeAddFact(fact)

        dictObservation = self.handler.getObservation()
        observation = self._get_obs(dictObservation)
        info = self._get_info(dictObservation)
        return observation, info
    
    def step_uni(self, action):
        if not isinstance(action, dict):
            action = self.allActions[action]

        

        formated_action = self.handler.print(action)[0]

        res = self.handler.makeQuery('transition(' + formated_action + ',T, R)')
        if len(res) > 1:
            print("Warning: more than one transition mapping for", formated_action)
        state_facts = res[0]['T']

        for state_fact in state_facts:
            if state_fact[0] == '+':
                self.handler.addFact(state_fact[1:])
            elif state_fact[0] == '-':
                self.handler.removeFact(state_fact[1:])
            else:
                print("Warning: only add (+) or remove (-) operators are valid")

        reward = res[0]['R']

        self.nStep = self.nStep + 1

        dictObservation = self.handler.getObservation()
        observation = self._get_obs(dictObservation) 
        info = self._get_info(dictObservation, action)       
        terminated = self._is_done(user)
        truncated = self._truncate()
        return observation, reward, terminated, truncated, info




    def step(self, action):
        
        if not isinstance(action, dict):
            action = self.allActions[action]

        reward = 0
        action_name = action['action']
        user = action['X0']

        if action_name == "nullAction":
            reward = 0
        elif action_name == 'gainAccess':
            data = action['X1']
            self.handler.addFact("hasAccess(" + user + "," + data + ")")

            reward = 10
        elif action_name == 'infer': #results in creatinon of a new data-instance
            user = action['X0']
            data = action['X1']
            model = action['X2']
            newData = "newData" + user + str(self.nStep)
            
            if data == "govData" and model == "healthRiskModel":      
                self.handler.addFact("performedInference(" + user + "," + data + "," + model+ ")")
                self.handler.addFact("data(" + newData + ")")
                self.handler.addFact("hasMatchingVars(" + newData + "," + data + ")")
                self.handler.addFact("hasMatchingVars(" + data + "," + newData + ")")
                self.handler.addFact('varNames(' + newData + ',["name", "age", "health"])')

                self.handler.addFact("hasMatchingVars(" + newData + "," + "healthRiskData" + ")")
                self.handler.addFact("hasMatchingVars(" + "healthRiskData" + "," + newData + ")")

                #get data and do inference
                newRowName = "inferredPatient"

                nameLink_Data = self.handler.makeQuery('nameLink(' + data + ',Dataclass)')
                nameLink_Data = nameLink_Data[0]['Dataclass']
                dataFrame = self.handler.makeQuery(nameLink_Data + '(DataRow)')
                dataFrame = [d['DataRow'] for d in dataFrame]

                varNames_data = self.handler.makeQuery('varNames(' + data + ',VarNames)')
                varNames_data = varNames_data[0]['VarNames']
                varNames_data = [s.decode("utf-8") for s in varNames_data]

                dataFrame = pd.DataFrame(dataFrame, columns = varNames_data)

                for indexPrivate, row in dataFrame.iterrows():

                    #prediction model
                    predictedHeatlh = 'good' if row["age"] < 35 else 'bad'

                    newrow = [row["name"], row["age"], predictedHeatlh]
                    self.handler.addFact(newRowName + "(" + str(newrow) + ")")

                self.handler.addFact("nameLink(" + newData + "," + newRowName + ")")
                
                

            #varNames_data = self.handler.makeQuery('varNames(' + data + ',VarNames)')
            #varNames_model = self.handler.makeQuery('varNames(' + model + ',VarNames)')
            #varNames_data = varNames_data[0]['VarNames']
            #varNames_model = varNames_model[0]['VarNames']

            #union_variables = set(varNames_data).union(varNames_model)
            #self.handler.addFact("varNames(" + newData + "," + union_variables + ")")

            ##get data from data
            #nameLink_Data = self.handler.makeQuery('nameLink(' + data + ',Dataclass)')
            #nameLink_Data = nameLink_Data[0]['Dataclass']
            #dataFrame = self.handler.makeQuery(nameLink_Data + '(DataRow)')

            #make inference

            #write data from extended dataframe



            reward = 500
        else:
            print("Warning: unknown action ", action_name)
        
        self.nStep = self.nStep + 1

        dictObservation = self.handler.getObservation()
        observation = self._get_obs(dictObservation) 
        info = self._get_info(dictObservation, action)       
        terminated = self._is_done(user)
        truncated = self._truncate()
        return observation, reward, terminated, truncated, info


    def _is_done(self, user):
        isBreach = False
        #for sol in self.handler.makeQuery('solution(' + user +',X1,X2)'):
        #    isBreach = True
        
        toCompareList = self.handler.makeQuery("terminate(insurenceCompany,A,B)")
        simScore = self.getSimilarityScore(toCompareList)
        if simScore > self.simThr:
            isBreach = True
        return isBreach
    
    def _truncate(self):
        if len(self.handler.getAllowedActions()) == 0:
            return True
        if self.nStep > 50:
            return True
        return False

    def _get_obs(self, state):
        if self.spaceType == 'encoded':
            return {
                'action_mask': self.maskArray(),
                'observations': self.encodeObservation(state)
                }
        elif self.spaceType == 'symbolic':
            return self.handler.print(state)
        else:
            print("Warning: unknown spaceType")
    
    def _get_info(self, observation, action = None):
        state = self.handler.getState()
        tmp_dict = {"dictObservation": observation, "dictState": state, "formatState": self.handler.print(state)}
        if action is not None:
            tmp_dict["formatAction"] = self.handler.print(action)
        if action is not None and isinstance(action, int):
            tmp_dict["dictAction"] = action
        if self.spaceType == 'encoded':
            tmp_dict["formatObesrvation"] = self.handler.print(observation)
        return tmp_dict


    def randomAllowedAction(self, agent = None): #adjust also for encoded space type
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

    def encodeObservation(self, state):
        array = np.zeros(self.observation_space_size, dtype=np.int8)
        for i, fact in enumerate(self.allObservations):
            if fact in state:
                array[i] = 1
        return array
    
    def maskArray(self):
        allowed = self.handler.getAllowedActions()
        mask_array = np.zeros(self.action_space.n, dtype=np.int8)
        for i, action in enumerate(self.allActions):
            if action in allowed:
                mask_array[i] = 1
        return mask_array
    
    def similiarityScore(self, a,b):
        s = 0
        if type(a) == type(b):
            #if isinstance(a, numbers.Number) and isinstance(b, numbers.Number):
            #    s = 1/(1+abs(a-b))
            #else:
            #    s = 1 if a == b else 0
            s = 1 if a == b else 0
        return s

    def getSimilarityScore(self, toCompareList):
        distScore = 0.0
        for pair in toCompareList:
            privateData = pair['A']
            testData = pair['B']

            #get name link
            nameLink_privateData = self.handler.makeQuery('nameLink(' + privateData + ',Dataclass)')
            nameLink_testData = self.handler.makeQuery('nameLink(' + testData + ',Dataclass)')
            if len(nameLink_privateData) == 1 and len(nameLink_testData) == 1:
                nameLink_privateData = nameLink_privateData[0]['Dataclass']
                nameLink_testData = nameLink_testData[0]['Dataclass']
                varNames_private = self.handler.makeQuery('varNames(' + privateData + ',VarNames)')
                varNames_test = self.handler.makeQuery('varNames(' + testData + ',VarNames)')
                varNames_private = varNames_private[0]['VarNames']
                varNames_test = varNames_test[0]['VarNames']    
                privateDataFrame = self.handler.makeQuery(nameLink_privateData + '(DataRow)')
                privateDataFrame = [d['DataRow'] for d in privateDataFrame]
                testDataFrame = self.handler.makeQuery(nameLink_testData + '(DataRow)')
                testDataFrame = [d['DataRow'] for d in testDataFrame]
        
                #link var names to var instances in pandas df
                privateDataFrame = pd.DataFrame(privateDataFrame, columns = varNames_private)
                testDataFrame = pd.DataFrame(testDataFrame, columns = varNames_test) 

                #iterate over two dfs and check each row of private if is present in test at score it
                common_variables = set(varNames_private).intersection(varNames_test)

                #print(privateDataFrame.shape[0])

                for indexPrivate, rowPrivate in privateDataFrame.iterrows():
                    rowDistMax = 0.0
                    for indexTest, rowTest in testDataFrame.iterrows():
                        rowDist = 0.0
                        for variable in common_variables:
                            rowDist = rowDist + self.similiarityScore(rowTest[variable], rowPrivate[variable])
                        if rowDistMax < rowDist:
                            rowDistMax = rowDist
                    #print(rowDistMax)
                    distScore = distScore + rowDistMax
                distScore = distScore/privateDataFrame.size

                
                if distScore >= 0.7:
                    print(distScore)
                    print(privateDataFrame)
                    print(testDataFrame)
                
                print("\n")

        return distScore
    

from ray.rllib.models.tf.fcnet import FullyConnectedNetwork
from ray.rllib.models.tf.tf_modelv2 import TFModelV2
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from ray.rllib.models.torch.fcnet import FullyConnectedNetwork as TorchFC
from ray.rllib.utils.framework import try_import_tf, try_import_torch
from ray.rllib.utils.torch_utils import FLOAT_MIN

tf1, tf, tfv = try_import_tf()
torch, nn = try_import_torch()

class ActionMaskModel(TFModelV2):
    """Model that handles simple discrete action masking.

    This assumes the outputs are logits for a single Categorical action dist.
    Getting this to work with a more complex output (e.g., if the action space
    is a tuple of several distributions) is also possible but left as an
    exercise to the reader.
    """

    def __init__(
        self, obs_space, action_space, num_outputs, model_config, name, **kwargs
    ):

        orig_space = getattr(obs_space, "original_space", obs_space)
        assert (
            isinstance(orig_space, Dict)
            and "action_mask" in orig_space.spaces
            and "observations" in orig_space.spaces
        )

        super().__init__(obs_space, action_space, num_outputs, model_config, name)

        self.internal_model = FullyConnectedNetwork(
            orig_space["observations"],
            action_space,
            num_outputs,
            model_config,
            name + "_internal",
        )

        # disable action masking --> will likely lead to invalid actions
        self.no_masking = model_config["custom_model_config"].get("no_masking", False)

    def forward(self, input_dict, state, seq_lens):
        # Extract the available actions tensor from the observation.
        action_mask = input_dict["obs"]["action_mask"]

        # Compute the unmasked logits.
        logits, _ = self.internal_model({"obs": input_dict["obs"]["observations"]})

        # If action masking is disabled, directly return unmasked logits
        if self.no_masking:
            return logits, state

        # Convert action_mask into a [0.0 || -inf]-type mask.
        inf_mask = tf.maximum(tf.math.log(action_mask), tf.float32.min)
        masked_logits = logits + inf_mask

        # Return masked logits.
        return masked_logits, state

    def value_function(self):
        return self.internal_model.value_function()