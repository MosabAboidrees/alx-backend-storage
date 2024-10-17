-- Task: Create an index on the table names for the first letter of name and the score
-- Create the index idx_name_first_score on the first letter of name and score

CREATE INDEX idx_name_first_score ON names (name(1), score);
