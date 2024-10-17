-- Task: Create a function SafeDiv that divides the first number by the second number or returns 0 if the second number is equal to 0.
-- a: The numerator for the division
-- b: The denominator for the division
-- This function performs a safe division,
-- returning 0 if the denominator is 0

DELIMITER //

CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS FLOAT
BEGIN
	RETURN (IF (b = 0, 0, a / b));
END //

DELIMITER ;
