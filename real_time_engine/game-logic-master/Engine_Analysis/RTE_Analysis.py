import os
import csv
rootdir = 'game_prediction_info'

def list_files(rootdir):
    list=[]
    r = []
    i=0
    
    for i in range(150):
        array=[0,0,0,0]
        
        list.append(array)

    for root, dirs, files in os.walk(rootdir):
        for name in files:
            fullPath=(os.path.join(root, name))
            print(fullPath)
            
            fullPathList=[]
            fullPathList=fullPath.split('/')
            
            #print(fullPathList[1])
            list=confusion_matrix_data(fullPath,list)
    
    filestr = ("predictionInfoSummary.csv")        
    fileCSV = open(filestr,"w+")
    
    #write headers
    fileCSV.write('TurnNumber'+','+'TruePositive'+','+'FalsePositive'+','+'TrueNegative'+','+'FalseNegative'+','+
    'Accuracy'+','+'Specificity'+','+'Sensitivity'+','+'Precision'+','+'F2Score')
    fileCSV.write("\n")
    
    i = 1
    for item in list:
        print(i, item)
        #accuracy
        accuracy = (int(item[0]) + int(item[2]))/(int(item[0]) + int(item[2]) + int(item[1]) + int(item[3]))
        #specificity
        if int(item[2]) + int(item[1]) == 0:
            specificity = 1
        else:
            specificity = (int(item[2]))/(int(item[2]) + int(item[1]))
        #sensitivity
        if int(item[0]) + int(item[3]) == 0:
            sensitivity = 1
        else:
            sensitivity = (int(item[0]))/(int(item[0]) + int(item[3]))
        fileCSV.write(str(i) + ",")
        #precesion
        if (int(item[0]) + int(item[1])) == 0:
            precision = 0
        else:
            precision = (int(item[0]))/(int(item[0]) + int(item[1]))
      
       #f2 score
       #division by error issue, needs to be looked into more. 
        if (float(precision) + float(sensitivity)) == 0.0 or precision * sensitivity == 0:
            f1_score = 0
        else:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", precision + sensitivity, precision * sensitivity)
            f1_score = 2 * ((float(precision) * float(sensitivity))/(precision + sensitivity))
        
        for element in item:
            fileCSV.write(str(element)+",")
        fileCSV.write(str(accuracy)+",")
        fileCSV.write(str(specificity)+",")
        fileCSV.write(str(sensitivity)+",")
        fileCSV.write(str(precision)+",")
        fileCSV.write(str(f1_score))
        fileCSV.write("\n")
        i += 1
def confusion_matrix_data(path,list):
    File = open(path,"r")
    turn_info_list=[]
    
    File.readline()
    
    #loop to iterate telemetry file
    for row in File:
        tempRow = {}
        tempRow = row.split(",")
        if int(tempRow[1]) == 1 and int(tempRow[4]) == 1:
            
            list[int(tempRow[0]) - 1][0] += 1
            print("TP>>>>>>>>>>>>>>>>>>>>>>>>>>",list[int(tempRow[0]) - 1])
        elif int(tempRow[1]) == 1 and  int(tempRow[4]) == 0:
            list[int(tempRow[0])-1][1] += 1
            print("FP")
        elif int(tempRow[1]) == 0 and  int(tempRow[4]) == 0:
            list[int(tempRow[0])-1][2] += 1
        elif int(tempRow[1]) == 0 and  int(tempRow[4]) == 1:
            list[int(tempRow[0])-1][3] += 1
            print("FN")
        else:
            print("Error")
    File.close()
    
    return list
  
list_files(rootdir)
