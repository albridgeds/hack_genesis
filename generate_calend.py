import math
import os

from functools import reduce
from random import choice, randint

import pandas as pd

from const import *
from use_model import get_prediction


def check_cell(calendar_df, sku, week, is_pair=False):
    if 1 not in list(calendar_df.loc[[week]][sku].values):
        tier = tier_map[sku]
        tier_row = calendar_df.loc[[week]][tier]
        if tier_row.values.sum() <= 2:  # Боремся с канибализмом среди товаров одного ценового сегмента
            prev_week = week - 2
            days_in_prev_weeks = calendar_df.loc[prev_week:week][sku].sum()

            next_week = week + 2
            days_in_next_weeks = calendar_df.loc[week:next_week][sku].sum()

            if days_in_prev_weeks < 2 and days_in_next_weeks < 2:  # Не запланировать промо продолжительностью более 2х недель
                if not is_pair:
                    pair = pairs_map.get(sku)
                    if pair:
                        is_able_to_set_pair = check_cell(calendar_df, pair, week, is_pair=True)
                        if is_able_to_set_pair:
                            calendar_df.at[week, pair] = 1
                        return is_able_to_set_pair
                else:
                    return True

                if sku in tier_3_4:  # Дешевые и супер-дешевые в сопутствующие товары
                    rand_pair_sku = choice(tier_1_2)
                    is_able_to_set_pair = check_cell(calendar_df, rand_pair_sku, week, is_pair=True)

                    if is_able_to_set_pair:
                        calendar_df.at[week, rand_pair_sku] = 1
                    return is_able_to_set_pair
    return False


def generate_calendar(promo_weeks):
    weeks = list(range(WEEK_START, WEEKS))
    data = {x: [0] * len(weeks) for x in skus}
    data['weeks'] = weeks
    calendar_df = pd.DataFrame(data).set_index('weeks')

    saturartion = 0

    generated_pairs = set()
    while True:
        rand_sku = choice(skus)
        rand_week = randint(WEEK_START, WEEKS - 1)

        if (rand_sku, rand_week) in generated_pairs:
            saturartion += 1
            if saturartion == 10000:
                break
            continue
        generated_pairs.add((rand_sku, rand_week))

        is_able_to_set_cell = check_cell(calendar_df, rand_sku, rand_week)
        if is_able_to_set_cell:
            calendar_df.at[rand_week, rand_sku] = 1

        sum_df  = calendar_df.sum()
        if sum_df.sum() > promo_weeks:
            zero_values = sum_df[sum_df <= 2]
            for sku, _ in zero_values.iteritems():
                calendar_df.at[rand_week, sku] = 1

            break
    
    return calendar_df
