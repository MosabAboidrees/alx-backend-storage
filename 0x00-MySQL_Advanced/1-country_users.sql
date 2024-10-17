-- Script to create a table `users` with specified attributes
-- id: integer, never null, auto-increment, and set as the primary key
-- email: string (255 characters), never null, and unique
-- name: string (255 characters)
-- country: enum of countries ('US', 'CO', 'TN'), never null, with a default value of 'US'
-- The table will have id, email, name, and country columns
-- The country column will be an enumeration of countries: US, CO, and TN

CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) UNIQUE NOT NULL,
	name VARCHAR(255),
	country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);
