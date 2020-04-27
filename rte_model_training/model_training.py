import os
import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.calibration import CalibratedClassifierCV
import pickle
from sklearn.preprocessing import scale

# set root directory
rootdir = 'datasets'

def list_files(rootdir):
    list = []
    for root, dirs, files in os.walk(rootdir):
        list = files
    print(list)
    train_save_model(list)
   
def train_save_model(files):
    i = .01
    
    for file in files:
        print(file)
        train(file, i)
        i = i + .01

def train(file_name, i):
    
    #add directory to file name
    file = "datasets/" + file_name
    cols = ['Winner','Turn_Number','Point_Diff','Player1_Base_Control','Player2_Base_Control','Unit_Diff','Unit_Health_Diff']
    
    #store csv as a data frame
    df = pd.read_csv(file, names = cols, header = None, usecols = cols)
    
    #Set features
    feature_cols = ['Point_Diff', 'Player1_Base_Control', 'Player2_Base_Control', 'Unit_Diff', 'Unit_Health_Diff']

    #declare X matrix and y vector 
    X = df[feature_cols]
    y = df['Winner']
    
    # Create the model with 100 trees
    model = RandomForestClassifier(n_estimators = 64, 
                                   random_state = 100, 
                                   max_features = 'sqrt',
                                   n_jobs = -1, verbose = 0)

    # Fit on training data
    model.fit(X, y)
    
    model_sigmoid = CalibratedClassifierCV(model, cv = 2, method = 'isotonic')
    model_sigmoid.fit(X, y)
    
    filename = 'models/model_' + str(round(i,2)) + '.PICKLE'
    
    pickle.dump(model_sigmoid, open(filename,'wb'))

list_files(rootdir)
