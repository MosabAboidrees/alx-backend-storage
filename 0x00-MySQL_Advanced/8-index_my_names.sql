-- Create an index on the 'name' column of the 'names' table
-- The index will use only the first character of the 'name' column

CREATE INDEX idx_name_first
ON names (name(1));
