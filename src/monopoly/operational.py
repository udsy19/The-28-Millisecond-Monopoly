"""Best-case commercial throughput bounds for a pre-distributed CHSH resource.

This is *not* a trading forecast. A delivered optical pair is not necessarily
a valid, fresh, heralded, stored and executable CHSH resource. We deliberately
give the startup every benefit of the doubt, so any failed upper bound is a
stronger negative result than a failed nominal estimate.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import csv
import json
import math
from pathlib import Path

from .config import Case
from .economics import comparison
from .lightcone import classical_status
from .photonics import upper_bound_received_pair_rate, source_rate_from_observed_at_distance


@dataclass(frozen=True)
class OperatingScenario:
    name: str
    distance_km: float
    deadline_ms: float
    source_pair_rate_hz: float
    annual_demand_rounds: float = 4_000_000
    operating_seconds_per_year: float = 31_536_000
    usable_pair_fraction: float = 1.0
    incremental_non_case_cost_per_round_usd: float = 0.0
    fixed_annual_cost_usd: float = 0.0
    attenuation_db_per_km: float = 0.2
    route_multiplier: float = 1.08
    fibre_refractive_index: float = 1.468

    def __post_init__(self) -> None:
        for key in (
            "distance_km", "deadline_ms", "source_pair_rate_hz",
            "annual_demand_rounds", "operating_seconds_per_year",
            "incremental_non_case_cost_per_round_usd", "fixed_annual_cost_usd",
            "attenuation_db_per_km",
        ):
            if getattr(self, key) < 0 or not math.isfinite(getattr(self, key)):
                raise ValueError(f"{key} must be finite and nonnegative")
        if not 0 <= self.usable_pair_fraction <= 1:
            raise ValueError("usable_pair_fraction must be in [0, 1]")
        if not math.isfinite(self.usable_pair_fraction):
            raise ValueError("usable_pair_fraction must be finite")
        if self.route_multiplier < 1 or not math.isfinite(self.route_multiplier):
            raise ValueError("route_multiplier must be finite and >= 1")
        if self.fibre_refractive_index < 1 or not math.isfinite(self.fibre_refractive_index):
            raise ValueError("fibre_refractive_index must be finite and >= 1")


def annual_ceiling(scenario: OperatingScenario, case: Case = Case()) -> dict:
    """Optimistic incremental ceiling over the exact best no-message CHSH policy.

    Missing pairs revert to the optimal *classical* policy, not zero-valued
    trades. This is an upper bound assuming each surviving pair is consumable
    once with the claimed quantum win-rate and exact fictional payoff.
    """
    edge = comparison(case)["incremental_usd_per_round"]
    rate = upper_bound_received_pair_rate(
        scenario.source_pair_rate_hz, scenario.distance_km,
        scenario.attenuation_db_per_km
    )
    supply = rate * scenario.operating_seconds_per_year * scenario.usable_pair_fraction
    served = min(supply, scenario.annual_demand_rounds)
    before_fixed = served * (edge - scenario.incremental_non_case_cost_per_round_usd)
    after_fixed = before_fixed - scenario.fixed_annual_cost_usd
    status = classical_status(
        scenario.distance_km, scenario.deadline_ms,
        scenario.route_multiplier, scenario.fibre_refractive_index
    )
    # One-bit classical messaging wins *every* CHSH round when it arrives.
    # In the route-dependent regime, a faster feasible route may remove the edge.
    incremental_when_fibre_model_applies = (
        max(0.0, after_fixed) if status != "one_bit_available" else 0.0
    )
    return {
        **asdict(scenario),
        "source_rate_interpretation": "scenario_assumption_not_a_measured_transatlantic_pair_rate",
        "ideal_direct_fibre_pair_rate_hz": rate,
        "ideal_direct_fibre_annual_pairs": supply,
        "eligible_round_ceiling": served,
        "best_classical_counterfactual": "optimal_local_uniform_chsh_with_fallback",
        "classical_message_status": status,
        "fictional_incremental_per_served_round_usd": edge,
        "incremental_game_value_before_fixed_cost_usd": before_fixed,
        "incremental_game_value_after_fixed_cost_usd": after_fixed,
        "nonnegative_conditional_value_ceiling_usd": incremental_when_fibre_model_applies,
        "is_a_market_forecast": False,
        "is_proof_of_usable_entanglement": False,
        "commercial_viability_verified": False,
        "economic_premium_unverified_if_route_dependent": status == "route_dependent",
    }


def min_emitted_rate_for_target(
    distance_km: float, annual_target_usd: float, incremental_usd_per_round: float,
    annual_seconds: float = 31_536_000, usable_fraction: float = 1.0,
    attenuation_db_per_km: float = 0.2
) -> float | None:
    """Required emitter pairs/s for the fictional incremental target, no capex.

    Return None when even one perfect emitted pair could not produce a positive
    payoff, or when usable time/fraction is zero. Repeater/satellite designs
    cannot be evaluated with this direct-fibre equation.
    """
    if any(not math.isfinite(v) or v < 0 for v in (
        distance_km, annual_target_usd, annual_seconds, usable_fraction,
        attenuation_db_per_km
    )) or usable_fraction > 1:
        raise ValueError("Invalid nonnegative rate-budget inputs")
    if annual_target_usd == 0:
        return 0.0
    if incremental_usd_per_round <= 0 or annual_seconds <= 0 or usable_fraction <= 0:
        return None
    log10_rate = (
        math.log10(annual_target_usd / (incremental_usd_per_round * annual_seconds * usable_fraction))
        + attenuation_db_per_km * distance_km / 10
    )
    return 10 ** log10_rate if log10_rate < 308 else math.inf


def max_direct_distance_for_target(
    source_rate_hz: float, annual_target_usd: float, incremental_usd_per_round: float,
    annual_seconds: float = 31_536_000, usable_fraction: float = 1.0,
    attenuation_db_per_km: float = 0.2
) -> float | None:
    """Optimistic optical-only distance cap in km, not a causal or trading cap."""
    if source_rate_hz < 0 or not math.isfinite(source_rate_hz):
        raise ValueError("source_rate_hz must be finite and nonnegative")
    if any(not math.isfinite(v) or v < 0 for v in (
        annual_target_usd, annual_seconds, usable_fraction, attenuation_db_per_km
    )) or usable_fraction > 1:
        raise ValueError("Invalid target/availability inputs")
    if annual_target_usd == 0:
        return math.inf
    if incremental_usd_per_round <= 0 or annual_seconds == 0 or usable_fraction == 0:
        return None
    required_received_rate = annual_target_usd / (
        incremental_usd_per_round * annual_seconds * usable_fraction
    )
    if source_rate_hz < required_received_rate:
        return None
    if attenuation_db_per_km == 0:
        return math.inf
    return 10 / attenuation_db_per_km * math.log10(source_rate_hz / required_received_rate)


def build_operational_appendix(
    output_dir: str | Path,
    case: Case = Case(),
    assumptions: dict | None = None
) -> dict:
    """Write machine-readable underwriting, scenario CSV and narrative appendix."""
    a = assumptions or {}
    alpha = float(a.get("fibre_attenuation_db_per_km", 0.2))
    source_rate = float(a.get("source_pair_rate_hz_for_illustration", 1000.0))
    demand = float(a.get("assumed_business_rounds_per_year", 4_000_000))
    seconds = float(a.get("annual_seconds_assumed", 31_536_000))
    n = float(a.get("fibre_refractive_index", 1.468))
    recovered_source = source_rate_from_observed_at_distance(
        case.reported_pair_rate_hz, case.demonstration_link_km, alpha
    )
    scenarios = [
        OperatingScenario("metro_40km_assumed_emitted", 40, 0.1, source_rate,
                          demand, seconds, attenuation_db_per_km=alpha, fibre_refractive_index=n),
        OperatingScenario("regional_160km_assumed_emitted", 160, 0.5, source_rate,
                          demand, seconds, attenuation_db_per_km=alpha, fibre_refractive_index=n),
        OperatingScenario("regional_200km_assumed_emitted", 200, 0.5, source_rate,
                          demand, seconds, attenuation_db_per_km=alpha, fibre_refractive_index=n),
        OperatingScenario("atlantic_5600km_assumed_emitted", 5600, 20, source_rate,
                          demand, seconds, attenuation_db_per_km=alpha, fibre_refractive_index=n),
        OperatingScenario("atlantic_5600km_if_1000_received_at_40km", 5600, 20, recovered_source,
                          demand, seconds, attenuation_db_per_km=alpha, fibre_refractive_index=n),
    ]
    rows = [annual_ceiling(s, case) for s in scenarios]
    edge = comparison(case)["incremental_usd_per_round"]
    annual_target = case.claimed_annual_opportunity_usd
    cap_distance = max_direct_distance_for_target(
        source_rate, annual_target, edge, seconds, attenuation_db_per_km=alpha
    )
    required_atlantic_source = min_emitted_rate_for_target(
        5600, annual_target, edge, seconds, attenuation_db_per_km=alpha
    )
    summary = {
        "assumed_annual_seconds": seconds,
        "assumed_annual_customer_rounds": demand,
        "target_incremental_fictional_game_usd": annual_target,
        "minimum_annual_eligible_rounds_for_target": math.ceil(annual_target / edge) if edge > 0 else None,
        "optimistic_direct_fibre_distance_cap_km_if_source_1000_per_s": cap_distance,
        "source_rate_required_at_5600km_for_target_pairs_hz": required_atlantic_source,
        "modes": [
            "hypothetical_source_rate_1000_per_second",
            "hypothetical_40km_received_pair_rate_back_extrapolation",
        ],
        "scenarios": rows,
        "scientific_constraints": {
            "uniform_independent_CHSH_inputs_only": True,
            "not_a_market_forecast": True,
            "not_a_real_transatlantic_entanglement_service": True,
            "long_distance_repeater_satellite_memory_not_modelled": True,
            "source_vs_received_case_claim_is_ambiguous": True,
            "best_possible_classical_fallback_on_unserved_rounds": True,
            "no_proven_monetizable_real_world_CHSH_rounds": True,
        },
    }
    out = Path(output_dir)
    (out / "tables").mkdir(parents=True, exist_ok=True)
    (out / "underwriting.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    with (out / "tables" / "operational_scenarios.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    distance_label = f"{cap_distance:,.1f}" if cap_distance is not None else "not possible"
    (out / "OPERATIONS_APPENDIX.md").write_text(
        "# The strongest operational counterfactual\n\n"
        "This upper-bound exercise **gives the fictional startup perfect detectors, perfect fidelity, "
        "perfect utilization, no repeater costs, and no additional infrastructure costs**. "
        "It does NOT prove that any optical arrival is a usable Bell pair.\n\n"
        f"- Target: ${annual_target:,.0f} of incremental *fictional referee-game* benefit.\n"
        f"- Implied rounds: {summary['minimum_annual_eligible_rounds_for_target']:,} per year.\n"
        f"- Assumed emitted pairs: {source_rate:,.0f}/s, all {seconds:,.0f} seconds/year.\n"
        f"- Maximum unrepeated optical length supporting that target under these idealizations: **{distance_label} km**.\n"
        f"- Source rate that the same optimistic direct-fibre model would require at 5,600 km: "
        f"**{required_atlantic_source:.3e} pairs/s**. This is a sensitivity calculation, not a proposed design.\n\n"
        "The shorter-path scenarios can fit within an optical supply budget, but shorter paths "
        "also make rapid classical messaging easier. The route-dependent regime must be "
        "checked against the *fastest feasible* alternative, not only assumed fibre.\n\n"
        "A credible founder rebuttal is to pre-distribute and store pairs, or use repeaters "
        "or satellites. Those architectures require separately evidenced entanglement fidelity, "
        "heralding, memory lifetime, usable pair inventory and lifecycle cost. "
        "They are **not** excluded by the simple fibre calculation.\n\n"
        "No annual market volume, CHSH-shaped customer contract, fixed cost, or customer willingness "
        "to pay has been established. Do not label these numbers trading P&L.\n",
        encoding="utf-8",
    )
    return summary
