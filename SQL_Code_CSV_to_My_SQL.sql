CREATE DATABASE stock_data_db;
USE stock_data_db;

CREATE TABLE stock_prices (
    ticker VARCHAR(20),
    date DATETIME,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume BIGINT,
    month VARCHAR(7),

    PRIMARY KEY (ticker, date)
);

SELECT * FROM stock_prices LIMIT 10;

SELECT COUNT(*) FROM stock_prices;

SELECT * FROM stock_prices WHERE ticker='SBIN' ORDER BY date;

SELECT ticker, month, AVG(close) AS avg_close
FROM stock_prices
GROUP BY ticker, month;

SELECT COUNT(*) AS null_count
FROM stock_prices
WHERE ticker IS NULL OR "date" IS NULL OR "open" IS NULL OR high IS NULL OR low IS NULL OR "close" IS NULL OR volume is NULL OR "month" is NULL

USE stock_data_db;
SHOW COLUMNS FROM stock_prices;

DESCRIBE stock_prices;

#Check wrong date format:
SELECT ticker, "date "
FROM stock_prices
WHERE "date" IS NULL OR "date" = '';

USE stock_data_db;
DESCRIBE stock_prices;
USE stock_data_db;
DESCRIBE sector_data;

ALTER TABLE sector_data
DROP COLUMN COMPANY_NAME,
DROP COLUMN SYMBOL_CLEAN;

ALTER TABLE sector_data 
ADD COLUMN COMPANY_NAME VARCHAR(255),
ADD COLUMN SYMBOL_CLEAN VARCHAR(255);

-- Disable safe updates
SET SQL_SAFE_UPDATES = 0;

UPDATE sector_data
SET 
    COMPANY_NAME = TRIM(SUBSTRING_INDEX(Symbol, ':', 1)),
    SYMBOL_CLEAN = TRIM(SUBSTRING_INDEX(Symbol, ':', -1));

SELECT 
    COUNT(*) AS total_rows,
    SUM(CASE WHEN COMPANY_NAME IS NULL THEN 1 ELSE 0 END) AS null_company,
    SUM(CASE WHEN SYMBOL_CLEAN IS NULL THEN 1 ELSE 0 END) AS null_symbol,
    SUM(CASE WHEN sector IS NULL THEN 1 ELSE 0 END) AS null_sector
FROM sector_data;

SELECT *
FROM sector_data
WHERE COMPANY_NAME IS NULL
   OR SYMBOL_CLEAN IS NULL
   OR sector IS NULL;

SELECT 
    COUNT(*) AS total_rows,
    SUM(CASE WHEN ticker IS NULL THEN 1 ELSE 0 END) AS null_ticker,
    SUM(CASE WHEN date IS NULL THEN 1 ELSE 0 END) AS null_date,
    SUM(CASE WHEN open IS NULL THEN 1 ELSE 0 END) AS null_open,
    SUM(CASE WHEN high IS NULL THEN 1 ELSE 0 END) AS null_high,
    SUM(CASE WHEN low IS NULL THEN 1 ELSE 0 END) AS null_low,
    SUM(CASE WHEN close IS NULL THEN 1 ELSE 0 END) AS null_close,
    SUM(CASE WHEN volume IS NULL THEN 1 ELSE 0 END) AS null_volume,
    SUM(CASE WHEN month IS NULL THEN 1 ELSE 0 END) AS null_month
FROM stock_prices;

SELECT s.ticker
FROM stock_prices s
LEFT JOIN sector_data sd
    ON s.ticker = sd.SYMBOL_CLEAN
WHERE sd.SYMBOL_CLEAN IS NULL;

SELECT sd.SYMBOL_CLEAN
FROM sector_data sd
LEFT JOIN stock_prices s
    ON sd.SYMBOL_CLEAN = s.ticker
WHERE s.ticker IS NULL;

SELECT 
    COUNT(*) AS total_stock_tickers,
    SUM(CASE WHEN s.ticker = sd.SYMBOL_CLEAN THEN 1 ELSE 0 END) AS matching_count
FROM stock_prices s
LEFT JOIN sector_data sd
    ON s.ticker = sd.SYMBOL_CLEAN;

SELECT DISTINCT s.ticker AS unmatched_ticker
FROM stock_prices s
LEFT JOIN sector_data sd
    ON s.ticker = sd.SYMBOL_CLEAN
WHERE sd.SYMBOL_CLEAN IS NULL;

UPDATE stock_prices
SET ticker = 'ADANIGREEN'
WHERE ticker = 'ADANIENT';

UPDATE stock_prices
SET ticker = 'AIRTEL'
WHERE ticker = 'BHARTIARTL';

UPDATE stock_prices
SET ticker = 'TATACONSUMER'
WHERE ticker = 'TATACONSUM';

INSERT INTO sector_data (COMPANY, SECTOR, SYMBOL, COMPANY_NAME, SYMBOL_CLEAN)
VALUES ('BRITANNIA', 'FMCG', 'BRITANNIA: BRITANNIA', 'BRITANNIA', 'BRITANNIA');

SELECT DISTINCT s.ticker AS unmatched_ticker
FROM stock_prices s
LEFT JOIN sector_data sd
    ON s.ticker = sd.SYMBOL_CLEAN
WHERE sd.SYMBOL_CLEAN IS NULL;

SELECT DISTINCT ticker
FROM stock_prices
ORDER BY ticker;

SELECT DISTINCT sd.SYMBOL_CLEAN AS unmatched_symbol
FROM sector_data sd
LEFT JOIN stock_prices s
    ON sd.SYMBOL_CLEAN = s.ticker
WHERE s.ticker IS NULL
ORDER BY sd.SYMBOL_CLEAN;

SELECT DISTINCT s.ticker AS unmatched_ticker
FROM stock_prices s
LEFT JOIN sector_data sd
    ON s.ticker = sd.SYMBOL_CLEAN
WHERE sd.SYMBOL_CLEAN IS NULL
ORDER BY s.ticker;
