# Rules2Lab

This repo is related to paper *Rules2Lab: from Prolog Knowledge-Base, to Learning Agents, to Norm Engineering* publised at [The 21st European Conference on Multi-Agent Systems](https://euramas.github.io/eumas2024/). 
Briefly, this paper explains how to transfrom a normative system defined in a (symbolic) logic-based programming language (e.g. Prolog) into an executable simulation environment where state transitions and (sub-symbolic) operations are performed by a procedural programming lanugage (e.g. Python).

## Overview

In this repository, you will find an implmentation of Rules2Lab approach using: 
1. Prolog lanugage for (static) definition of a normative system, in our case, a Prolog knowledge base containing norms.
2. Python lanugage for (dynamic) modification of the knowledge base following execution of actions from a user-defined set of actions.

In the file [ConstraintsHandler.py](https://github.com/fratric/Rules2Lab/blob/master/env_input/ConstraintsHandler.py) you will find a class implementing a state-action interface handling the conmunication between Prolog and Python.

This implementation is illustrated on a data-sharing enviornmnent following the [Farma Foundation Gymnasium](https://gymnasium.farama.org) (former Open-AI gym) standard for multi-agent environments. 
In this environment, a deep reinforcement learning agent performs allowed actions queried from the Prolog knowledge base. The deep-RL agent is implemented using [RLlib package](https://docs.ray.io/en/latest/rllib).

## How to use (and install) this repo

The Rules2Lab approach aims to facilitate research on integration of symbolic logic-based mothods with sub-symbolic methods to compase a simulation environment.
Since this requires installation of various Python packages, some of which might be a bit challanging to install. 
This short instalation guide describes how to use this repository such that package dependencies are increasingly complex, but only few of them are neccessary. 
For this reason, we encourgage the user to use [Conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html).

### Developing an environment with Prolog-defined knowledge base following Rules2Lab approach

The constraintHandler.py class defines basic functionalities needed for development of a multi-agent simulation environment running on top of Prolog database. 
To use the class constraintHandler.py, the **necessary requirement** is to install [pyswip](https://github.com/yuce/pyswip) package implementing comunication between Python and [SWI-Prolog](https://www.swi-prolog.org/) interpreter during simulation. 
In order to instantiate several Prolog object without interferance between objects, the [Isolated Prolog](https://github.com/mortacious/pyswip-notebook/blob/master/pyswip_notebook/prolog_notebook.py) class is included in this repository.
 
Development steps to create a new multi-agent based enviornmnet are described in Section 3 of the paper *Rules2Lab: from Prolog Knowledge-Base, to Learning Agents, to Norm Engineering*. To summarize these steps:
1. Define agent types, state variables, observable states, action constraints, and (optionally) state transitions, terminating states, or reward functions, in a Prolog file (see [benchmarks/dataSharing/rules.pl](https://github.com/fratric/Rules2Lab/blob/master/benchmarks/dataSharing/rules.pl) for example).
2. Define the initial state of the environment in a Prolog file (see [benchmarks/dataSharing/initialState.pl](https://github.com/fratric/Rules2Lab/blob/master/benchmarks/dataSharing/initialState.pl) for example).
3. Implement a reset function in Python (see [environments/dataSharing/dataSharing.py](https://github.com/fratric/Rules2Lab/blob/master/environments/dataSharing/dataSharing.py) for example), resetting the environment into the initial state.
4. Implement a step function in Python, and a state terminating method (see [environments/dataSharing/dataSharing.py](https://github.com/fratric/Rules2Lab/blob/master/environments/dataSharing/dataSharing.py) for example).
5. (Optionally) to be consistent with the Gymnasium standard, implemnet _is_done, _truncate, _get_obs, and _get_info, methods and make your environment a sub-class of the gymnasium class (see [environments/dataSharing/dataSharing.py](https://github.com/fratric/Rules2Lab/blob/master/environments/dataSharing/dataSharing.py) for example).

Additionally, usage of Python language allows for utilization of commonly used data-processing and visualization packages. 
This requires only instalation of few Python packages, e.g., networkx to visualize the knowledge base as a knowledge graph.
Since the ConstraintsHandler class can be queried for allowed actions, developed environment can be using a simple zero-intelligence random agent (see randomAllowedAction method in (see [environments/dataSharing/dataSharing.py](https://github.com/fratric/Rules2Lab/blob/master/environments/dataSharing/dataSharing.py) for example))

### Implementing RLlib agents

Since action constraints are defined in Prolog, it is easy to get allowed actions for a given state. Moreover, by convenietly structuring the Prolog code, action encoding can be easily obtained (see Section 3 of the main paper). Such encodings are usefull for deep reinforcement learning. If the prolog-based environmnet is compatible with Gymnasium standard (see step 5 in previous subsection), then it is possible to utilize deep reinforcement learning [RLlib library](https://docs.ray.io/en/latest/rllib). 
This requires installation of several requirements (see [Ray](https://docs.ray.io/en/latest/ray-overview/installation.html) website for installation guide). 

### Normative analysis of the simulation output

Definition of action constraints and other related concepts in Prolog allows for flexible modification of normative policies in the environment on run-time.
In the folder [norm_analysis](https://github.com/fratric/Rules2Lab/blob/master/norm_analysis), you may find classes helping to perform inductive logic programming (ILP) based on simulation output of agents' behaviors. 
To perform ILP, we use the [Popper](https://github.com/logic-and-learning-lab/Popper) package.
For the full example, see see [benchmarks/dataSharing/experiment.ipynb](https://github.com/fratric/Rules2Lab/blob/master/benchmarks/dataSharing/experiment.ipynb) for example. Note that the latest version of Popper is rather difficult to use with the Conda environment. 
For this reason, we redundantly include older version of Popper into this repository.
