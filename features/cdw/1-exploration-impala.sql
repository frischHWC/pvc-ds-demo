USE datagen_banking;

-- Basic Select ---
SELECT *
FROM atm
LIMIT 100
;

-- Accounts grouped by city and health --
SELECT count(*) AS c, atm_city, health
FROM atm
GROUP BY health , atm_city ;

