"""Typed, immutable interpretation of the fictional case file."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class Case:
    valuation_pre_money_usd: float = 25_000_000
    investment_sought_usd: float = 3_000_000
    quantum_win_rate: float = 0.82
    startup_classical_win_rate: float = 0.74
    trials_per_protocol: int = 1000
    success_payout_usd: float = 100.0
    failure_payout_usd: float = -100.0
    quantum_operating_cost_per_round_usd: float = 0.08
    classical_operating_cost_per_round_usd: float = 0.001
    claimed_annual_opportunity_usd: float = 50_000_000
    demonstration_link_km: float = 40.0
    reported_pair_rate_hz: float = 1000.0

    @classmethod
    def from_json(cls, path: str | Path) -> "Case":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(**{name: data[name] for name in cls.__dataclass_fields__ if name in data})

    def __post_init__(self) -> None:
        for p in (self.quantum_win_rate, self.startup_classical_win_rate):
            if not 0 <= p <= 1:
                raise ValueError("Success probabilities must be in [0,1].")
        if self.trials_per_protocol < 1:
            raise ValueError("Trials must be positive.")
        if self.reported_pair_rate_hz < 0:
            raise ValueError("Pair rate must be non-negative.")


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CASE_PATH = REPOSITORY_ROOT / "data" / "case.json"
