-- ComputeAverageWeightedScoreForUser stored procedure
-- This procedure computes and stores the average weighted score for a student

DELIMITER $$
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
	-- Update the user's average score based on the average weighted score
	-- of the quizzes they have taken
	UPDATE users
	SET average_score = (
		SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight)
		FROM corrections
		INNER JOIN projects ON projects.id = corrections.project_id
		WHERE corrections.user_id = user_id
	)
	WHERE user.id = user_id;
END $$
DELIMITER ;
