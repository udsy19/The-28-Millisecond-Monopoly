"""Pure functions for the CHSH-game investment analysis.

Every function here is deterministic given its inputs (Monte Carlo functions take an
explicit ``numpy.random.Generator``), so the notebook and the tests can call the same
code and a reviewer can re-run any number.

The game: a referee sends bit x to desk A and bit y to desk B. Each desk answers one
bit (a, b) without talking to the other. They win when ``a XOR b == x AND y``.
"""
from __future__ import annotations

import itertools
import math

import numpy as np

# ---------------------------------------------------------------------------
# Constants (all are modelling choices, recorded in DECISIONS.md / assumptions.md)
# ---------------------------------------------------------------------------
SPEED_OF_LIGHT_KM_S = 299_792.458   # vacuum; best case for a line-of-sight microwave link
FIBRE_LOSS_DB_PER_KM = 0.2          # standard telecom fibre at 1550 nm
EBERHARD_FLOOR = 2.0 / 3.0          # lowest efficiency any CHSH-type test can tolerate
IDEAL_QUANTUM_WIN = math.cos(math.pi / 8) ** 2   # Tsirelson bound, ~0.8536
CLASSICAL_MAX = 0.75

# Standard CHSH measurement angles (polarisation angles, radians).
ALICE_ANGLES = (0.0, math.pi / 4)
BOB_ANGLES = (math.pi / 8, -math.pi / 8)


def wins(x, y, a, b):
    """True where the round is won: a XOR b equals x AND y. Works on arrays."""
    return np.bitwise_xor(a, b) == np.bitwise_and(x, y)


# ---------------------------------------------------------------------------
# E1  Classical limit
# ---------------------------------------------------------------------------
def deterministic_strategies():
    """All 16 no-communication strategies.

    A strategy is (a0, a1, b0, b1): desk A answers a0 when x=0 and a1 when x=1, etc.
    Randomised strategies are mixtures of these, so they can never beat the best one.
    """
    return list(itertools.product((0, 1), repeat=4))


def strategy_win_rate(strategy, p=0.5):
    """Exact win probability of one deterministic strategy.

    ``p`` is the probability that each desk's input bit is 1 (0.5 in the standard game).
    """
    a0, a1, b0, b1 = strategy
    total = 0.0
    for x, y in itertools.product((0, 1), repeat=2):
        weight = (p if x else 1 - p) * (p if y else 1 - p)
        a = a1 if x else a0
        b = b1 if y else b0
        total += weight * float((a ^ b) == (x & y))
    return total


def classical_max(p=0.5):
    """Best win rate over all 16 deterministic strategies (brute force)."""
    return max(strategy_win_rate(s, p) for s in deterministic_strategies())


def one_bit_strategy_win_rate():
    """Win rate when A may send its bit x to B before answering.

    A answers 0; B, now knowing x and y, answers x AND y. Then a XOR b = x AND y always.
    We check all four input pairs rather than assert it.
    """
    results = []
    for x, y in itertools.product((0, 1), repeat=2):
        a = 0
        b = x & y          # B uses the bit it received from A
        results.append((a ^ b) == (x & y))
    return float(np.mean(results))


def z_score(p_hat, p0=CLASSICAL_MAX, n=1000):
    """Binomial z-score of an observed rate against a null rate p0 (null-hypothesis SE)."""
    se = math.sqrt(p0 * (1 - p0) / n)
    return (p_hat - p0) / se


def singlet_joint_probs(alpha, beta):
    """Born-rule joint outcome table P[a, b] for a polarisation singlet.

    State (|HV> - |VH>)/sqrt(2). Desk A measures along angle alpha, desk B along beta.
    Outcome 0 = photon passes the polariser, 1 = it is reflected. Desk B flips its bit
    afterwards (a fixed local relabelling) so that "same answer" means correlated.
    """
    H = np.array([1.0, 0.0])
    V = np.array([0.0, 1.0])
    psi = (np.kron(H, V) - np.kron(V, H)) / math.sqrt(2)

    def basis(theta):
        # outcome 0 along theta, outcome 1 along theta + 90 degrees
        return [np.array([math.cos(theta), math.sin(theta)]),
                np.array([-math.sin(theta), math.cos(theta)])]

    table = np.zeros((2, 2))
    for a, va in enumerate(basis(alpha)):
        for b_raw, vb in enumerate(basis(beta)):
            amp = np.kron(va, vb) @ psi
            table[a, 1 - b_raw] = amp ** 2       # B's relabelling: b = 1 - b_raw
    return table


def quantum_joint_table(visibility=1.0):
    """P[x, y, a, b] for the CHSH strategy on a (possibly noisy) singlet.

    ``visibility`` V mixes the singlet with white noise: with probability 1-V both
    desks get independent fair coin flips. This is how we model a source whose quality
    is below the ideal (e.g. the startup's 82%).
    """
    table = np.zeros((2, 2, 2, 2))
    for x, y in itertools.product((0, 1), repeat=2):
        ideal = singlet_joint_probs(ALICE_ANGLES[x], BOB_ANGLES[y])
        table[x, y] = visibility * ideal + (1 - visibility) * 0.25
    return table


def visibility_for_win(p_q):
    """Noise level V that gives win rate p_q when both photons arrive."""
    return (p_q - 0.5) / (IDEAL_QUANTUM_WIN - 0.5)


def exact_quantum_win(visibility=1.0):
    """Exact win rate of the CHSH strategy from the joint table (no sampling)."""
    t = quantum_joint_table(visibility)
    total = 0.0
    for x, y, a, b in itertools.product((0, 1), repeat=4):
        total += 0.25 * t[x, y, a, b] * float((a ^ b) == (x & y))
    return total


def sample_quantum_outcomes(x, y, rng, visibility=1.0):
    """Draw (a, b) for each round from the joint table, given input arrays x, y."""
    table = quantum_joint_table(visibility).reshape(2, 2, 4)   # 4 = (a,b) pairs
    cdf = np.cumsum(table, axis=-1)[x, y]                      # per-round CDF
    u = rng.random(len(x))[:, None]
    idx = (u > cdf).sum(axis=1)                                # inverse-CDF sampling
    idx = np.minimum(idx, 3)
    return idx // 2, idx % 2


def simulate_quantum(n, rng, visibility=1.0):
    """Monte Carlo win rate of the quantum strategy with perfect photon delivery."""
    x = rng.integers(0, 2, n)
    y = rng.integers(0, 2, n)
    a, b = sample_quantum_outcomes(x, y, rng, visibility)
    return float(wins(x, y, a, b).mean())


# ---------------------------------------------------------------------------
# E2  Missing-photon problem
# ---------------------------------------------------------------------------
def all_rounds_win(eta, p_q):
    """Win rate over ALL rounds when each desk gets its photon with probability eta.

    Both arrive (eta^2): quantum quality p_q.
    Exactly one arrives (2 eta (1-eta)): the lucky desk's answer is a fair coin and the
        other desk plays a fixed 0, so the round is a coin flip (0.5).
    Neither arrives ((1-eta)^2): both play 0, the best classical answer (0.75).
    """
    return eta**2 * p_q + 2 * eta * (1 - eta) * 0.5 + (1 - eta) ** 2 * CLASSICAL_MAX


def eta_threshold(p_q):
    """Efficiency at which all_rounds_win equals 0.75: eta* = 0.5 / (p_q - 0.25)."""
    return 0.5 / (p_q - 0.25)


def fibre_eta(d_km, loss_db_per_km=FIBRE_LOSS_DB_PER_KM, detector_eff=1.0):
    """Per-desk efficiency with the source at the midpoint (each arm is d/2 km)."""
    arm_loss_db = loss_db_per_km * d_km / 2
    return detector_eff * 10 ** (-arm_loss_db / 10)


def max_separation_km(eta_needed, loss_db_per_km=FIBRE_LOSS_DB_PER_KM, detector_eff=1.0):
    """Largest desk separation whose fibre efficiency still reaches eta_needed.

    Returns 0.0 if the detectors alone are already below the requirement.
    """
    if eta_needed >= detector_eff:
        return 0.0
    return -20.0 / loss_db_per_km * math.log10(eta_needed / detector_eff)


def simulate_lossy(n, eta, rng, visibility=1.0):
    """Monte Carlo that actually drops photons.

    Each desk independently receives its photon with probability eta. A desk that
    receives it answers with its measured bit; a desk that does not answers 0. Neither
    desk knows what happened at the other. Returns (all-rounds win, coincidence win,
    both-arrived share).
    """
    x = rng.integers(0, 2, n)
    y = rng.integers(0, 2, n)
    a_q, b_q = sample_quantum_outcomes(x, y, rng, visibility)
    got_a = rng.random(n) < eta
    got_b = rng.random(n) < eta
    a = np.where(got_a, a_q, 0)       # fallback: fixed classical answer 0
    b = np.where(got_b, b_q, 0)
    w = wins(x, y, a, b)
    both = got_a & got_b
    return float(w.mean()), float(w[both].mean()), float(both.mean())


def heralded_win(h, p_q):
    """Win rate with heralded delivery (quantum memories): founder-rescue scenario.

    A herald tells both desks in advance whether a good pair is stored, so a missing pair
    costs nothing: rounds with a pair (fraction h) play quantum at p_q, the rest play the
    75% classical rule. No coin-flip rounds. The startup has NOT claimed memories.
    """
    return h * p_q + (1 - h) * CLASSICAL_MAX


# ---------------------------------------------------------------------------
# E3  Classical cheater (detection loophole)
# ---------------------------------------------------------------------------
def simulate_cheater(n, rng, q=0.4375):
    """Classical strategy that fakes a quantum-looking score by discarding rounds.

    Both desks always answer 0, so they lose only when x = y = 1. Whenever x = 1,
    desk A reports "no photon detected" with probability q, using only its own input.
    No entanglement, no communication. Returns (all-rounds win, detected-rounds win,
    fraction of rounds retained).
    """
    x = rng.integers(0, 2, n)
    y = rng.integers(0, 2, n)
    a = np.zeros(n, dtype=int)
    b = np.zeros(n, dtype=int)
    silent = (x == 1) & (rng.random(n) < q)
    w = wins(x, y, a, b)
    kept = ~silent
    return float(w.mean()), float(w[kept].mean()), float(kept.mean())


def cheater_exact(q=0.4375):
    """Closed form for the cheater: (all-rounds, detected-rounds, retained)."""
    retained = 0.5 + 0.5 * (1 - q)
    losses_kept = 0.25 * (1 - q)            # x=y=1 and A stayed "detected"
    return 0.75, 1 - losses_kept / retained, retained


# ---------------------------------------------------------------------------
# E4  Frontier map
# ---------------------------------------------------------------------------
REGION_GREY, REGION_RED, REGION_YELLOW, REGION_GREEN = 0, 1, 2, 3


def frontier_region(d_km, window_s, p_demo=0.82, detector_eff=1.0,
                    c_km_s=SPEED_OF_LIGHT_KM_S):
    """Classify a (separation, decision window) point. Works on arrays.

    grey   : the window is longer than light-travel time, so one classical bit arrives
             and wins every round.
    green  : no time for a bit, and fibre efficiency beats the threshold at p_demo.
    yellow : no time for a bit; only an ideal source near the 2/3 floor could win.
    red    : no time for a bit and too much photon loss for any quantum strategy.
    """
    d_km = np.asarray(d_km, dtype=float)
    window_s = np.asarray(window_s, dtype=float)
    eta = fibre_eta(d_km, detector_eff=detector_eff)
    region = np.full(np.broadcast(d_km, window_s).shape, REGION_RED)
    region = np.where(eta > EBERHARD_FLOOR, REGION_YELLOW, region)
    region = np.where(eta > eta_threshold(p_demo), REGION_GREEN, region)
    region = np.where(window_s > d_km / c_km_s, REGION_GREY, region)
    return region


# ---------------------------------------------------------------------------
# E5  Biased inputs (Ding & Jiang, Theorem 10)
# ---------------------------------------------------------------------------
def biased_classical(p):
    """Classical value when each input is 1 with probability p (Theorem 10)."""
    return 1 - p**2 if p <= 0.5 else -(p**2) + 2 * p


def biased_quantum(p):
    """Quantum value when each input is 1 with probability p (Theorem 10)."""
    lo, hi = 1 - 1 / math.sqrt(2), 1 / math.sqrt(2)
    if lo <= p <= hi:
        return (1 - 2 * p * (1 - p)) / math.sqrt(2) + 0.5
    return biased_classical(p)


def biased_quantum_numeric(p, rng, starts=30):
    """Independent check of Theorem 10: optimise CHSH angles on a maximally entangled state.

    For XOR games a maximally entangled state with planar measurements is optimal
    (Tsirelson), so maximising over four angles gives the true quantum value.
    """
    from scipy.optimize import minimize

    def neg_value(t):
        alpha, beta = t[:2], t[2:]
        v = 0.0
        for x, y in itertools.product((0, 1), repeat=2):
            w = (p if x else 1 - p) * (p if y else 1 - p)
            sign = -1 if (x & y) else 1
            v += w * (1 + sign * math.cos(2 * (alpha[x] - beta[y]))) / 2
        return -v

    return max(-minimize(neg_value, rng.uniform(0, math.pi, 4)).fun for _ in range(starts))


# ---------------------------------------------------------------------------
# E6  Economics
# ---------------------------------------------------------------------------
def edge_per_round(p_quantum, p_classical=0.75, payoff=100.0,
                   cost_quantum=0.08, cost_classical=0.001):
    """Extra dollars per round from quantum over classical.

    Each win/loss swing is 2 x payoff, so the edge is 2*payoff*(rate gap) minus the
    extra operating cost. The +/-$100 payoff is invented by the case file.
    """
    return 2 * payoff * (p_quantum - p_classical) - (cost_quantum - cost_classical)


def rounds_for_target(target_usd, edge_usd):
    """Rounds per year needed to earn target_usd at edge_usd per round (inf if edge <= 0)."""
    return target_usd / edge_usd if edge_usd > 0 else math.inf


def hours_to_generate(rounds, pairs_per_s=1000.0, usable_fraction=1.0):
    """Hours for the source to supply `rounds` usable pairs."""
    return rounds / (pairs_per_s * usable_fraction) / 3600.0
