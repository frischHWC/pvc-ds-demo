USE datagen_finance;

-- Create an iceberg table based on existing one with data already in it --
CREATE EXTERNAL TABLE stock_price_as_iceberg
STORED BY ICEBERG
AS
SELECT * FROM stock_price
;


-- Check data is present --
SELECT *
FROM stock_price_as_iceberg
LIMIT 100
;

-- Get and copy output of this select to be used later --
SELECT from_unixtime(unix_timestamp());

-- Insert a new row --
INSERT INTO stock_price_as_iceberg VALUES ('CLDR', 'Cloudera', 'Information Technology', 1000, 0, 15, 1000);

-- Run a select to make sure it is present --
SELECT * FROM stock_price_as_iceberg WHERE symbol="CLDR";


-- Run select on data before last row was inserted --
SELECT * FROM stock_price_as_iceberg FOR SYSTEM_TIME AS OF '<REPLACE WITH TIME OBTAINED EARLIER>' WHERE symbol="CLDR" ;

-- Execute a rollback --
ALTER TABLE stock_price_as_iceberg EXECUTE rollback('<REPLACE WITH TIME OBTAINED EARLIER>') ;


-- Run a select to make sure it is no longer present --
SELECT * FROM stock_price_as_iceberg WHERE symbol="CLDR";
