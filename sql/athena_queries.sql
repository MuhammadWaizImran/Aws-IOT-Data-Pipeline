-- ─────────────────────────────────────
-- SETUP — Run these first
-- ─────────────────────────────────────

CREATE DATABASE iot_analytics;

CREATE EXTERNAL TABLE iot_analytics.sensor_data (
    id          BIGINT,
    device_id   STRING,
    temperature FLOAT,
    humidity    FLOAT,
    recorded_at STRING
)
STORED AS PARQUET
LOCATION 's3://iot-enriched-bucket-waiz/enriched-data/';


-- ─────────────────────────────────────
-- QUERIES
-- ─────────────────────────────────────

-- All data
SELECT * FROM iot_analytics.sensor_data LIMIT 20;

-- Total rows
SELECT COUNT(*) AS total FROM iot_analytics.sensor_data;

-- Average per device
SELECT
    device_id,
    ROUND(AVG(temperature), 2) AS avg_temp,
    ROUND(AVG(humidity), 2)    AS avg_humidity,
    COUNT(*)                   AS readings
FROM iot_analytics.sensor_data
GROUP BY device_id
ORDER BY avg_temp DESC;

-- High temperature alerts
SELECT device_id, temperature, humidity, recorded_at
FROM iot_analytics.sensor_data
WHERE temperature > 35
ORDER BY temperature DESC;

-- Overall stats
SELECT
    COUNT(*)                   AS total_readings,
    COUNT(DISTINCT device_id)  AS active_devices,
    ROUND(AVG(temperature), 2) AS avg_temp,
    MIN(temperature)           AS min_temp,
    MAX(temperature)           AS max_temp,
    ROUND(AVG(humidity), 2)    AS avg_humidity
FROM iot_analytics.sensor_data;
