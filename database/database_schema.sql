CREATE TABLE Agents (
  script CHAR(50) NOT NULL,
  PRIMARY KEY( script )
);

CREATE TABLE Games (
  game_id    INT NOT NULL AUTO_INCREMENT,
  player_0   CHAR(50),
  player_1   CHAR(50),
  turn_count INT,
  win_state  INT,
  directory  CHAR(100),
  PRIMARY KEY( game_id ),
  FOREIGN KEY( player_0 ) REFERENCES Agents(script),
  FOREIGN KEY( player_1 ) REFERENCES Agents(script),
  UNIQUE KEY( directory )
);

CREATE TABLE Groups (
  game_id   INT,
  player    TINYINT,
  group_id  INT,
  unit_type CHAR(15),
  PRIMARY KEY( game_id, group_id ),
  FOREIGN KEY( game_id ) REFERENCES Games(game_id)
);

CREATE TABLE Units (
  game_id  INT,
  group_id INT,
  unit_id  INT,
  PRIMARY KEY( game_id, group_id, unit_id ),
  FOREIGN KEY( game_id )  REFERENCES Games(game_id),
  FOREIGN KEY( game_id, group_id ) REFERENCES Groups(game_id, group_id)
);

CREATE TABLE Nodes (
  game_id INT,
  node_id INT,
  PRIMARY KEY( game_id, node_id ),
  FOREIGN KEY( game_id ) REFERENCES Games(game_id)
);

CREATE TABLE Scores (
  game_id  INT,
  turn_num INT,
  p0_score INT,
  p1_score INT,
  PRIMARY KEY( game_id, turn_num ),
  FOREIGN KEY( game_id ) REFERENCES Games(game_id)
);

CREATE TABLE Combat (
  game_id  INT,
  node_id  INT,
  turn_num INT,
  group_id INT,
  unit_id  INT,
  health   FLOAT,
  PRIMARY KEY( game_id, unit_id, turn_num ),
  FOREIGN KEY( game_id ) REFERENCES Games(game_id),
  FOREIGN KEY( game_id, node_id ) REFERENCES Nodes(game_id, node_id),
  FOREIGN KEY( game_id, group_id ) REFERENCES Groups(game_id, group_id),
  FOREIGN KEY( game_id, group_id, unit_id ) REFERENCES Units(game_id, group_id, unit_id)
);

CREATE TABLE Disband (
  game_id   INT,
  player    TINYINT,
  group_id  INT,
  turn_num  INT,
  PRIMARY KEY( game_id, group_id ),
  FOREIGN KEY( game_id ) REFERENCES Games(game_id),
  FOREIGN KEY( game_id, group_id ) REFERENCES Groups(game_id, group_id)
);

CREATE TABLE Group_Knowledge (
  game_id     INT,
  player      TINYINT,
  turn_num    INT,
  unit_type   CHAR(15),
  unit_count  INT,
  in_transit  TINYINT,
  node        INT,
  destination INT,
  FOREIGN KEY( game_id ) REFERENCES Games(game_id),
  FOREIGN KEY( game_id, node ) REFERENCES Nodes(game_id, node_id)
);

CREATE TABLE Group_Move (
  game_id     INT,
  turn_num    INT,
  player      TINYINT,
  group_id    INT,
  node        INT,
  destination INT,
  move_state  char(15),
  FOREIGN KEY( game_id ) REFERENCES Games(game_id),
  FOREIGN KEY( game_id, group_id ) REFERENCES Groups(game_id, group_id),
  FOREIGN KEY( game_id, node ) REFERENCES Nodes(game_id, node_id),
  FOREIGN KEY( game_id, destination ) REFERENCES Nodes(game_id, node_id)
);

CREATE TABLE Node_Control (
  game_id       INT,
  turn_num      INT,
  node_id       INT,
  controller    TINYINT,
  control_value INT,
  controlled    CHAR(10),
  PRIMARY KEY( game_id, turn_num, node_id ),
  FOREIGN KEY( game_id ) REFERENCES Games(game_id),
  FOREIGN KEY( game_id, node_id ) REFERENCES Nodes(game_id, node_id)
);

CREATE TABLE Node_Knowledge (
  game_id         INT,
  turn_num        INT,
  player          TINYINT,
  node_id         INT,
  knowledge       INT,
  controller      INT,
  control_percent INT,
  PRIMARY KEY( game_id, turn_num, player, node_id ),
  FOREIGN KEY( game_id ) REFERENCES Games(game_id),
  FOREIGN KEY( game_id, node_id ) REFERENCES Nodes(game_id, node_id)
);