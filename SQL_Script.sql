create database stocks_db
SET @ref_table = '2023-10-03_05-30-00';

SELECT 
    table_name
FROM information_schema.tables
WHERE table_schema = 'stocks_db'
  AND table_name <> @ref_table
  AND (
        SELECT GROUP_CONCAT(column_name ORDER BY ordinal_position)
        FROM information_schema.columns
        WHERE table_schema = 'your_database_name'
          AND table_name = @ref_table
    ) <>
    (
        SELECT GROUP_CONCAT(column_name ORDER BY ordinal_position)
        FROM information_schema.columns
        WHERE table_schema = 'your_database_name'
          AND table_name = information_schema.tables.table_name
    );
use stocks_db;
show TABLES;

CREATE TABLE master_stock_data (
    Ticker VARCHAR(20),
    `close` FLOAT,
    `date` DATE,
    high FLOAT,
    low FLOAT,
    `month` VARCHAR(10),
    `open` FLOAT,
    volume BIGINT
);

SET GLOBAL local_infile = 1;

SELECT 
    COUNT(*) AS total_rows,
    MAX(date) AS latest_date
FROM master_stock_data;

CREATE TABLE master_stock_clean AS
SELECT DISTINCT *
FROM master_stock_data;


SET SQL_SAFE_UPDATES = 0;

DELETE FROM master_stock_data
WHERE Ticker IS NULL
   OR `date` IS NULL
   OR `open` IS NULL
   OR `close` IS NULL
   OR `open` < 0 OR `close` < 0 OR high < 0 OR low < 0;
   
SET SQL_SAFE_UPDATES = 1;

ALTER TABLE master_stock_data MODIFY `date` DATE;
ALTER TABLE master_stock_data MODIFY `open` FLOAT;
ALTER TABLE master_stock_data MODIFY `close` FLOAT;
ALTER TABLE master_stock_data MODIFY high FLOAT;
ALTER TABLE master_stock_data MODIFY low FLOAT;
ALTER TABLE master_stock_data MODIFY volume BIGINT;

CREATE TABLE processed_stock_data AS
SELECT
    Ticker,
    `date`,
    `open`,
    high,
    low,
    `close`,
    volume,
    MONTH(`date`) AS month,
    YEAR(`date`) AS year,
    (`close` - `open`) AS day_change,
    ((`close` - `open`) / `open`) * 100 AS day_return
FROM master_stock_data;

CREATE TABLE stock_summary AS
SELECT
    Ticker,
    YEAR(`date`) AS year,
    MIN(`close`) AS min_close,
    MAX(`close`) AS max_close,
    AVG(`close`) AS avg_close,
    AVG(volume) AS avg_volume,
    ((MAX(`close`) - MIN(`close`)) / MIN(`close`)) * 100 AS yearly_return
FROM processed_stock_data
GROUP BY Ticker, YEAR(`date`);

SELECT COUNT(*) FROM stock_summary;

DESCRIBE stock_summary;
DESCRIBE processed_stock_data;







