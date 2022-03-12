# Hack.Genesis
"MAD Team" decision for Accenture task: create promos plan (dates and discount values in percents for each good) using historical sales and promos data


accenture.ipynb - data analisys and model training

Application:
- main.py
- generate_calend.py - generates random promo configurations
- use_lgbm.py - calculates sales forecast for chosen promo configuration
- const.py - all the constants
- "data" folder:
  - mean_sales_roll.csv - rolled sales data being grouped by weeks and goods 
  - lgb_booster - trained model
  - %calendar.xlsx - the best found promo configuration (discount values are given in percents)
  - %prediction.xlsx - sales forecast by goods accounting the impact of best found promo configuration
