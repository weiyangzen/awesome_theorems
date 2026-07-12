# Intake validation

Base revision: `3436a9512b8c720d6b89ba3b8a1d4c405ae3a95f`.

Validation is limited to manifest consistency, dossier structure, scope invariants, toolchain
availability, JSON syntax, and whitespace. The existing canonical `.lake` artifacts were used read
only. No exact source statement or Lean expression exists yet, so no theorem elaboration or kernel
proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0654` | exit 0; rank 699, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux release |
| `python3 -m json.tool Stage1_Instances/THM-M-0654/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0654/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0654` | exit 0; no output |

The bibliographic locator was checked with a read-only Crossref query for the paper title; it
returned Robinson, 1956, journal volume 59, pages 47-58, and the DOI recorded in the crosswalk.
That network lookup is discovery evidence, not a pinned validation recipe or source-proof audit.

Known downstream failures are deliberate and explicit: primary-source theorem/page inspection,
errata review, exact source-to-statement mapping, canonical Lean elaboration and mutations, anchor
audit, proof, hermetic replay, and independent review remain open. They prevent statement and
theorem completion but do not invalidate this fail-closed planned intake.
