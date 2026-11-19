# Claude Code entry point

Read AGENTS.md first. Then read docs/AUTONOMY.md, automation/tasks.json and the role-specific prompt under agents/. Operate as an autonomous research team while retaining the scientific evidence gates.

If invoked directly without an assigned task, begin with docs/ROADMAP.md and identify the highest-priority incomplete task whose dependencies are satisfied. If a task is blocked by missing evidence, document the blocker and work on the next independent task rather than making up a result.

Preferred implementation loop:
- inspect source and tests;
- propose precise falsifiable criteria in a concise work log;
- implement only owned paths and keep generated artifacts reproducible;
- run make check;
- require an independent scientific reviewer for claims;
- leave a PR or commit with tested evidence;
- proceed to the next eligible task.

Use standard-library Python for scientific kernels, separate input source data from assumptions, and zero-build web primitives for the interactive exhibit unless a change has a strong justification.

Run commands locally only. Do not assume a coding agent can spawn more agents just because these instructions mention roles; scripts/autopilot.py coordinates invocations when a supported CLI is actually installed.

The user wants high autonomy. Do not interrupt for ordinary implementation choices. Do not change the public investment recommendation, publish external claims, push secrets or represent hypothetical revenue as real returns merely to finish a milestone.

Default project command: make check.
