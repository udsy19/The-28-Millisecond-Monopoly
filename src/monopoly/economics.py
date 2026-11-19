"""All payoffs are from the fictional referee game, not actual market trading."""
from __future__ import annotations

from math import ceil
from .config import Case
from .chsh import optimal_local_win_rate


def expected_net_usd(win_rate: float, win_pay: float = 100.0,
                     lose_pay: float = -100.0, operating_cost: float = 0.0) -> float:
    if not 0 <= win_rate <= 1:
        raise ValueError("Invalid win rate")
    return win_rate * win_pay + (1-win_rate) * lose_pay - operating_cost


def comparison(case: Case = Case()) -> dict:
    local_opt = optimal_local_win_rate()
    q = expected_net_usd(case.quantum_win_rate, case.success_payout_usd,
                         case.failure_payout_usd, case.quantum_operating_cost_per_round_usd)
    observed_classic = expected_net_usd(case.startup_classical_win_rate, case.success_payout_usd,
                                        case.failure_payout_usd, case.classical_operating_cost_per_round_usd)
    best_classic = expected_net_usd(local_opt, case.success_payout_usd,
                                    case.failure_payout_usd, case.classical_operating_cost_per_round_usd)
    edge = q - best_classic
    return {"quantum_net_usd": q, "startup_classical_net_usd": observed_classic,
            "optimal_classical_net_usd": best_classic,
            "incremental_usd_per_round": edge,
            "rounds_for_claimed_opportunity": ceil(case.claimed_annual_opportunity_usd / edge) if edge > 0 else None,
            "equity_post_money_fraction": case.investment_sought_usd /
            (case.valuation_pre_money_usd + case.investment_sought_usd),
            "not_real_trading_profit": True}


def independent_bit_probabilities(px: float, py: float) -> tuple[float, float, float, float]:
    if not 0 <= px <= 1 or not 0 <= py <= 1:
        raise ValueError("Invalid input odds")
    return ((1-px)*(1-py), (1-px)*py, px*(1-py), px*py)


def payoff_surgery(px: float, py: float, assumed_fixed_quantum_rate: float = 0.82,
                   quantum_cost: float = 0.08, classic_cost: float = 0.001) -> dict:
    """Assumes per-setting quantum win rate stays constant when odds change.

    Not a quantum-optimal bound and not derivable from an aggregate measured rate.
    """
    weights = independent_bit_probabilities(px, py)
    classical = optimal_local_win_rate(weights)
    q_net = expected_net_usd(assumed_fixed_quantum_rate, operating_cost=quantum_cost)
    c_net = expected_net_usd(classical, operating_cost=classic_cost)
    return {"px": px, "py": py, "weights": list(weights), "classical_opt": classical,
            "assumed_fixed_quantum_rate": assumed_fixed_quantum_rate,
            "incremental_usd_per_round": q_net - c_net,
            "is_hypothesis_not_observation": True}
