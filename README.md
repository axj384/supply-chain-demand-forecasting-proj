# Supply Chain Inventory & Demand Forecasting
**Target:** Supply Chain / Operations Analyst Intern | **Stack:** Python, SQL, Excel, Power BI, scikit-learn

## Business question
How can an inventory planner forecast SKU demand and flag items at risk of running below reorder point?

## How to run
```bash
pip install -r requirements.txt
python analysis.py
```
Outputs: `outputs/sku_replenishment.csv`, `outputs/forecast_evaluation.csv`, `figures/demand_forecast.png`, `outputs/inventory.db`.

## Methods
Compare a naive last-observation forecast against a rolling 7-day mean on held-out dates. Calculate MAE. Reorder point is an **illustrative heuristic**: mean daily demand × lead time × 1.25. It is not a statistically calibrated service-level policy.

## Power BI layout
Cards: Total Units Demanded, Average Lead Time, SKUs Below Reorder Point. Visuals: Daily Demand, SKU Reorder Point vs On-Hand, Supplier Lead Times. Slicers: SKU and Supplier.

**Limitations:** All data are synthetic. Ending inventory is a simplified simulated balance and may not reflect actual lost sales or supplier constraints.
