import math
import os

import numpy as np
import pandas as pd

from const  import DATA_DIR, MC_ITERATIONS
from generate_calend import generate_calendar
from use_model import get_prediction

prices =  pd.read_csv(os.path.join(DATA_DIR, 'prices.csv'))
prices = prices[~prices.isin([np.nan, np.inf, -np.inf]).any(1)]
perc = pd.DataFrame(prices.drop('sale_dt', axis=1).mean())
perc['%'] = perc[0].apply(lambda x: x / perc[0].sum())
perc = perc['%'].to_dict()
prices = prices.drop('sale_dt', axis=1).mean().to_dict()


def round_5_perc(perc):
    return round(perc * 100 / 5) * 5 / 100


def run(budget):
    final_results = {}

    for w in [20, 30, 40]:
        for i in range(MC_ITERATIONS):
            data = generate_calendar(w)
            prediction = get_prediction(data)
            result = prediction * data
            print('predict', i)

            budget_sku = budget / 10
            # disc = budget / (price * prom sales)

            is_inconsisten_discount = False
            for col in result:
                summ = result[col].sum()
                promo_weeks = len(result[result[col] != 0])
                result[f'{col}_budget_%'] = round_5_perc(100  * (budget_sku / promo_weeks) / (prices[str(col)] * (result[col])))
                result[f'{col}_budget_%'] = result[f'{col}_budget_%'].replace(np.inf, 0)

                filtered = result[result[f'{col}_budget_%'] > 0]
                if not filtered[(filtered[f'{col}_budget_%'] < 5) | (filtered[f'{col}_budget_%'] > 40)][f'{col}_budget_%'].empty:
                    top = filtered[(filtered[f'{col}_budget_%'] > 40)]
                    if not top.empty:
                        for v in list(top[f'{col}_budget_%']):
                            result[f'{col}_budget_%'] = result[f'{col}_budget_%'].replace(v, 40)

                    less = filtered[(filtered[f'{col}_budget_%'] < 5)]
                    if not less.empty:
                        for v in list(less[f'{col}_budget_%']):
                            result[f'{col}_budget_%'] = result[f'{col}_budget_%'].replace(v, 5)

            columns = [col for col in result.columns if '%' in str(col)]

            final_results[i * w] = {
                'prediction_df': prediction,
                'prediction': prediction.sum().sum(),
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
    final_results[num]['prediction_df'].to_excel(f'{DATA_DIR}/%prediction_df.xlsx')

if __name__ == '__main__':
    run(70000000000)
