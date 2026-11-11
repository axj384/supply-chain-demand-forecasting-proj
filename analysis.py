from pathlib import Path
import pandas as pd, numpy as np, sqlite3, matplotlib.pyplot as plt
p=Path(__file__).resolve().parent;d=pd.read_csv(p/'data/sample_data.csv').sort_values(['sku','date']);(p/'outputs').mkdir(exist_ok=True)
rows=[];evaluations=[]
for sku,g in d.groupby('sku'):
 g=g.sort_values('date'); train=g.iloc[:-14];test=g.iloc[-14:]
 history=list(train.units_demanded); actual=[];pred_naive=[];pred_roll=[]
 for y in test.units_demanded:
  pred_naive.append(history[-1]);pred_roll.append(float(np.mean(history[-7:])));actual.append(y);history.append(y)
 evaluations.append([sku,np.mean(np.abs(np.array(actual)-pred_naive)),np.mean(np.abs(np.array(actual)-pred_roll))])
 mean=train.units_demanded.mean();lead=int(g.lead_time_days.iloc[-1]);stock=int(g.ending_inventory.iloc[-1]);rp=int(np.ceil(mean*lead*1.25))
 rows.append([sku,g.supplier.iloc[-1],round(mean,2),lead,stock,rp,stock<rp])
replen=pd.DataFrame(rows,columns=['sku','supplier','avg_daily_demand','lead_time_days','on_hand','reorder_point','reorder_flag']);replen.to_csv(p/'outputs/sku_replenishment.csv',index=False)
ev=pd.DataFrame(evaluations,columns=['sku','naive_MAE','rolling7_MAE']);ev.to_csv(p/'outputs/forecast_evaluation.csv',index=False)
g=d[d.sku==d.sku.iloc[0]].copy();g['rolling7']=g.units_demanded.rolling(7,min_periods=1).mean();ax=g.plot(x='date',y=['units_demanded','rolling7'],figsize=(10,4),title='SKU Demand and Rolling Average (synthetic)');ax.set_ylabel('Units');plt.xticks(rotation=45);plt.tight_layout();plt.savefig(p/'figures/demand_forecast.png');plt.close()
with sqlite3.connect(p/'outputs/inventory.db') as con:d.to_sql('inventory_daily',con,if_exists='replace',index=False)
print('SKUs flagged:',replen.reorder_flag.sum(),'Mean MAE:',ev[['naive_MAE','rolling7_MAE']].mean().to_dict())
