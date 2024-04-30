class Instance:
    def __init__(self): #trajectory_type: ('s-a-s', 'a-s', 's-a')
        self.observation = []
        self.action = []
        self.new_observation = []
        self.reward = []
        self.info = []

        self.cumReward = 0
        self.tlen = 0

        self.truncated = False
        self.terminated = False
        self.label = 0 #either -1,0,1 (non-compliant, unknonwn, compliant), or score from (-1,1) interval 
        

    def append(self, observation, action, new_observation, reward, info):
        self.observation.append(observation)
        self.action.append(action)
        self.new_observation.append(new_observation)
        self.reward.append(reward)
        self.info.append(info)
        self.cumReward = self.cumReward + reward
        self.tlen = self.tlen + 1
    
    def actionEqualTo(self, instance):
        pass

    def stateEqualTo(self, instance):
        pass

    def endStateEqualTo(self, instance):
        if self.tlen > 0:
            if self.info[-1] == instance.info[-1]:
                return True
            else:
                return False
        else:
            print("Wraning: too short instance")
            return None


    def getSlice(self, t = -1):
        if t < self.tlen:
            return {'observation': self.observation[t],
                    'action': self.action[t],
                    'new_observation': self.new_observation[t],
                    'reward': self.reward[t],
                    'info': self.info[t]}
        else:
            print("Warning: time step out of bounds")

