-- Task: List all bands with Glam rock as their main style, ranked by their longevity
-- Column names: band_name and lifespan (in years until 2022)
-- You should use attributes formed and split for computing the lifespan

-- Import the table dump: metal_bands.sql.zip

-- Select bands with Glam rock as their main style and calculate their lifespan
SELECT band_name, IFNULL(split, 2022) - IFNULL(formed, 0) AS lifespan
FROM metal_bands
WHERE style = '%Glam rock%'
ORDER BY lifespan DESC;
