# Hack.Genesis
"MAD Team" desicion for Accenture task

accenture.ipynb - data analisys and model training

Application:
- main.py
- generate_calend.py - generates promo configurations (dates and discount values in percents)
- use_lgbm.py - calculates sales forecast for chosen promo configuration
- const.py - all the constants
- "data" folder:
  - mean_sales_roll.csv - rolled sales data being grouped by weeks and goods 
  - lgb_booster - trained model
  - %calendar.xlsx - the best found promo configuration (discount values are given in percents)
  - %prediction.xlsx - sales forecast by goods accounting the impact of best found promo configuration
