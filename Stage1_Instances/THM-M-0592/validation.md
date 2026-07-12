# Intake validation

Base revision: `f247e0d21ae7b4235e6bc7f78c1fad05b754ff16`.

Validation is intentionally limited to membership, manifest consistency, the planned dossier's
structured invariants, the availability of the pinned Lean toolchain, and whitespace. Because the
repository source does not identify a proposition, there is no canonical Lean expression to
elaborate and no kernel theorem result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0592` | exit 0; rank 632, planned, L0/rework_required, theorem_complete false |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool Stage1_Instances/THM-M-0592/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0592/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0592` | exit 0; no output |

Known downstream failures are deliberate and fail closed: the target needs correction from a topic
label to one exact source proposition; primary-source theorem/page/assumption/errata review,
canonical Lean elaboration, mutation tests, anchor audit, obligation registry, proof, hermetic replay,
and independent review are all open. These prevent statement and theorem completion but do not
invalidate a truthful planned intake.

The worktree already contained the untracked canonical `.lake` link exposed at
`Formalizations/Lean/.lake`; this run did not modify or fetch dependency artifacts. The shared pinned
cache is toolchain evidence only and is not release evidence.
