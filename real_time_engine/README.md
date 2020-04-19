Many changes have been made to this version of the game:

/datasets
Stores turn csvs there should be 30 of these split by 5 turn increments. It is important the naming shema remains similar. The files need to be in
order by turn number.

model_training.py
trains models and saves them. It uses the data sets from /datasets. It trains them them in the order in which they are in
the directory, this is why the naming schema is important.  

/models
directory where the saved models are stored from model_training.py. These models are loaded into a list of models when the game starts by the Real
Time Engine

RT_Engine_Class.py
This contains the engine class and the game state class (along unit classes)
RTEngine: This class loads all models from the models directory and stores them in a list (1-30) 
predicitons can be made using the prediction_alg() method.

GameState: This tracks the game state using the data pipline from server.py. Features to make predictions will be derived using this functionality
**data pipeline is from server.py, a new method was added called get_output(). test_battly.py calls this method and passes it to our games state class

The game produces a new Telmetry* Data File. It prints, from an entire game, all the turn numbers with the respective predicted winner and the
the actual winner. This done by the print_probibility_list() method in the real time engine. This information is stored in the game_predicton_info
sub folder. 

RTE_Analysis script:
This script can be found in the Engine_Analysis sub folder. When this script is ran it will summarize all files in the game_prediction_info folder
and produces an a new csv file. This new csv file is a confusion matrix break down turn by turn. (So if 100 games are ran it will be 150 turns of
confusion matrix info over those 100 games) The script produces:
True Positive
False Positives
True Negatives
False Negatvies
Accuracy 
Senistivity 
Specificity
Precision 
Fscore. 