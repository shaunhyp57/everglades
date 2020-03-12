import os
import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

#set root directory
rootdir = 'datasets'

#
def list_files(rootdir):
    list=[]
    for root, dirs, files in os.walk(rootdir):
        list=files
    print(list)
    train_save_model(list)
   
def train_save_model(files):
    i=.01
    for file in files:
        
        train(file,i)
        i=i+.01

def train(file_name,i):
    
    #add directory to file name
    file = "datasets/" + file_name
    
    #store csv as a data frame
    df = pd.read_csv(file,index_col=0)
    
    #Set features
    feature_cols=['Player_of_1st_Unit_lost','Player_of_2nd_Unit_lost','Player_of_3rd_Unit_lost']

    #declare x feature cols and y depenenta variable
    X=df[feature_cols]
    y=df['Winner']
    #print(y.head)
    
    
    # Create the model with 100 trees
    model = RandomForestClassifier(n_estimators=1, 
                               random_state=100, 
                               max_features = 'sqrt',
                               n_jobs=-1, verbose = 0)

    # Fit on training data
    model.fit(X, y)
    filename='models/model_'+str(i)
    
    pickle.dump(model,open(filename,'wb'))

list_files(rootdir)