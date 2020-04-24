SELECT Win_Loss.*,
       Scores.p0_score,
       Scores.p1_score,
       First_Group_Loss.turn_num,
       First_Group_Loss.player,
       First_Group_Loss.unit_type,
       First_Group_Loss.group_id
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
       SELECT D.game_id, D.turn_num, D.player, G.unit_type, D.group_id
       FROM Disband D, Groups G
       WHERE D.game_id = G.game_id AND
             D.group_id = G.group_id AND
             D.turn_num = ( SELECT MIN( turn_num )
                            FROM Disband D2, Groups G2
                            WHERE G2.game_id = D2.game_id AND
                                  G2.group_id = D2.group_id AND
                                  G.game_id = G2.game_id )
) as First_Group_Loss
ON First_Group_Loss.game_id = Win_Loss.game_id
INTO OUTFILE '/var/lib/mysql-files/first_group_disband.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY ''
LINES TERMINATED BY '\n';