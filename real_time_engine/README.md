Many changes have been made to this version of the game:

/datasets
Stores turn csvs (should be/eventually) there will be 75 of these. It is important the naming shema remains similar. The files need to be in
order by turn number.

model_training.py
trains models and saves them (eventually 75). It uses the data sets from /datasets. It trains them them in the order in which they are in
the directory, this is why the naming schema is important.  

/models
directory where the saved models are stored from model_training.py

RT_Engine_Class.py
This contains the engine class and the game state class (along with group and unit classes)
RTEngine: This class loads all models from the models directory and stores them in a list (1-75) 
predicitons can be made using the prediction_alg() method.

GameState: This tracks the game state using the data pipline from server.py. Features to make predictions will be derived using this functionality
**data pipeline is from server.py, a new method was added called get_output(). test_battly.py calls this method and passes it to our RT_Engine_Class