-- SQLite table: inventory_daily
SELECT sku, ROUND(AVG(units_demanded),1) AS avg_daily_demand, MAX(lead_time_days) AS lead_days, ROUND(AVG(units_demanded)*MAX(lead_time_days)*1.25,0) AS reorder_point FROM inventory_daily GROUP BY sku;
SELECT supplier, ROUND(AVG(lead_time_days),1) AS avg_lead_time, SUM(units_demanded) AS demand_units FROM inventory_daily GROUP BY supplier ORDER BY avg_lead_time;
WITH sku_day AS (SELECT *, ROW_NUMBER() OVER(PARTITION BY sku ORDER BY date DESC) AS rn FROM inventory_daily) SELECT sku, ending_inventory, units_demanded FROM sku_day WHERE rn=1;
