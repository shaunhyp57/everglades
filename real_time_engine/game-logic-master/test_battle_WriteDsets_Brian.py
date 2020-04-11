## Static Imports
import os
import importlib
import gym
import gym_everglades
import pdb
import math

import numpy as np

from everglades_server import server
from RT_Engine_Class import *

## Input Variables
# Agent files must include a class of the same name with a 'get_action' function
# Do not include './' in file path
agent0_file = ('agents/random_actions.py')
#agent0_file = ('agents/all_cycle.py')
#agent0_file = ('agents/base_rushV1.py')
#agent0_file = ('agents/Cycle_BRush_Turn50.py')
#agent0_file = ('agents/Cycle_BRush_Turn25.py')
#agent0_file = ('agents/cycle_targetedNode11.py')


#agent1_file = 'agents/same_commands.py'
#agent1_file = 'agents/random_actions.py'
#agent1_file = ('agents/all_cycle.py')
#agent1_file = ('agents/base_rushV1.py')
agent1_file = ('agents/Cycle_BRush_Turn50.py')
#agent1_file = ('agents/cycle_targetedNode11.py')

config_dir = 'config/'
map_file = config_dir + 'DemoMap.json'
setup_file = config_dir + 'GameSetup.json'
unit_file = config_dir + 'UnitDefinitions.json'
output_dir = 'game_telemetry/'

debug = 1
#C:\Users\brian\OneDrive\Documents\GitHub\LMCO-Everglades-Robot-Behavior-Analytics\real_time_engine\game-logic-master
## Specific Imports
agent0_name, agent0_extension = os.path.splitext(agent0_file)
agent0_mod = importlib.import_module(agent0_name.replace('/','.'), package='.Users.brian.OneDrive.Documents.GitHub.LMCO-Everglades-Robot-Behavior-Analytics.real_time_engine.game-logic-master')
#agent0_mod = importlib.import_module(agent0_name.replace('/','.'), package='.Users.brian.game-logic-master.agents.random_actions')
agent0_class = getattr(agent0_mod, os.path.basename(agent0_name))

agent1_name, agent1_extension = os.path.splitext(agent1_file)
agent1_mod = importlib.import_module(agent1_name.replace('/','.'), package='.Users.brian.OneDrive.Documents.GitHub.LMCO-Everglades-Robot-Behavior-Analytics.real_time_engine.game-logic-master')
#agent1_mod = importlib.import_module(agent1_name.replace('/','.'), package='.Users.brian.game-logic-master.agents.random_actions')
agent1_class = getattr(agent1_mod, os.path.basename(agent1_name))

## Main Script
env = gym.make('everglades-v0')
players = {}
names = {}

players[0] = agent0_class(env.num_actions_per_turn, 0)
names[0] = agent0_class.__name__
players[1] = agent1_class(env.num_actions_per_turn, 1)
names[1] = agent1_class.__name__

observations = env.reset(
        players=players,
        config_dir = config_dir,
        map_file = map_file,
        unit_file = unit_file,
        output_dir = output_dir,
        pnames = names,
        debug = debug
)

actions = {}
#Engine = RT_Engine()
## Game Loop
done = 0
turn_number=1

while not done:
    if debug:
        #env.game.debug_state()
        #data pipeline from server.py
        data_List=env.game.get_output()
        
        

    for pid in players:
        actions[pid] = players[pid].get_action( observations[pid] )

    observations, reward, done, info = env.step(actions)
    
    print("***************************")
    
    if turn_number == 1:
        Running_Game=GameState(data_List)
    #update games state after a turn runs    
    Running_Game.update_game_state(data_List,turn_number)
    featureList=Running_Game.features(turn_number)
    
    ### Show how refined list works#####
    #print(refined_list(data_List['NODE_Knowledge'],turn_number)) #all data for a turn
    #print(refined_list(data_List['NODE_Knowledge'],turn_number)[0]) # first line of data for turn
    #print(refined_list(data_List['NODE_Knowledge'],turn_number)[0][1]) #first line cell 1 (2 in csv)
    #print(refined_list(data_List['NODE_Knowledge'],turn_number)[0][1][0]) #all cells are a list/tuple so even if it is one element it must be ref. with zero
   
  
    print("Turn >>>>",turn_number)
    #predictions = Engine.prediction_alg(math.ceil(float(featureList[0])/2)-1,[featureList[1:]])
    #print(predictions)
    
    print("***************************")
    
    turn_number+=1
###Used to write turn by turn data to the CSVs which are used to build models
Running_Game.print_features_CSV()


