Select G.game_id, S.p0_score, S.p1_score, D.player, G.turn_count, G.win_state, IF(S.p0_score > S.p1_score, 0, 1)
FROM Games G, Scores S, Groups G2, Disband D
WHERE G.win_state = 1 AND
      G.turn_count = S.turn_num AND
      G.game_id = S.game_id AND
      G.game_id = G2.game_id AND
      G.game_id = D.game_id AND
      G2.unit_type = "Tank" AND
      D.group_id = G2.group_id AND
      D.turn_num = ( Select MIN(turn_num)
                     FROM Disband D2, Groups G3
                     WHERE G3.group_id = D2.group_id AND
                           G3.game_id = D2.game_id AND
                           G3.unit_type = "Tank" AND
                           G.game_id = G3.game_id )
UNION
Select G.game_id, S.p0_score, S.p1_score, D.player, G.turn_count, G.win_state, IF(N.control_percent = -100, 1, 0)
FROM Games G, Scores S, Groups G2, Disband D, Node_Knowledge N
WHERE G.win_state = 2 AND
      G.turn_count = S.turn_num AND
      G.turn_count = N.turn_num AND
      G.game_id = N.game_id AND
      G.game_id = S.game_id AND
      G.game_id = G2.game_id AND
      G.game_id = D.game_id AND
      G2.unit_type = "Tank" AND
      N.node_id = 1 AND
      N.player = 1 AND
      D.group_id = G2.group_id AND
      D.turn_num = ( Select MIN(turn_num)
                     FROM Disband D2, Groups G3
                     WHERE G3.group_id = D2.group_id AND
                           G3.game_id = D2.game_id AND
                           G3.unit_type = "Tank" AND
                           G.game_id = G3.game_id )
INTO OUTFILE '/var/lib/mysql-files/first_tank_disband.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY ''
LINES TERMINATED BY '\n';