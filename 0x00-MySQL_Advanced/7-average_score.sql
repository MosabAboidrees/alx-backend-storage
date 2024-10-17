-- Task: Create a stored procedure ComputeAverageScoreForUser that computes and stores the average score for a student

DELIMITER $$;

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
	DECLARE avg_score FLOAT;

	-- Calculate the average score for the given user_id
	SELECT AVG(score) INTO avg_score
	FROM corrections
	WHERE corrections.user_id = user_id;

	-- Update the user's average_score in the users table
	UPDATE users
	SET average_score = avg_score
	WHERE id = user_id;
END;$$

DELIMITER ;