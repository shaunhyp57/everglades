# Database

## Schema
Contains schema for database used in project. Can be used to initialize a new database with appropriate fields and relations.

## Datasets
The datasets folder contains all `.csv` datasets created for the project and the associated `.sql` query to generate them from the database.

## Data Reading
This folder also contains the two following files:

* read_data.py
* run_and_upload.bat

These were used to automate the uploading of game files to the database from the game environment. 
`read_data.py` was placed in the game_telemetry folder and `run_and_upload.bat` was placed in the main directory of the game environment.