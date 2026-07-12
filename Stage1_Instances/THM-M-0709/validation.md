# Intake validation

Base revision: `2ff2721a0184cf5f856054cb7d46b10dbc703f5a`.

The pre-existing untracked `Formalizations/Lean/.lake` link exposes the canonical pinned artifacts
reused read-only by this worker; this intake did not update or otherwise mutate `.lake`. This is
nonrelease worker evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0709` | exit 0; rank 750, planned, L0/rework_required, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0709/IntakeProbe.lean)` | exit 0; `ComputablePred`, `IsMatch`, and `HasSolution` elaborated with the displayed expected types |
| `python3 -m json.tool Stage1_Instances/THM-M-0709/instance.json >/dev/null` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0709/task-dag.json >/dev/null` | exit 0 |
| scoped Python dossier assertions | exit 0; `intake invariant check: ok (7 artifacts, planned, 6 downstream tasks open, no accepted proof state)` |
| `git diff --check -- Stage1_Instances/THM-M-0709` | exit 0; no output |

The Lean probe checks only that the finite tile/match shape and `ComputablePred` vocabulary are
available. It does not select an effective encoding, elaborate the canonical undecidability target,
or prove anything. Source pinpointing and review, statement fingerprints and mutation tests,
anchor audit, obligation freeze, proof, trust closure, readable reconstruction, hermetic replay,
independent verification, master acceptance, and release remain open.
