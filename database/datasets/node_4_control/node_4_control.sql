SELECT Win_Loss.*,
       Scores.p0_score,
       Scores.p1_score,
       node_4_control.controller, 
       node_4_control.turn_num, 
       node_4_control.control_value,
       node_4_health_p0.avg_health,
       node_4_health_p1.avg_health,
       node_4_p0_tanks.unit_count,
       node_4_p0_tanks.avg_health,
       node_4_p1_tanks.unit_count,
       node_4_p1_tanks.avg_health,
       node_4_p0_strikers.unit_count,
       node_4_p0_strikers.avg_health,
       node_4_p1_strikers.unit_count,
       node_4_p1_strikers.avg_health,
       node_4_p0_controllers.unit_count,
       node_4_p0_controllers.avg_health,
       node_4_p1_controllers.unit_count,
       node_4_p1_controllers.avg_health
FROM ( 
    SELECT Games.game_id,
           Games.player_0, 
           Games.player_1,
           Games.turn_count, 
           Games.win_state, 
           IF( Scores.p0_score > Scores.p1_score, 0, 1 )
    FROM Games
    INNER JOIN Scores
    ON Games.game_id    = Scores.game_id AND
       Games.turn_count = Scores.turn_num 
    WHERE Games.win_state = 1
    UNION
    SELECT Games.game_id, 
           Games.player_0, 
           Games.player_1,
           Games.turn_count,
           Games.win_state, 
           IF( Node_Knowledge.control_percent = -100, 1, 0 )
    FROM Games
    INNER JOIN Node_Knowledge
    ON Games.turn_count = Node_Knowledge.turn_num AND
       Games.game_id    = Node_Knowledge.game_id
    WHERE Games.win_state = 2 AND
          Node_Knowledge.node_id = 1 AND
          Node_Knowledge.player = 1
    UNION
    SELECT Games.game_id, 
           Games.player_0, 
           Games.player_1,
           Games.turn_count,
           Games.win_state, 
           -1
    FROM Games
    WHERE Games.win_state = 3 ) as Win_Loss
INNER JOIN Scores
On Win_Loss.turn_count = Scores.turn_num AND
   Win_Loss.game_id = Scores.game_id
INNER JOIN (
    SELECT N1.game_id, N1.controller, N1.turn_num, N1.control_value
    FROM Node_Control N1 
    WHERE N1.node_id = 4 AND
          ( N1.control_value >= 100 OR N1.control_value <= -100) AND
          N1.turn_num = ( SELECT MAX( N2.turn_num )
                       FROM Node_Control N2
                       WHERE N2.game_id = N1.game_id AND
                             N2.node_id = N1.node_id AND
                             ( N2.control_value >= 100 OR 
                               N2.control_value <= -100) 
    ) 
) AS node_4_control
ON node_4_control.game_id = Win_Loss.game_id
INNER JOIN (
    SELECT game_id, AVG( health ) as avg_health, turn_num, node_id
    FROM Combat
    WHERE unit_id >= 101 AND
          node_id = 4
    GROUP BY game_id, node_id, turn_num
) AS node_4_health_p0
ON node_4_health_p0.game_id = Win_Loss.game_id AND
   node_4_health_p0.turn_num = node_4_control.turn_num
INNER JOIN (
    SELECT game_id, AVG( health ) as avg_health, turn_num, node_id
    FROM Combat
    WHERE unit_id < 101 AND
          node_id = 4
    GROUP BY game_id, node_id, turn_num
) AS node_4_health_p1
ON node_4_health_p1.game_id = Win_Loss.game_id AND
   node_4_health_p1.turn_num = node_4_control.turn_num
LEFT JOIN (
    SELECT Combat.game_id, COUNT(*) as unit_count, AVG( health ) as avg_health, Combat.turn_num
    FROM Combat
    INNER JOIN Groups
    ON Combat.group_id = Groups.group_id AND
       Combat.game_id = Groups.game_id
    WHERE Combat.unit_id >= 101 AND
          Groups.unit_type = "Tank" AND
          Combat.node_id = 4
    GROUP BY game_id, turn_num 
) as node_4_p0_tanks
ON node_4_p0_tanks.game_id = Win_Loss.game_id AND
   node_4_p0_tanks.turn_num = node_4_control.turn_num
LEFT JOIN (
    SELECT Combat.game_id, COUNT(*) as unit_count, AVG( health ) as avg_health, Combat.turn_num
    FROM Combat
    INNER JOIN Groups
    ON Combat.group_id = Groups.group_id AND
       Combat.game_id = Groups.game_id
    WHERE Combat.unit_id < 101 AND
          Groups.unit_type = "Tank" AND
          Combat.node_id = 4
    GROUP BY game_id, turn_num 
) as node_4_p1_tanks
ON node_4_p1_tanks.game_id = Win_Loss.game_id AND
   node_4_p1_tanks.turn_num = node_4_control.turn_num
LEFT JOIN (
    SELECT Combat.game_id, COUNT(*) as unit_count, AVG( health ) as avg_health, Combat.turn_num
    FROM Combat
    INNER JOIN Groups
    ON Combat.group_id = Groups.group_id AND
       Combat.game_id = Groups.game_id
    WHERE Combat.unit_id >= 101 AND
          Groups.unit_type = "Striker" AND
          Combat.node_id = 4
    GROUP BY game_id, turn_num 
) as node_4_p0_strikers
ON node_4_p0_strikers.game_id = Win_Loss.game_id AND
   node_4_p0_strikers.turn_num = node_4_control.turn_num
LEFT JOIN (
    SELECT Combat.game_id, COUNT(*) as unit_count, AVG( health ) as avg_health, Combat.turn_num
    FROM Combat
    INNER JOIN Groups
    ON Combat.group_id = Groups.group_id AND
       Combat.game_id = Groups.game_id
    WHERE Combat.unit_id < 101 AND
          Groups.unit_type = "Striker" AND
          Combat.node_id = 4
    GROUP BY game_id, turn_num 
) as node_4_p1_strikers
ON node_4_p1_strikers.game_id = Win_Loss.game_id AND
   node_4_p1_strikers.turn_num = node_4_control.turn_num
LEFT JOIN (
    SELECT Combat.game_id, COUNT(*) as unit_count, AVG( health ) as avg_health, Combat.turn_num
    FROM Combat
    INNER JOIN Groups
    ON Combat.group_id = Groups.group_id AND
       Combat.game_id = Groups.game_id
    WHERE Combat.unit_id >= 101 AND
          Groups.unit_type = "Controller" AND
          Combat.node_id = 4
    GROUP BY game_id, turn_num 
) as node_4_p0_controllers
ON node_4_p0_controllers.game_id = Win_Loss.game_id AND
   node_4_p0_controllers.turn_num = node_4_control.turn_num
LEFT JOIN (
    SELECT Combat.game_id, COUNT(*) as unit_count, AVG( health ) as avg_health, Combat.turn_num
    FROM Combat
    INNER JOIN Groups
    ON Combat.group_id = Groups.group_id AND
       Combat.game_id = Groups.game_id
    WHERE Combat.unit_id < 101 AND
          Groups.unit_type = "Controller" AND
          Combat.node_id = 4
    GROUP BY game_id, turn_num 
) as node_4_p1_controllers
ON node_4_p1_controllers.game_id = Win_Loss.game_id AND
   node_4_p1_controllers.turn_num = node_4_control.turn_num
INTO OUTFILE '/var/lib/mysql-files/node_4_control.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY ''
LINES TERMINATED BY '\n';
