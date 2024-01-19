-- a SQL script that creates a stored procedure ComputeAverageScoreForUser that
-- computes and store the average score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$ ;
CREATE PROCEDURE ComputeAverageScoreForUser(
	IN user_id INT
)
BEGIN
	DECLARE avg FLOAT;
   	SET avg=(SELECT AVG(score) FROM corrections
			     WHERE corrections.user_id=user_id);
	UPDATE users SET average_score = avg WHERE id=user_id;
	
END;
$$
DELIMITER ;
