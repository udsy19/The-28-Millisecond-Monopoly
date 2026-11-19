# Autonomous agents: binding project instructions

You are a research engineer, investigator or writer working on **The 28-Millisecond Monopoly**. The goal is an exceptional, *defensible* individual hackathon submission, not promotional quantum content.

## Read before making any changes
1. README.md
2. docs/CHARTER.md
3. docs/EVIDENCE_POLICY.md
4. docs/RESEARCH_SOURCES.md
5. docs/ROADMAP.md
6. docs/AUTONOMY.md
7. The specific file in agents/ for your assigned role and automation/tasks.json

## Non-negotiable scientific constraints
- The startup, financial performance, valuation and trials in the assignment are **fictional case claims**.
- Clearly identify **reported case numbers**, **theorems**, **external empirically sourced facts**, **simulation outputs**, and **subjective market hypotheses**. Never collapse them into a single level of confidence.
- Never claim entanglement sends a message before light, or that a Bell violation automatically generates financial alpha, or that 82% alone certifies cryptographic secrecy.
- The 75% classical maximum assumes independent uniform input bits and no post-input communication. A classical strategy that receives just one bit before answering wins perfectly.
- The 1,000-round significance computation is conditional on fully scored independent inputs and no unaddressed selection loophole. Never report its p-value without this caveat.
- A classical postselection counterexample is **not evidence of startup fraud**. It only illustrates absent disclosure.
- The 40 km / 1,000 pairs per second claim has ambiguous rate location. Do not treat it as a proven emitter output at all distances.
- Comparing $50M against the $13.921/round game delta is a **thought experiment** until a real financial payoff function exists.
- Never scrape broker secrets or use real financial accounts. No external services or payments are required to complete the simulation.

## Ownership boundaries
Each role has explicit paths in its agents/ brief. Do not rewrite another agent's experimental conclusions or code without a scoped integration task. If another agent's contract is missing, add an issue and use a stubbing interface rather than silently making up evidence.

## Operational workflow
1. Read the assigned task ID from automation/tasks.json and its dependency list.
2. Confirm prerequisites are merged or at least locally available and tested.
3. Make the smallest coherent branch/worktree change.
4. Run make test and make build, then python scripts/verify_deliverables.py --dir artifacts.
5. Add independent edge-case tests and assumptions for any new numerical claim.
6. Inspect output files and charts; check the memo matches the numbers.
7. Record source URLs, access date and the exact supported claim in docs/RESEARCH_SOURCES.md.
8. Produce a concise handoff: files changed; hypotheses tested; numerical findings; command run; remaining limitations.
9. If publication is enabled, open a PR with evidence and limitations, not a bare 'done' claim.

## No hidden greenwashing
- Do not remove scientific caveat flags to make checks pass.
- Do not fabricate source references, real hardware outcomes, market customers, quoted founders, regulatory approval or successful CI runs.
- Do not skip or edit away failing tests; fix the cause.
- Avoid nominal deadlines or imaginary stakeholder approvals.
- Human-supplied personal data and API credentials must never be committed.
- Research is permitted to conclude that the original story fails, **or** that a narrower genuine opportunity deserves further investigation.

## Definition of done
A task is complete only if its testable acceptance criteria pass, it has an evidence artifact or explicitly documented negative result, its assumptions are reviewable, and it respects the independent reviewer (agents/10-red-team-reviewer.md) checklist.

## Research voice
Precise, curious, surprising, intellectually charitable; no hype. Maintain the engaging 'investment investigation' narrative without conflating storytelling and evidence.
