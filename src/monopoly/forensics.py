"""A local hidden-variable detection-loophole counterexample.

For any given fraction q of rounds we select a deterministic classical strategy:
  outputs a=b=0 -> wins on 00,01,10, loses on 11.
  On selected rounds Alice reports no click when x=1; Bob always reports.
No information is exchanged after the settings. Conditioning on coincidences
biases the recorded sample; it does not violate Bell on complete trials.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from random import Random


def conditional_win_rate(q: float) -> float:
    if not 0 <= q <= 1:
        raise ValueError("q must be in [0, 1]")
    return (0.75 - 0.25*q) / (1 - 0.5*q)


def retained_fraction(q: float) -> float:
    if not 0 <= q <= 1:
        raise ValueError("q must be in [0, 1]")
    return 1 - q/2


def required_filter_fraction(target_rate: float) -> float:
    if not 0.75 <= target_rate <= 1:
        raise ValueError("This construction can target only [0.75, 1].")
    return (target_rate - 0.75) / (0.5*target_rate - 0.25)


@dataclass(frozen=True)
class AuditResult:
    rounds_issued: int
    retained: int
    reported_wins: int
    true_unconditional_wins: int
    observed_win_rate: float
    unconditional_win_rate: float
    retention_rate: float
    filter_fraction: float
    seed: int

    def to_dict(self) -> dict:
        return asdict(self)


def simulate(rounds: int = 100_000, filter_fraction: float = 0.4375,
             seed: int = 20261119) -> AuditResult:
    if rounds <= 0 or not 0 <= filter_fraction <= 1:
        raise ValueError("Invalid simulation settings.")
    rng = Random(seed)
    kept = 0
    observed_wins = 0
    full_wins = 0
    for _ in range(rounds):
        x = rng.randrange(2)
        y = rng.randrange(2)
        # Shared strategy and Alice's local input, never Bob's input.
        filter_this_round = rng.random() < filter_fraction
        record = not (filter_this_round and x == 1)
        win = not (x == 1 and y == 1)
        full_wins += win
        if record:
            kept += 1
            observed_wins += win
    return AuditResult(rounds, kept, observed_wins, full_wins,
                       observed_wins / kept if kept else float("nan"),
                       full_wins / rounds, kept / rounds, filter_fraction, seed)
