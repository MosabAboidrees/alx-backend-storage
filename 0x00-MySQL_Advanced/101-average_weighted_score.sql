-- ComputeAverageWeightedScoreForUsers stored procedure
-- This procedure computes and stores the average weighted score for all students

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Update the average score for all users based on weighted scores from corrections and projects
    UPDATE users AS U,
           (SELECT U.id, SUM(score * weight) / SUM(weight) AS weight_avg
            FROM users AS U
            JOIN corrections AS C ON U.id = C.user_id
            JOIN projects AS P ON C.project_id = P.id
            GROUP BY U.id) AS weight
    SET U.average_score = weight.weight_avg
    WHERE U.id = weight.id;
END$$
DELIMITER ;
