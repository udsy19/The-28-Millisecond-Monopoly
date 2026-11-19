"""Fibre link budget. No repeaters and no hardware guarantees are assumed."""
from __future__ import annotations


def attenuation_db(distance_km: float, alpha_db_per_km: float = 0.2) -> float:
    if distance_km < 0 or alpha_db_per_km < 0:
        raise ValueError("Distance and attenuation must be non-negative")
    return distance_km * alpha_db_per_km


def transmission_probability(distance_km: float, alpha_db_per_km: float = 0.2) -> float:
    return 10 ** (-attenuation_db(distance_km, alpha_db_per_km) / 10)


def upper_bound_received_pair_rate(source_rate_hz: float, distance_km: float,
                                   alpha_db_per_km: float = 0.2) -> float:
    """Idealized joint transmission across total path length.

    Assumes no detector loss and no additional coupler/dark-count/fidelity cost.
    1,000/s in the fictional case has unspecified measurement point; caller
    MUST label whether this is an assumed source rate or 40km observed rate.
    """
    if source_rate_hz < 0:
        raise ValueError("Source rate cannot be negative")
    return source_rate_hz * transmission_probability(distance_km, alpha_db_per_km)


def source_rate_from_observed_at_distance(observed_rate_hz: float,
                                          observation_km: float,
                                          alpha_db_per_km: float = 0.2) -> float:
    t = transmission_probability(observation_km, alpha_db_per_km)
    if t == 0:
        raise ValueError("Cannot infer source rate when transmission underflows")
    return observed_rate_hz / t


def arrival_probability_in_window(rate_hz: float, window_seconds: float) -> float:
    """Poisson at-least-one event; not proof of useable entanglement."""
    from math import exp
    if rate_hz < 0 or window_seconds < 0:
        raise ValueError("Rate/window cannot be negative")
    return -__import__("math").expm1(-rate_hz * window_seconds)
