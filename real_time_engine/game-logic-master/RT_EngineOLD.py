import os
import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle


rootdir = 'models'


def list_files(rootdir):
    model_list=[]
    for root, dirs, files in os.walk(rootdir):
        list =[]
        list=files
    
    for file in list:
        
        model_list.append(load_model(file))
        
    #print(model_list)
    return model_list    
def load_model(file_name):
    file= "models/" + file_name
    
    return pickle.load(open(file,'rb'))
   
def predection_alg(models_list,test):
    print(model_list[0].predict_proba(test))
    print(model_list[1].predict_proba(test))
    print(model_list[2].predict_proba(test))
    print(model_list[3].predict_proba(test))
    print(model_list[4].predict_proba(test))
    print(model_list[0].predict(test))
    print(model_list[1].predict(test))
    print(model_list[2].predict(test))
    print(model_list[3].predict(test))
    print(model_list[4].predict(test))
        


model_list=list_files(rootdir)
test_prediction=[[1,1,1]]
predection_alg(model_list,test_prediction)