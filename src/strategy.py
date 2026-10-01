from dataclasses import dataclass
from typing import Literal

OptionType = Literal["CE", "PE"]

@dataclass(frozen=True)
class RatioStrategy:
    name: str
    option_type: OptionType
    long_offset: int = 4
    short1_offset: int = 5
    short2_offset: int = 6

    def validate(self) -> None:
        if sorted((self.long_offset, self.short1_offset, self.short2_offset)) != [4, 5, 6]:
            raise ValueError("This test is frozen to OTM4/OTM5/OTM6.")
        if self.option_type not in ("CE", "PE"):
            raise ValueError("option_type must be CE or PE.")

    def signed_legs(self, atm: float, strikes: list[float]) -> list[tuple[float, int]]:
        self.validate()
        if self.option_type == "CE":
            otm = sorted([s for s in strikes if s > atm])
        else:
            otm = sorted([s for s in strikes if s < atm], reverse=True)
        if len(otm) < 6:
            raise ValueError("Fewer than six OTM strikes are available.")
        k4, k5, k6 = otm[3], otm[4], otm[5]
        return [(k4, +1), (k5, -1), (k6, -1)]

    @staticmethod
    def entry_cashflow(entry_prices: dict[float, float], legs: list[tuple[float, int]]) -> float:
        return sum(sign * entry_prices[strike] for strike, sign in legs)

    @staticmethod
    def strike_spacing(legs: list[tuple[float, int]]) -> float:
        strikes = sorted(k for k, _ in legs)
        if len(strikes) != 3:
            raise ValueError("Expected three strikes.")
        d1 = strikes[1] - strikes[0]
        d2 = strikes[2] - strikes[1]
        if abs(d1 - d2) > 1e-9:
            raise ValueError("Maximum-profit formula requires equal strike spacing.")
        return d1

    @staticmethod
    def flatline_points(entry_prices: dict[float, float], legs: list[tuple[float, int]]) -> float:
        return -RatioStrategy.entry_cashflow(entry_prices, legs)

    def max_profit_points(self, entry_prices: dict[float, float], legs: list[tuple[float, int]]) -> float:
        return self.strike_spacing(legs) - self.entry_cashflow(entry_prices, legs)

    def target_points(self, entry_prices: dict[float, float], legs: list[tuple[float, int]], fraction: float) -> float:
        if not (0 < fraction <= 1):
            raise ValueError("fraction must be in (0, 1].")
        return fraction * self.max_profit_points(entry_prices, legs)


STRATEGY_1 = RatioStrategy("strategy_1_put_ratio", "PE")
STRATEGY_2 = RatioStrategy("strategy_2_call_ratio", "CE")


def expiry_intrinsic(strategy: RatioStrategy, spot: float, legs: list[tuple[float, int]]) -> float:
    total = 0.0
    for strike, sign in legs:
        intrinsic = max(spot - strike, 0.0) if strategy.option_type == "CE" else max(strike - spot, 0.0)
        total += sign * intrinsic
    return total
