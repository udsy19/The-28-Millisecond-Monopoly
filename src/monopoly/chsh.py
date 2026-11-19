"""CHSH game: exact local enumeration, quantum bound and finite-sample tails.

Each trial has independent uniformly random settings x and y. Local strategies
may share arbitrary pre-agreed randomness, but cannot communicate after inputs.
"""
from __future__ import annotations

from itertools import product
from math import comb, cos, fsum, pi


SETTINGS = tuple(product((0, 1), repeat=2))


def wins(x: int, y: int, a: int, b: int) -> bool:
    return (a ^ b) == (x & y)


def local_strategies() -> list[dict]:
    results = []
    for a0, a1, b0, b1 in product((0, 1), repeat=4):
        table = (a0, a1, b0, b1)
        outcomes = [wins(x, y, table[x], table[2 + y]) for x, y in SETTINGS]
        results.append({"outputs": list(table), "wins": list(outcomes), "win_rate": sum(outcomes) / 4})
    return results


def optimal_local_win_rate(weights: tuple[float, float, float, float] | None = None) -> float:
    """Proof by exhaustive enumeration; weights correspond to (00,01,10,11)."""
    weights = weights or (0.25, 0.25, 0.25, 0.25)
    if len(weights) != 4 or any(x < 0 for x in weights) or abs(sum(weights)-1) > 1e-9:
        raise ValueError("Expected four nonnegative input probabilities summing to one.")
    return max(sum(w * ok for w, ok in zip(weights, s["wins"])) for s in local_strategies())


def quantum_tsirelson_win_rate() -> float:
    """Optimal quantum CHSH win probability for ideal maximally entangled qubits."""
    return cos(pi / 8) ** 2


def one_sided_binomial_tail(n: int, observed_wins: int, null_rate: float = 0.75) -> float:
    """P(X >= observed_wins), valid for independent, pre-specified unbiased input trials.

    Also bounds adapted local strategies with conditional success <=null_rate when
    complete, independently chosen rounds are scored. Not valid for post-selection.
    """
    if n < 0 or not 0 <= observed_wins <= n or not 0 <= null_rate <= 1:
        raise ValueError("Invalid tail parameters.")
    if null_rate == 0:
        return 1.0 if observed_wins == 0 else 0.0
    if null_rate == 1:
        return 1.0
    return fsum(comb(n, k) * null_rate**k * (1-null_rate)**(n-k) for k in range(observed_wins, n+1))


def optimal_one_bit_strategy(x: int, y: int) -> tuple[int, int]:
    """After Alice sends x to Bob (and Bob receives it), win with certainty."""
    return 0, x & y
