"""A physics/engineering feasibility map, deliberately not a market forecast."""
from __future__ import annotations

from .lightcone import classical_status
from .photonics import upper_bound_received_pair_rate


DISTANCES_KM = (40, 100, 160, 320, 640, 1200, 2400, 4000, 5600)
DEADLINES_MS = (0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 15, 20, 25, 30, 40)


def classify(distance_km: float, deadline_ms: float,
             assumed_source_pair_rate_hz: float = 1000.0,
             minimum_pair_rate_hz: float = 1.0,
             route_multiplier: float = 1.08) -> dict:
    status = classical_status(distance_km, deadline_ms, route_multiplier)
    rate = upper_bound_received_pair_rate(assumed_source_pair_rate_hz, distance_km)
    if status == "one_bit_available":
        region = "classical_one_bit_suffices"
    elif rate < minimum_pair_rate_hz:
        region = "no_direct_fibre_supply"
    elif status == "route_dependent":
        region = "depends_on_fastest_classical_route"
    else:
        region = "conditional_physics_candidate"
    return {"distance_km": distance_km, "deadline_ms": deadline_ms,
            "classical_status": status, "ideal_direct_fibre_pairs_hz": rate,
            "illustrative_rate_threshold_hz": minimum_pair_rate_hz,
            "region": region, "commercial_viability_verified": False}


def grid(distances=DISTANCES_KM, deadlines=DEADLINES_MS) -> list[dict]:
    return [classify(d, t) for t in deadlines for d in distances]
