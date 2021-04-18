import os


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_PATH, 'data')


CALENDAR_ITERATIONS = 32
MC_ITERATIONS = 100
WEEK_START = 1
WEEKS = 27


skus = [
    7182, 7194, 7232, 7234,  # TIER 1 | 0, 1, 2, 3
    7238, 7193,              # TIER 2 | 4, 5
    7189, 7205,              # TIER 3 | 6, 7
    7236,                    # TIER 4 | 8, 9
    # NO PROMOS 
    7247                     # TIER 4                     
]

tier_1 = set([7182, 7194, 7232, 7234])
tier_2 = set([7238, 7193])
tier_3 = set([7189, 7205])
tier_4 = set([7236, 7247])

tier_1_2 = list(tier_1.union(tier_2))
tier_3_4 = tier_3.union(tier_4)


tier_map = {}
for tiers in (tier_1, tier_2, tier_3, tier_4):
    for tier in tiers:
        tier_map[tier] = tiers - {tier}

tier_map = {
    sku: tier 
    for tier in (tier_1, tier_2, tier_3, tier_4)
    for sku in tier 
}

pairs_map = {
    7194: 7189,
    7189: 7194,
    7234: 7205,
    7205: 7234
}
