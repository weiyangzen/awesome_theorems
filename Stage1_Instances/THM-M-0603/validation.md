# Intake validation

Base revision: `83c1cc0af3ba7bd4612988241849d2949fad9e72` (tree
`e7ff66969e8c4de88c41e34603fc7879142296b0`).

Validation is limited to manifest membership, repository-standard consistency, dossier structure,
JSON syntax, planned-state invariants, pinned toolchain availability, and whitespace. The received
source phrase does not determine a canonical proposition, so elaborating an invented Lean theorem
would be substitution rather than validation. Consequently no theorem file is compiled and no
kernel proof result is claimed at intake.

| Command (from repository root unless noted) | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0603` | exit 0; rank 641, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0603/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0603/task-dag.json` | exit 0 |
| scoped Python assertions over identity, lifecycle, rank, accepted states, formal target, and six open downstream nodes | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git diff --check -- Stage1_Instances/THM-M-0603 .stage1-worker-selftest.json` | exit 0; no output |

The automation-provided untracked `Formalizations/Lean/.lake` link exposes the canonical pinned
artifacts. This run did not create or mutate it and ran no update, build, clone, or fetch.

Known downstream failures are intentionally open: a pinpoint primary theorem and errata review;
resolution of unoriented/oriented/Pontryagin-Thom scope; canonical Lean elaboration, fingerprints,
and mutation tests; immutable anchor audit; obligation registry; proof; hermetic replay; and
independent release verification. They prevent audit and theorem completion but do not invalidate
this fail-closed planned intake.
