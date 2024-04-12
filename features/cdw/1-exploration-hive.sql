USE datagen_banking;

-- Basic Select ---
SELECT *
FROM bank_account
LIMIT 100
;

-- Accounts grouped by city and type of card --
SELECT count(*) AS c, city_of_residence, card_type
FROM bank_account
GROUP BY card_type , city_of_residence ;

-- Cities with the most number of bank accounts --
SELECT count(*) as number_of_accounts, city_of_residence  
FROM bank_account 
GROUP BY city_of_residence 
ORDER BY number_of_accounts DESC
LIMIT 20;
