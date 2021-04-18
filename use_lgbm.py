import os

import lightgbm as lgb
import pandas as pd

from const import DATA_DIR

# загружаем модель из файла
model = lgb.Booster(model_file=os.path.join(DATA_DIR, 'lgb_booster'))
#model = lgb.Booster(model_file='lgb_booster')

# загружаем усредненные значения
mean_sales_roll = pd.read_csv(os.path.join(DATA_DIR, 'mean_sales_roll.csv'), index_col='week')
#print(mean_sales_roll)

def get_prediction(ext_data):
    ext_data = ext_data.reset_index().rename(columns={'weeks': 'index'}).set_index('index')
    sku_cols = ext_data.columns

    ext_data = ext_data[[7182,7189,7193,7194,7205,7232,7234,7236,7238,7247]]
    ext_data.columns = ['promo_'+str(x) for x in ext_data.columns]
    ext_data.reset_index(inplace=True)

    # добавляем фичей
    for i in ext_data.index:
        row = ext_data.loc[i]
        ext_data.drop(i, inplace=True)
        for sku in mean_sales_roll.columns:
            row['sku'] = int(sku)
            row['season'] = mean_sales_roll.loc[row['index'],sku]
            ext_data = ext_data.append(row)
    ext_data.reset_index(drop=True, inplace=True)
    #print(ext_data)

    # ohe-кодирование
    num_cols = ['season']
    X = ext_data.drop(['index'], axis=1)
    '''X_ohe = pd.get_dummies(X, columns=['sku'], drop_first=True)
    print(X_ohe.columns)'''

    # прогноз
    pred = model.predict(X)
    pred_df = pd.DataFrame(data={'pred': pred})
    pred_df['sku'] = ext_data['sku'].astype('int')
    pred_df['weeks'] = ext_data['index'].astype('int')
    #print(pred_df)
    pred_table = pred_df.pivot_table(index='weeks', columns='sku')
    return pd.DataFrame(pred_table.to_records()).rename(columns={'week': 'weeks'}).set_index('weeks').rename(columns=lambda x: int(x.split(', ')[1].replace('\'', '').replace(')', '')))
