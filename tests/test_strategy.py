import math

from src.strategy import STRATEGY_1, STRATEGY_2


def test_put_ratio_has_positive_plateau():
    # ATM=100; OTM puts from nearest to farthest are 95,90,85,80,75,70.
    legs = STRATEGY_1.signed_legs(100, [70, 75, 80, 85, 90, 95, 100])
    prices = {80: 10.0, 75: 4.0, 70: 2.0}
    assert legs == [(80, 1), (75, -1), (70, -1)]
    assert math.isclose(STRATEGY_1.strike_spacing(legs), 5.0)
    assert math.isclose(STRATEGY_1.flatline_points(prices, legs), -4.0)
    assert math.isclose(STRATEGY_1.max_profit_points(prices, legs), 1.0)


def test_call_ratio_target():
    # ATM=100; OTM calls from nearest to farthest are 105,110,115,120,125,130.
    legs = STRATEGY_2.signed_legs(100, [105, 110, 115, 120, 125, 130])
    prices = {120: 2.0, 125: 1.0, 130: 0.4}
    assert legs == [(120, 1), (125, -1), (130, -1)]
    assert math.isclose(STRATEGY_2.max_profit_points(prices, legs), 4.4)
    assert math.isclose(STRATEGY_2.target_points(prices, legs, 0.95), 4.18)


def test_bump_height_is_strike_spacing():
    for strategy in (STRATEGY_1, STRATEGY_2):
        legs = [(90, 1), (95, -1), (100, -1)]
        prices = {90: 8.0, 95: 3.0, 100: 1.0}
        assert math.isclose(
            strategy.max_profit_points(prices, legs) - strategy.flatline_points(prices, legs),
            5.0,
        )
