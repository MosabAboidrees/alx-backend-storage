-- 9. Optimize search and score
-- This SQL script creates an index idx_name_first_score on the table names
-- The index is created on the first letter of the name and the score

CREATE INDEX idx_name_first_score ON names (name(1), score);
