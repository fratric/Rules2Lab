
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random


class NormExplorer:

    #later extend to be able to use multiple agents
    def __init__(self):
        self.instances = {}
        self.selectedInstances = {}
        self.id = 0

    #get,set functions

    def addInstance(self, trajectory, unique = None):
        if unique is not None:
            if unique == 'endStateEqualTo':
                toAdd = True
                for id, traj in self.instances.items():
                    if traj.endStateEqualTo(trajectory) == True:
                        toAdd = False
                        break
                if toAdd == True:
                    self.instances[self.id] = trajectory
                    self.id = self.id + 1
        else:
            self.instances[self.id] = trajectory
            self.id = self.id + 1

    #selection

    def getRandomIdStep(self):
        id = random.choice(range(self.id))
        step = random.choice(range(self.instances[id].tlen))
        return id, step    
    
    def maxRewardIdStep(self):
        if self.id == 0:
            return None
        max_reward = max(self.instances[0].reward)
        max_id = 0
        max_t = self.instances[max_id].reward.index(max_reward)
        for id, traj in self.instances.items():
            tmp_max = max(traj.reward)
            if tmp_max > max_reward:
                max_reward = tmp_max
                max_id = id
                max_t = self.instances[max_id].reward.index(max_reward)
        return max_id, max_t
    
    #plotting functions

    def plotReward(self, id):
        plt.plot(self.instances[id].reward)
        plt.xlabel('step')
        plt.ylabel('reward')
        plt.show()

    def plotRewards(self):
        for id, traj in self.instances.items():
            plt.plot(traj.reward)
        plt.xlabel('step')
        plt.ylabel('reward')
        plt.show()
    
    def getTotalRewards(self):
        totalRewards = []
        for id, traj in self.instances.items():
            totalRewards.append(traj.cumReward)
        return totalRewards
    
    def getLastRewards(self):
        lastRewards = []
        for id, traj in self.instances.items():
            lastRewards.append(traj.reward[-1])
        return lastRewards

    #this will probably be deleted once I decide it's not needed
    def getRewardDistanceMerix(self, data):
        dim = len(data)
        rewM =  np.zeros((dim,dim))
        for i, (idA, sliceA) in enumerate(data.items()):
            for j, (idB, sliceB) in enumerate(data.items()):
                if i > j:
                    r1 = sliceA['reward']
                    r2 = sliceB['reward']
                    rewM[i,j] =  abs(r1 - r2)
                    rewM[j,i] = rewM[i,j]
        #plt.matshow(rewM)
        #plt.colorbar()
        return rewM


class KnowledgeGraphExlorer(NormExplorer):

    def __init__(self):
        super().__init__()


    def from_data_frame_to_knowledge_graph(self, state, all_nodes = False):
        G = nx.DiGraph()
        
        if all_nodes == True:
            for fact in state['state']:
                if len(fact) == 2:
                    G.add_node(fact['X0'])

        df = state['triplets']
        for _, row in df.iterrows():
            G.add_edge(row['head'], row['tail'], relation=row['relation'])
        
        entities = {}
        for node in G.nodes():
            if {'X0': node, 'fact': 'country'} in state['state']:
                entities[node] = {'entity': 'country'}
            elif {'X0': node, 'fact': 'company'} in state['state']:
                entities[node] = {'entity': 'company'}
            else:
                print('Warning: unknonw entity type')

        nx.set_node_attributes(G, entities)
        return G

    #knowledge graph embedding

    def kernel(self, KG):
        pass  

    #basic similarity
    def sim(self, G, H, tau):
        if isinstance(G, nx.DiGraph) and isinstance(H, nx.DiGraph):
            minv = np.inf
            for v in nx.optimize_graph_edit_distance(G, H, upper_bound = tau, 
                                                     edge_match = lambda a,b: a['relation'] == b['relation'],
                                                     node_match = lambda a,b: a['entity'] == b['entity']):
                minv = v
            return minv
        #elif isinstance(G, np.ndarray) and isinstance(H, np.ndarray):
        #    return np.linalg.norm(G-H)
        else:
            print("Warning: unknown data type in Sim function")
    
    def distance_matrix(self, tau, useSelected = False): #assumes the similarity function is a metric, ie. is symmetric
        graphs = {}
        if useSelected is True:
            dim = len(self.selectedInstances)
            M =  np.zeros((dim,dim))
            for id, traj in self.selectedInstances.items():
                graphs[id] = self.from_data_frame_to_knowledge_graph(traj.info[-1])
        else:
            dim = len(self.instances)
            M =  np.zeros((dim,dim))
            for id, traj in self.instances.items():
                graphs[id] = self.from_data_frame_to_knowledge_graph(traj.info[-1])

        for i, (idA, G) in enumerate(graphs.items()):
            for j, (idB, H) in enumerate(graphs.items()):
                if i > j:
                    simv = self.sim(G,H, tau)
                    #note that infinite distances are present in matrix
                    M[i,j] = simv
                    M[j,i] = simv
                    print(i,j)
        return M
    
    #https://stackoverflow.com/questions/12122021/python-implementation-of-a-graph-similarity-grading-algorithm
    def select_k(self, spectrum, minimum_energy = 0.9):
        running_total = 0.0
        total = sum(spectrum)
        if total == 0.0:
            return len(spectrum)
        for i in range(len(spectrum)):
            running_total += spectrum[i]
            if running_total / total >= minimum_energy:
                return i + 1
        return len(spectrum)

    #laplacian1 = nx.spectrum.laplacian_spectrum(graph1)
    #laplacian2 = nx.spectrum.laplacian_spectrum(graph2)

    #k1 = select_k(laplacian1)   
    #k2 = select_k(laplacian2)
    #k = min(k1, k2)

    #similarity = sum((laplacian1[:k] - laplacian2[:k])**2)

    
    #plotting

    def plotKnowledgeGraph(self, id, step = -1):
        data = self.instances[id].info[step]
        G = self.from_data_frame_to_knowledge_graph(data)
        pos = nx.circular_layout(G)
        labels = nx.get_edge_attributes(G, 'relation')
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, font_size=10, node_size=700, node_color='lightblue', edge_color='gray', alpha=0.6, connectionstyle='arc3, rad = 0.1')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8, label_pos=0.3, verticalalignment='baseline')
        plt.title('Knowledge Graph (id=' + str(id) + ', t=' + str(step) + ')')
        plt.show()