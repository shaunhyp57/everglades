SELECT Games.*, IF(Scores.p0_score > Scores.p1_score, 0, 1)
FROM Games
INNER JOIN Scores
ON Games.game_id    = Scores.game_id AND
   Games.turn_count = Scores.turn_num 
WHERE Games.win_state = 1
UNION
SELECT Games.*, IF(Node_Knowledge.control_percent = -100, 1, 0)
FROM Games
INNER JOIN Node_Knowledge
ON Games.turn_count = Node_Knowledge.turn_num AND
   Games.game_id    = Node_Knowledge.game_id
WHERE Games.win_state = 2 AND
      Node_Knowledge.node_id = 1 AND
      Node_Knowledge.player = 1
UNION
SELECT Games.*, -1
FROM Games
WHERE Games.win_state = 3