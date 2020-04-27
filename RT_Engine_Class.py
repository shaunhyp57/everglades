import os
import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
import pickle
import math
import datetime


rootdir = 'model_training/models'

class RT_Engine:
    #loads the machine learning models that are saved in rootdir
    #this models are generated from model_training.py using the csvs in the datasets directory
    def __init__(self):
        self.model_list = []
        for root, dirs, files in os.walk(rootdir):
            list = []
            list = files
        
        for file in list:
            file_temp = "models/" + file
        
            current_model=pickle.load(open(file_temp, 'rb'))
            self.model_list.append(current_model)
            
    # prediction algorithm
    # takes in turn number and a list of features
    # returns a list of P1, P2 and Tie probabilities

    def prediction_alg(self, turn, feature_list):
        pred = self.model_list[turn].predict_proba(feature_list)
        pred_list = []
        pred_list.append(float(pred[0][0]) * 100)
        pred_list.append(float(pred[0][1]) * 100)
        
        return pred_list
      
    def predict_player(self, turn, feature_list):
        predicted_player = self.model_list[turn].predict(feature_list)
        return predicted_player
    
class GameState:
    def __init__(self, data_list):
        
        '''Intialize game state '''
        self.CSV_features = []
        self.probability_list = []
        
        # set starting scores
        self.player_one_score = 0
        self.player_two_score = 0
        
        # these lists are for reference purposes on which player owns which group
        self.player_one_groups = []
        self.player_two_groups = []
        
        # game groups and game units store a list of the Group objects and Unit objects
        # this is so the groups (0-23) are consistant by list index as are units (2-201)
        self.game_groups = []
        self.game_units = []
        
        # beginning board state by control and percentage of control.Hard coded for now
        self.node_controller = [0,-1,-1,-1,-1,-1,-1,-1,-1,-1,1]
        self.node_percent = [100,0,0,0,0,0,0,0,0,0,-100]
        
        # generate the GROUP_Initialization data passing turn number as zero
        initialization_info = refined_list(data_list['GROUP_Initialization'], 0)
        
        # populate begining games state of player group list and a list of group objects
        for element in initialization_info:
            if element[1][0] == '0':
               self.player_one_groups.append(element[2][0])
               self.game_groups.append(Group(element))
               
            elif element[1][0] == '1':
               self.player_two_groups.append(element[2][0])
               self.game_groups.append(Group(element))
        
        # dictionary for unit type health reference
        dict = {"Striker":1, "Controller":2, "Tank":3}
        
        # creates a list of units from GROUP_Initialization data for each line(element) of csv data
        ## BUG ## Turns out Unit 1 does not exist. Units start at 2 so Group one is 2-9 all the way to 2-201 total units
        
        # these two lines append dummy units at zero health and group zero so the index match the true unit numbers
        self.game_units.append(Unit(0,0,-1)) 
        self.game_units.append(Unit(0,0,-1))
        for element in initialization_info:
            if element[1][0] != 'player':  #skip the first line
                
               #create units of a given type from Start (id) to Start (Id) + count. 
               for x in range(int(element[5][0]), (int(element[5][0]) + int(element[6][0]))):
                    self.game_units.append(Unit(dict.get(element[4][0]), element[2][0], element[1][0]))
    # end of init        

    ''' Update game state: primary engine to maintain turn by turn game state'''
    
    # updated game state, should be called after actions every turn
    def update_game_state(self, data_list, turn_number):
        
        # update node information
        node_control_info = refined_list(data_list['NODE_Knowledge'], turn_number)
        self.update_node_controller(node_control_info)
        self.update_node_controller(node_control_info)
        self.update_node_percent(node_control_info)
        self.update_node_percent(node_control_info)
        
        # update player scores to game_scores[line][cell][index]
        game_scores = refined_list(data_list['GAME_Scores'], turn_number)
        self.player_one_score = game_scores[0][1][0]
        self.player_two_score = game_scores[0][2][0]
        
        # update unit health
        unit_combat = refined_list(data_list['GROUP_CombatUpdate'], turn_number)
        
        # for each combat that occured this turn update the unit with it's new health
        for lines in unit_combat:
            for unitID , unitHealth in zip(lines[4], lines[5]):
                self.game_units[int(unitID)].set_health(unitHealth)

    '''update_game_state utility and utility to build feature lists'''
    # get a list of reaming units for each player. 
    # returns: units[player1 unit count][player2 unit count]
    def get_player_remaining_units(self):
        p1Units = 0
        p2Units = 0
        
        # loop through the entire unit list, check the player and if any given unit health is zero
        for unit in self.game_units:
            if unit.get_unit_owner() is '0'  and round(float(unit.get_Unit_Health())) is not 0:
                p1Units = p1Units +1
            if unit.get_unit_owner() is '1'  and round(float(unit.get_Unit_Health())) is not 0:    
                p2Units = p2Units + 1
        return p1Units, p2Units
    
    # returns a list of : [player 1 avg unit health][player 2 avg unit health][player 1 % remaining][Player 2 % remaining]
    # note: the below calculations use hard coded starting unit values (100 units) and starting avg unit health (2.04)
    def get_avg_unit_health(self):
        p1Health = 0.0
        p2Health = 0.0
        
        for unit in self.game_units:
            if unit.get_unit_owner() is '0':
                p1Health = p1Health + float(unit.get_Unit_Health())
            if unit.get_unit_owner() is '1':
                p2Health = p2Health + float(unit.get_Unit_Health())
        return round(p1Health/100.00, 4), round(p2Health/100.00, 4),round(((p1Health/100)/2.04) * 100, 2),round(((p2Health/100)/2.04) * 100, 2)    
    
    # updates node controllers
    def update_node_controller(self,telem_list):
        
        # set the list to what player one KNOWS about the nodes
        self.node_controller=telem_list[0][4]
        
        # updates the list with what player two knows
        for index, element in enumerate(telem_list[1][4]):
            if element is '1':
                self.node_controller[index] = 1
 
    # updates node percent
    def update_node_percent(self,telem_list):
    
        # sets node percent to what player one KNOWS about the nodes
        self.node_percent = telem_list[0][5]
        
        # this loop updates the list with node information player 2 KNOWS about
        for index, element in enumerate(telem_list[1][5]):
            if round(float(element)) != 0:
                self.node_percent[index] = element
    
    # returns player-base control values
    # used as a feature to evaluate if a player is close to capturing a base. 
    def get_opponent_base_control(self):
        p1_baseControl = 0
        p2_baseControl = 0
        
        if float(self.node_percent[0]) < 0.0:
            p2_baseControl = self.node_percent[0]
        
        if float(self.node_percent[10]) > 0.0:
            p1_baseControl = self.node_percent[10]
        return p1_baseControl, p2_baseControl
    
    # this will be used if we decide to print to csvs
    def determine_winner(self, turn_number):
        # if it is turn 150, determine who won by points
        if turn_number == 150:
            if int(self.player_one_score) > int(self.player_two_score):
                return 0
            elif int(self.player_two_score) > int(self.player_one_score):
                return 1
            # tie
            else:
                return 3
            
        ### HAS NOT BEEN TESTED ### Need scripts that capture bases often
        # check if a player won by base capture
        if self.node_controller[0] == '1':
            return 1
        elif self.node_controller[10] =='0':
            return 0
        else:
            return None
         
    # custom feature list, there potentially could be variants of feature lists
    # returns turn number, the difference in points, Player 1 base % control, Play 2 base % control, difference in units, difference in unit health
    # this is also appened to the CSV_feature list that is used to print to turn summary CSVs
    def features(self,turn_number):
        feature_list = []
        feature_list.append(turn_number)
        point_diff = int(self.player_one_score) - int(self.player_two_score)
        feature_list.append(point_diff)
        
        player1_Base_controll = float(self.get_opponent_base_control()[0])
        player2_Base_controll = float(self.get_opponent_base_control()[1])
        feature_list.append(player1_Base_controll)
        feature_list.append(player2_Base_controll)
        
        unit_diff = int(self.get_player_remaining_units()[0]) - int(self.get_player_remaining_units()[1])
        feature_list.append(unit_diff)
        
        unit_health_diff = round(float(self.get_avg_unit_health()[0]) - float(self.get_avg_unit_health()[1]), 5)
        feature_list.append(unit_health_diff)
 
        # append to the CSV that can be used to build data sets
        self.CSV_features.append(feature_list)
        return feature_list
    
    # used to generate data sets
    # writes any features stored in CSV_features to CSV files turn by turn (in sets of 5 turns) to \datasets
    # used to train models for the prediction algorithm: model_training.py
    def print_features_CSV(self):
        
        for item in self.CSV_features:
            model_turn = math.ceil(float(item[0])/5)
            
            model_turn = round(model_turn * 0.01, 2)
            filestr=("datasets/Game_summary" + str(model_turn) + ".csv")
            
            fileCSV = open(filestr, "a+")
            fileCSV.write(str(self.determine_winner(150)) + ',')
            
            for element in item:
                fileCSV.write(str(element) + ',')
            fileCSV.write("\n")
            
    def append_proba_list(self, turn, predicted_winner, prob_list):
        APL_list = []
        APL_list.append(turn)
        APL_list.append(predicted_winner[0])
        APL_list.append(prob_list[0])
        APL_list.append(prob_list[1])
      
        self.probability_list.append(APL_list)
    
    def print_probability_list(self):
        date = datetime.datetime.today()
        date_frmt = date.strftime('%Y.%m.%d-%H.%M.%S')
        
        filestr = ("game_prediction_info/prediction_summary"+ date_frmt + ".csv")
        probCSV = open(filestr, "a+")
        probCSV.write("Turn" + "," + "Predicted_Winner" + "," + "P1_Prob" + "," + "P2_Prob" + "," + "Winner" + "\n")
        
        for row in self.probability_list:
            for element in row:
                probCSV.write(str(element) + ',')
            
            probCSV.write(str(self.determine_winner(150)))
            probCSV.write('\n')
       
    def print_summary(self):
        print("~~~~~~~~   Board State    ~~~~~~~~~")
        print("Node Control" + str(self.node_controller))
        print(self.node_percent)
        print("Player One Score : " + self.player_one_score)
        print("Player Two Score : " + self.player_two_score)
        print("Opponents Base Control Player 1: " + str(self.get_opponent_base_control()[0]) + "%")
        print("Opponents Base Control Player 2: " + str(self.get_opponent_base_control()[1]) + "%")
        print("Player 1 Remainging Units : " + str(self.get_player_remaining_units()[0]))
        print("Player 2 Remainging Units : " + str(self.get_player_remaining_units()[1]))
        print("Player 1 Units Average Remaining Health : " + str(self.get_avg_unit_health()[0]) +"\t" + str(self.get_avg_unit_health()[2]) +'%')
        print("Player 2 Units Average Remaining Health : " + str(self.get_avg_unit_health()[1]) +"\t"+ str(self.get_avg_unit_health()[3]) +'%')
    
    def print_game_stats(self, pred_list,turn_number):
        node_dict = {0: "P1", 1: "P2", -1: "N"}
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   ","Turn: ",turn_number,"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   Board State    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for i in range(1, 12):
            print("[",i,"]","\t", end = "")
        print("")
        
        for i in range(11):
            print(node_dict.get(int(self.node_controller[i])),"\t", end = "")
        print("")
        
        for i in range(11):
            print(round(float((self.node_percent[i]))),"%","\t",end = "")
        
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("\t\t\t","Player 1:","\t\t\t","Player 2:")
        print("\t\t\t",self.player_one_score,"\t","   -----Points-----","\t",self.player_two_score)
        print("\t\t\t",round(float(self.get_opponent_base_control()[0])),"\t","  ---Base Control---","\t",round(float(self.get_opponent_base_control()[1])))
        print("\t\t\t",self.get_player_remaining_units()[0],"\t"," --Units Remaining--","\t",self.get_player_remaining_units()[1])
        print("\t\t\t",round(float(self.get_avg_unit_health()[0]),2),"\t"," --Avg. Unit Health--","\t",round(float(self.get_avg_unit_health()[1]),2))
        print("\t\t\t",str(round(float(pred_list[0]))) + "%","\t","--Chance of Winning--","\t",str(round(float(pred_list[1]))) + "%")
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< End of Turn",turn_number, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
  
# leaving the Group functionality in place although it will be used very little due to the MoveUpdate bug
class Group:
    def __init__(self, initial_info):
        self.unit_type = initial_info[4][0]
        self.location = initial_info[3][0]
        self.status = "READY_TO_MOVE"
    
    def get_group_type(self):
        return self.unit_type
    def get_group_status(self):
        return self.status
    def get_group_location(self):
        return self.location
    def set_group_status(self, status):
        self.status = status
    def set_location(self,loc):
        self.location = loc
        
# units store their health and what group they belong to
class Unit:
    def __init__(self, health, groupID, owner):
        self.health = health
        self.groupID = groupID
        self.player = owner
        
    def get_Unit_Health(self):
        return self.health
    
    def get_groupID(self):
        return self.groupID
    
    def get_unit_owner(self):
        return self.player
    
    def set_health(self,health):
        self.health = health
        
# takes in  specified telemetry data set (ex. telem_list[GAME_Scores]) and turn number. It returns a list of [lines][cell][index] of all information
## in that data file for that turn. 
def refined_list(telem_list, turn_number):
        
    edit_list = []
    final_list = []
    
    # split each row
    for items in telem_list:
        temp_list = (items.split(","))
                   
        # check if it is current turn
        if round(float(temp_list[0])) == turn_number:
            
            # cleans the data, removes brackets and splits sub list by ' ; '
            for elements in temp_list:  
                stripped_element = elements.strip("[]")
                split_element = stripped_element.split(';')
                edit_list.append(split_element)
            final_list.append(edit_list)
            edit_list = []
                    
    return final_list        

