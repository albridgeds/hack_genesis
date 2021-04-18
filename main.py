import math
import os

import numpy as np
import pandas as pd

from const  import DATA_DIR, MC_ITERATIONS
from generate_calend import generate_calendar
#from use_model import get_prediction
from use_lgbm import get_prediction

prices = pd.read_csv(os.path.join(DATA_DIR, 'prices.csv'))
prices = prices[~prices.isin([np.nan, np.inf, -np.inf]).any(1)]
prices = prices.drop('sale_dt', axis=1).mean().to_dict()

final_results = {}

for w in [20,30, 40]:
    for i in range(3):
        data = generate_calendar(w)
        prediction = get_prediction(data)
        print(prediction.head(1))
        result = prediction * data

        # disc = budget / (price * prom sales)

        budget = 10000000
        budget_sku = budget / 10

        is_inconsisten_discount = False
        for col in result:
            summ = result[col].sum()
            promo_weeks = len(result[result[col] != 0])
            result[f'{col}_budget_%'] = 100  * (budget_sku / promo_weeks) / (prices[str(col)] * (result[col]))

            if not result[(result[f'{col}_budget_%'] < 5) & (result[f'{col}_budget_%'] > 40)].empty:
                is_inconsisten_discount = True
                break

        if is_inconsisten_discount:
            continue

        columns = [col for col in result.columns if '%' in str(col)]

        final_results[i * w] = {
            'prediction': prediction.sum().sum(),
            'prediction_df': prediction,
            'df': result[columns],
            'calend': data,
            'i * w': i * w,
            'w': w
        }

d = []
for x in final_results.values():
    d.append({'num': x['i * w'], 'pred': x['prediction']})

df = pd.DataFrame(d)
p_max = df['pred'].max()
num = df[df['pred'] == p_max]['num'].values[0]
final_results[num]['calend'].to_excel(f'{DATA_DIR}/optim_calendar.xlsx')
final_results[num]['df'].to_excel(f'{DATA_DIR}/%calendar.xlsx')
final_results[num]['prediction_df'].to_excel(f'{DATA_DIR}/%prediction.xlsx')