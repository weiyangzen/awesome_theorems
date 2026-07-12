# Obligation-tree validation

Date: `2026-07-12`  
Base revision: `58cde546113e54bfa95299c69db6ee1508316872`

The generated registry contains 11 unique semantic obligations and seven separate typed graphs.
All four proof requirements have reciprocal composition edges. The root-reachable proof spine is
acyclic, all node schemas and budgets validate, and every validation recipe denies network access.

## Commands and results

- `python3 Docs/tools/check_stage1_standard.py`: exit 0,
  `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)`.
- `python3 scripts/stage1_target.py check`: exit 0,
  `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)`.
- `python3 scripts/stage1_target.py show THM-M-1252`: exit 0; rank 431, lane
  `hard_mathlib_anchor_and_wrapper`, lifecycle `planned`, theorem complete `false`.
- From the repository root, `python3 Stage1_Instances/THM-M-1252/build_obligation_artifacts.py`:
  exit 0; wrote 11 obligations and 20 typed edges; denominator SHA-256
  `7c154670d8d80bc38a9977dd5e63f0ae189a3c6bf27653b4b042b94b6018fe8c`.
- From the repository root, `python3 Stage1_Instances/THM-M-1252/check_obligation_tree.py`:
  exit 0; `PASS THM-M-1252 obligation tree: 11 obligations, 20 typed edges`; root remains
  open at M3 and anchor installation remains downstream.
- From `Formalizations/Lean`,
  `lake env lean ../../Stage1_Instances/THM-M-1252/ObligationTree.lean`: exit 0; the pinned
  `Distribution.dsupport_compl_eq` type was printed and both conditional composition declarations
  reported only `propext`, `Classical.choice`, and `Quot.sound`.

No `lake update`, build, fetch, clone, or `.lake` mutation was performed. The existing
`Formalizations/Lean/.lake` symlink is an untracked automation-clone fixture and is not claimed as
a changed artifact.

## Status boundary

This self-test freezes and validates the obligation architecture only. It does not install the
anchor as the canonical proof artifact, close the root, establish H0 or R0, validate transitive
provenance, complete the audit, or complete the theorem. Master acceptance is still required.
