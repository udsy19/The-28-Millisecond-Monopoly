"""Causal communication bounds: do not confuse quantum correlations with signalling."""
from __future__ import annotations

import math

C_KM_PER_S = 299_792.458


def great_circle_km(lat1: float = 40.7128, lon1: float = -74.0060,
                    lat2: float = 51.5074, lon2: float = -0.1278) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1) * math.cos(p2) * math.sin(dl/2)**2
    return 6371.0088 * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def vacuum_min_ms(distance_km: float) -> float:
    if distance_km < 0:
        raise ValueError("Distance cannot be negative")
    return distance_km / C_KM_PER_S * 1000


def ideal_fibre_ms(distance_km: float, refractive_index: float = 1.468) -> float:
    if refractive_index < 1:
        raise ValueError("Fibre refractive index must be >=1")
    return vacuum_min_ms(distance_km) * refractive_index


def classical_status(distance_km: float, deadline_ms: float,
                     route_multiplier: float = 1.08,
                     refractive_index: float = 1.468) -> str:
    """Three-state classification avoids treating an assumed route as physical law.

    impossible: below vacuum straight-line limit.
    conditional: possible in principle but not via the assumed fibre route.
    available: one bit arrives over the assumed route.
    """
    if deadline_ms < 0 or route_multiplier < 1:
        raise ValueError("Bad deadline or route multiplier")
    if deadline_ms < vacuum_min_ms(distance_km):
        return "classical_physically_excluded"
    if deadline_ms < ideal_fibre_ms(distance_km, refractive_index) * route_multiplier:
        return "route_dependent"
    return "one_bit_available"


def historical_one_way_equivalent_ms(round_trip_ms: float = 58.95) -> float:
    """Half an RTT benchmark, not a measured one-way latency."""
    return round_trip_ms / 2.0
