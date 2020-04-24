import csv
import os
import mysql.connector
from mysql.connector import Error
import shutil

game_id = None

#Insert gameid into each dict in an array
def insertGameId( arr ):
  for x in arr:
    x['game_id'] = game_id

def executeInsertQuery( query, args ):
  try:
    cursor.executemany( query, args )
  except Error as e:
    print(query)
    print(e)

#Connect to DB
conn = None
try:
  conn = mysql.connector.connect( host='', 
                                  database='',
                                  user='',
                                  password='')
  if conn.is_connected():
    print("Connection to database established")
except Error as e:
  print(e)

dir_path = os.path.dirname( os.path.realpath( __file__ ) )

files = os.listdir()

#Delete non-folder values
files.remove(".gitignore")
files.remove("db_connect.py")
files.remove("read_data.py")

for directory in files:
  game_log_dir = '\\' + directory

  game_scores   = '\\GAME_Scores\\Telem_GAME_Scores'
  group_combat  = '\\GROUP_CombatUpdate\\Telem_GROUP_CombatUpdate' 
  group_disband = '\\GROUP_Disband\\Telem_GROUP_Disband'
  group_init    = '\\GROUP_Initialization\\Telem_GROUP_Initialization'
  group_know    = '\\GROUP_Knowledge\\Telem_GROUP_Knowledge'
  group_move    = '\\GROUP_MoveUpdate\\Telem_GROUP_MoveUpdate'
  node_update   = '\\NODE_ControlUpdate\\Telem_NODE_ControlUpdate'
  node_know     = '\\NODE_Knowledge\\Telem_NODE_Knowledge'
  player_tags   = '\\PLAYER_Tags\\Telem_PLAYER_Tags'

  #Init table information storage
  agents = []
  game = dict()
  groups = []
  units = []
  nodes = [dict() for x in range(11)]
  scores = []
  combat_instances = []
  disband_instances = []
  group_knowledge = []
  group_movement = []
  node_control = []
  node_knowledge = []

  # Add directory to game dict
  game['directory'] = game_log_dir.strip('\\')

  # Read from player_tags csv file
  with open( dir_path + game_log_dir + player_tags, newline='' ) as csvfile:
    reader = csv.DictReader( csvfile, delimiter=',' )
    for row in reader:
      #Add agents to agent table info
      agents.append( (row['player1'],) )
      agents.append( (row['player2'],) )
      #Store game info in game dictionary
      game['player_0'] = row['player1']
      game['player_1'] = row['player2']
      game['turn_count'] = int( float( row['0'] ) )

  # read from game_scores csv file
  with open( dir_path + game_log_dir + game_scores, newline='' ) as csvfile:
    reader = csv.DictReader( csvfile, delimiter=',' )
    for row in reader:
      #Record row in score dictionary
      score = dict()
      score['turn_num'] = int( float ( row['0'] ) )
      score['p0_score'] = row['player1']
      score['p1_score'] = row['player2']
      #Store dictionary in scores array
      scores.append( score )

  #Store last win status in game dictionary
  game['win_state'] = row['status']

  # Read from group_init csv file
  with open( dir_path + game_log_dir + group_init, newline='' ) as csvfile:
    reader = csv.DictReader( csvfile, delimiter=',' )
    for row in reader:
      #Record row info in group dictionary
      group = dict()
      group['player'] = int( row['player'] )
      group['group_id'] = row['group']
      group['unit_type'] = row['types'].strip('[]')
      groups.append( group )
      #Record unit id info
      starting_id = int( row['start'].strip('[]') )
      unit_count = int( row['count'].strip('[]') )
      for i in range( unit_count ):
        #Record unit info in unit dictionary
        unit = dict()
        unit['group_id'] = row['group']
        unit['unit_id'] = starting_id + i + 1
        units.append( unit )

  #Initialize Node Info
  i = 0
  for node in nodes:
    nodes[i]['node_id'] = i + 1
    i = i + 1

  # Read from group_combat csv file
  with open( dir_path + game_log_dir + group_combat, newline='' ) as csvfile:
    reader = csv.DictReader( csvfile, delimiter=',' )
    for row in reader:
      #Read in parallel arrays
      group_array = row['groups'].strip('[]').split(';')
      unit_array = row['units'].strip('[]').split(';')
      health_array = row['health'].strip('[]').split(';')
      for group, unit, health in zip(group_array, unit_array, health_array):
        #Record combat info in dict 
        combat = dict()
        combat['node_id'] = row['node']
        combat['turn_num'] = int( float( row['0'] ) )
        combat['group_id'] = group
        combat['unit_id'] = unit
        combat['health'] = float( health )
        combat_instances.append( combat )

  # Read from group_disband csv file
  with open( dir_path + game_log_dir + group_disband, newline='' ) as csvfile:
    reader = csv.DictReader( csvfile, delimiter=',' )
    for row in reader:
      #Record disband info in dict
      disband = dict()
      disband['player'] = int( row['player'] )
      disband['group_id'] = row['group']
      disband['turn_num'] = int( float( row['0'] ) )
      disband_instances.append( disband )

  # Read from group_knowledge csv file
  with open( dir_path + game_log_dir + group_know, newline='' ) as csvfile:
    reader = csv.DictReader( csvfile, delimiter=',' )
    for row in reader:
      #Record knowledge info into dict
      type_array = row['unitTypes'].strip('[]').split(';')
      count_array = row['unitCount'].strip('[]').split(';')
      for unit_type, count in zip( type_array, count_array ):
        knowledge = dict()
        knowledge['player'] = int( row['player'] )
        knowledge['turn_num'] = int( float( row['0'] ) )
        knowledge['in_transit'] = int( row['status'] )
        knowledge['node'] = row['node1']
        knowledge['destination'] = row['node2']
        knowledge['unit_type'] = unit_type
        knowledge['unit_count'] = unit_count
        group_knowledge.append( knowledge )

  # Read from group_movement csv file
  with open( dir_path + game_log_dir + group_move, newline='' ) as csvfile:
    reader = csv.DictReader( csvfile, delimiter=',' )
    for row in reader:
      #Record movement info into dict
      movement = dict()
      movement['turn_num'] = int( float( row['0'] ) )
      movement['player'] = int( row['player'] )
      movement['group_id'] = row['group']
      movement['node'] = row['start']
      movement['destination'] = row['destination']
      movement['move_state'] = row['status']
      group_movement.append( movement )

  # Read from node_control csv file
  with open( dir_path + game_log_dir + node_update, newline='' ) as csvfile:
    reader = csv.DictReader( csvfile, delimiter=',' )
    for row in reader:
      #Record control info into dict
      control = dict()
      control['turn_num'] = int( float( row['0'] ) )
      control['node_id'] = int( row['player'] )
      control['controlled'] = row['controlvalue'].strip('')
      control['controller'] = int( row['node'] )
      control['control_value'] = row['faction']
      node_control.append( control )

  # Read from node_knowledge csv file
  with open( dir_path + game_log_dir + node_know, newline='' ) as csvfile:
    reader = csv.DictReader( csvfile, delimiter=',' )
    for row in reader:
      #Record knowledge info into dict
      node_array = row['nodes'].strip('[]').split(';')
      know_array = row['knowledge'].strip('[]').split(';')
      controller_array = row['controller'].strip('[]').split(';')
      percent_array = row['percent'].strip('[]').split(';')
      for node, know, controller, percent in zip( node_array, know_array, controller_array, percent_array ):
        knowledge = dict()
        knowledge['turn_num'] = int( float( row['0'] ) )
        knowledge['player'] = int( row['player'] )
        knowledge['node_id'] = node
        knowledge['knowledge'] = know
        knowledge['controller'] = int( controller )
        knowledge['control_percent'] = percent
        node_knowledge.append( knowledge ) 

  print('Game logs read')

  cursor = conn.cursor()

  #Insert agents into agent table
  query = "INSERT IGNORE INTO Agents(script) " \
          "VALUES( %s )"
  executeInsertQuery( query, agents )

  #Insert game into games table
  query = "INSERT INTO Games(player_0, player_1, turn_count, win_state, " \
          "directory) " \
          "VALUES( %(player_0)s, %(player_1)s, %(turn_count)s, %(win_state)s, " \
          "%(directory)s )"
  try:
    cursor.execute( query, game )
    game_id = cursor.lastrowid
  except Error as e:
    print(e)

  #Insert game_id into data
  insertGameId( groups )
  insertGameId( units )
  insertGameId( nodes )
  insertGameId( scores )
  insertGameId( combat_instances )
  insertGameId( disband_instances )
  insertGameId( group_knowledge )
  insertGameId( group_movement )
  insertGameId( node_control )
  insertGameId( node_knowledge )

  #Insert groups into groups table
  query = "INSERT INTO Groups(game_id, player, group_id, unit_type) " \
          "VALUES( %(game_id)s, %(player)s, %(group_id)s, %(unit_type)s )"
  executeInsertQuery( query, groups )

  #Insert units into units table
  query = "INSERT INTO Units(game_id, group_id, unit_id) " \
          "VALUES( %(game_id)s, %(group_id)s, %(unit_id)s )"
  executeInsertQuery( query, units )

  #Insert nodes into nodes table
  query = "INSERT INTO Nodes(game_id, node_id) " \
          "VALUES( %(game_id)s, %(node_id)s )"
  executeInsertQuery( query, nodes )

  #Insert scores into scores table
  query = "INSERT INTO Scores(game_id, turn_num, p0_score, p1_score) " \
          "VALUES( %(game_id)s, %(turn_num)s, %(p0_score)s, %(p1_score)s )"
  executeInsertQuery( query, scores )

  #Insert combat_instances into Combat table
  query = "INSERT INTO Combat(game_id, node_id, turn_num, group_id, unit_id, health) " \
          "VALUES( %(game_id)s, %(node_id)s, %(turn_num)s, %(group_id)s, %(unit_id)s, %(health)s )"
  executeInsertQuery( query, combat_instances )

  #Insert disband_instances into Disband table
  query = "INSERT INTO Disband(game_id, player, group_id, turn_num) " \
          "VALUES( %(game_id)s, %(player)s, %(group_id)s, %(turn_num)s )"
  executeInsertQuery( query, disband_instances )

  #Insert group_knowledge into Group_Knowledge table
  query = "INSERT INTO Group_Knowledge(game_id, player, turn_num, unit_type, " \
          "unit_count, in_transit, node, destination) " \
          "VALUES( %(game_id)s, %(player)s, %(turn_num)s, %(unit_type)s, " \
          "%(unit_count)s, %(in_transit)s, %(node)s, %(destination)s )"
  executeInsertQuery( query, group_knowledge )

  #Insert group_movement into Group_Move table
  query = "INSERT INTO Group_Move(game_id, turn_num, player, group_id, node, " \
          "destination, move_state) " \
          "VALUES( %(game_id)s, %(turn_num)s, %(player)s, %(group_id)s, " \
          "%(node)s, %(destination)s, %(move_state)s )"
  #executeInsertQuery( query, group_movement )

  #Insert node_control into Node_Control table
  query = "INSERT INTO Node_Control(game_id, turn_num, node_id, controller, " \
          "control_value, controlled) " \
          "VALUES(%(game_id)s, %(turn_num)s, %(node_id)s, %(controller)s, " \
          "%(control_value)s, %(controlled)s)"
  executeInsertQuery( query, node_control )

  #Inesrt node_knowledge into Node_Knowledge table
  query = "INSERT INTO Node_Knowledge(game_id, turn_num, player, node_id, " \
          "knowledge, controller, control_percent) " \
          "VALUES(%(game_id)s, %(turn_num)s, %(player)s, %(node_id)s, " \
          "%(knowledge)s, %(controller)s, %(control_percent)s)"
  executeInsertQuery( query, node_knowledge )

  conn.commit()
  print("Transactions Completed")
  shutil.rmtree( dir_path + game_log_dir )