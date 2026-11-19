# Autonomous local multi-agent execution

## What is automatic versus not
The repository contains a **local** orchestration plan, role prompts and a task DAG. With a supported installed CLI (Claude Code or Codex), scripts/autopilot.py can dispatch tasks in isolated worktrees, request code changes, run the same scientific CI checks and retain logs. It does not create an always-on hosted agent merely by being in GitHub.

Default invocation is a safe preview. Actual agent execution requires --execute. GitHub publishing requires --publish and the user to have authenticated gh; any merge needs a separate audited process. This prevents an autonomous agent from silently fabricating an experiment and publishing it as verified fact.

## Inputs
- automation/tasks.json: ID, agent, instruction path, deps, allowed paths, acceptance criteria, status field.
- agents/*.md: exact research or implementation responsibility.
- AGENTS.md: binding scientific and operational contract.
- docs/EVIDENCE_POLICY.md: claim taxonomy and anti-hallucination gates.
- src/monopoly: tested methods that every new agent should reuse.
- docs/ROADMAP.md: integration milestone order.

## Recommended workstreams
Independent until integration:
1. CHSH theorem and finite-sample inference.
2. Light-cone, classical routes and causality.
3. Photonic architecture, loss and memories.
4. Adversarial detector and selection audit.
5. Market/game matching, payoff surgery, investment math.
6. Source verification and competing product-pivot hypotheses.
7. Interactive exhibit/UI.
8. Technical writing and academic deliverables.
9. Integration/CI and independent red-team review.

Agents 1–8 write only owned paths. Agent 9 reviews integration. Agent 10 red-teams sources and derivations. The lead agent resolves conflicts and is responsible for final claims.

## Contract for every task
- **Input:** exact task description, latest tested repo, explicit dependencies.
- **Output:** changed files in owned paths, added tests, reproducible figures or decision records.
- **Evidence:** command output, source URL plus claim, machine-readable provenance.
- **Review:** no scientific claim without validation by a separate reviewer.
- **Stop:** all tests pass + acceptance conditions met, or an explicit blocker is logged.

## CLI execution
    python scripts/autopilot.py --list
    python scripts/autopilot.py --dry-run
    python scripts/autopilot.py --execute --provider codex --task R02
    python scripts/autopilot.py --execute --provider claude --task R03

An agent's tool availability and model subscription are not provided by this repo. Verify installations first:
    command -v codex
    command -v claude
    command -v gh

The script must use independent git worktrees per task and never hand a secret to an LLM as a prompt. It must not execute in-place on main. If a task cannot run without permissions or credentials, it must fail clearly.

## Advancement and integration policy
- Prefer short scoped PRs.
- Lead agent reviews numerical changes against tests and research sources.
- Do not auto-merge a PR merely because a code test passes: policy-level science claims require a review sign-off.
- When the work is computational, tests must be deterministic and independent of paid API access.
- Document negative results rather than forcing positive hypotheses.

## Recovery
Worktrees, task logs, result JSON and error traces live outside version control, under .agent_runs/ and .worktrees/. A failed run is not silently retried forever. Retain task state and suggest a bounded retry only after the underlying error is understood.

## Security
Never commit credentials, broker connections, tokens, customer information or course-only material. Set local CLI auth with vendor tooling outside the repo. Only allow task worktrees to mutate their owned files; independent tests and a diff review must catch attempts to broaden scope.
