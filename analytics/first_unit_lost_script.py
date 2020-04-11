import os
import csv
rootdir = 'game_telemetry'

def list_files(rootdir):
    Unit_Type_Dict={"[Striker]":1,"[Tank]":2,"[Controller]":3}
    list=[-1,1]
    r = []
    i=0
    fileCSV = open("firstUnitLost_target4_randact","w")
    fileCSV.write("numberOfTurns"+','+
    "winType"+','+"player_0"+','+
    "player_1"+','+"unitLossTurn"+','+
    "unitLostPlayer"+","+"unitLostType"+','+
    "combinedStat"+','+"winner"+'\n')
    for root, dirs, files in os.walk(rootdir):

        dirs.sort()
        files.sort()

        for name in files:
            fullPath=(os.path.join(root, name))
            #print(fullPath)
            
            fullPathList=[]
            fullPathList=fullPath.split('/')
            current_File = str(fullPathList[3:])
            current_File=current_File.replace('[','').replace(']','').replace("'",'')
            
            if current_File ==  "Telem_GAME_Scores":
                #print("current file is Telem_GAME_Scores")
                TFG_List=get_Turns(fullPath)

            if current_File ==  "Telem_GROUP_Disband":
                #print("current file is Telem_GROUP_Disband")
                TGD_List=get_dispand_info(fullPath)
                #print("TGD List")
                #print(TGD_List)
            
            if current_File ==  "Telem_GROUP_Initialization":
                #print("current file is Telem_GROUP_Initialization")
                TFI_List=get_Initialization_info(fullPath)
                #print(TFI_List)
                
            if current_File ==  "Telem_PLAYER_Tags":
                #print("current file is Telem_PLAYER_Tags")
                #print("TFG Game_Scores: " + str(TFG_List))
                #print("TGD Group Disband: " + str(TGD_List))
                #print("TFI Group Init: " + str(TFI_List))

                fileCSV.write(str(TFG_List[0])+','+
                str(TFG_List[1])+','+
                str(TFG_List[2])+','+
                str(TFG_List[3])+','+
                str(TGD_List[0])+','+
                str(TGD_List[1])+','+str(Unit_Type_Dict.get(TFI_List[int(TGD_List[2])-1]))+','+
                str(list[(int(TGD_List[1]))]*int((Unit_Type_Dict.get(TFI_List[int(TGD_List[2])-1]))))+','+
                str(TFG_List[4])+'\n')
      
    return r

def get_Turns(path):
    game_scores_File = open(path,"r")
    turn_info_list=[]
    
    
    game_scores_File.readline()
    #loop to iterate telemetry file
    for row in game_scores_File:
        tempRow={}
        tempRow=row.split(",")
        turns=tempRow[0]
        type_Of_Win = tempRow[3]
        player0score = tempRow[1]
        player1score = tempRow[2]
        if int(tempRow[1]) > int(tempRow[2]):
            winner = 0 
        else: 
            winner = 1
    turn_info_list.append(turns)
    turn_info_list.append(type_Of_Win)
    turn_info_list.append(player0score)
    turn_info_list.append(player1score)
    turn_info_list.append(winner)
    game_scores_File.close()
    return turn_info_list
    
def get_dispand_info(path):
    dispand_info=open(path,'r')
    dispand_info_list=[]
    
    dispand_info.readline()
    for row in dispand_info:
        currentRow=[]
        currentRow=row.split(",")

        dispand_info_list.append(currentRow[0])
        dispand_info_list.append(currentRow[1])
        dispand_info_list.append(currentRow[2])
        #print(dispand_info_list[1])
    dispand_info.close()
    return dispand_info_list
        
def get_Initialization_info(path):
    initialization_info=open(path,'r')
    initialization_info_list=[]
    
    initialization_info.readline()
    for row in initialization_info:
        initialRow=[]
        initialRow=row.split(",")
        
        initialization_info_list.append(initialRow[4])
    initialization_info.close()
    return initialization_info_list
  
list_files(rootdir)