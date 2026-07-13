# THM-M-1566 proof-phase result

Item: `S56-M-1566-PROOF`
Date: `2026-07-14`
Base revision: `c45f3c7090cb4adf616d45e5414985f956e807b2`

## Verdict

`blocked`: no positive proof body can truthfully inhabit the exact frozen
target. `ProofCountermodel.lean` proves `not_GIPCorollary59Target` in the
pinned Lean kernel without placeholders or new axioms.

The statement quantifies over every `GIPCorollary59API`, but that structure
places no adequacy or nonemptiness condition on `Solution`. The checked
countermodel uses `Omega := Unit`, the Dirac probability measure, `Unit` for
every other carrier, and `Empty` for `Solution`. The frozen data assumptions
remain inhabited at `alpha = beta = 3/4`. Applying the claimed target then
produces a unique solution, hence an inhabitant of `Empty`.

This is a statement/interface defect, not a failure to formalize the deep
paracontrolled-distribution analysis. The negative result refutes only this
abstract encoding, not Corollary 5.9 in the cited paper. The conditional
`root_of_existence_and_uniqueness` body remains valid but consumes the two
missing analytic packages and therefore cannot close the root.

The first failed gate is exact-target consistency at `M1566-S-INTERFACE`.
The frozen graph's remaining root cut remains `M1566-T-EXISTENCE` and
`M1566-T-UNIQUENESS`, but neither can be implemented uniformly for the empty
solution API. Repair requires a fixed source-faithful API or noncircular
adequacy hypotheses, followed by new statement, audit, and obligation-tree
receipts. The proof item is not complete, so `.stage1-worker-selftest.json`
is deliberately absent.

## Validation

Commands ran from this worker clone using only the existing pinned Lake
artifacts. No update, build, clone, fetch, or `.lake` write was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1566` | 0 | Rank 182, planned, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1566/check_obligation_tree.py` | 0 | 15 obligations and 40 typed edges passed; root remains open M4. |
| `python3 Stage1_Instances/THM-M-1566/validate_obligation_tree.py` | 0 | Exact statement plus conditional composition elaborated in the pinned environment. |
| Temporary `/tmp` copies; `LEAN_NUM_THREADS=1 timeout 300s lake env lean -R <tmp> -o <tmp>/Statement.olean <tmp>/Statement.lean`; then `LEAN_NUM_THREADS=1 LEAN_PATH=<tmp>:$(lake env printenv LEAN_PATH) timeout 300s lake env lean -R <tmp> <tmp>/ProofCountermodel.lean` | 0 | Exact statement and countermodel elaborated; `not_GIPCorollary59Target` uses only `propext`, `Classical.choice`, and `Quot.sound`. Temporary files were removed. |
| `rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)\|sorryAx\|unsafe' Stage1_Instances/THM-M-1566 -g '*.lean'` | 1 | No prohibited Lean token found; exit 1 means no match. |

## Status boundary

The proposed classification is `H1 / M5 / R3`; the human-source audit remains
incomplete and the checked mismatch changes only the machine axis. The frozen
registry still records `H1 / M4 / R3` pending authorized refreeze and master review. This is
a checked proof-phase blocker, not a proof receipt. `root_closed=false`,
`audit_complete=false`, and `theorem_complete=false`; no accepted receipt or
state transition is claimed.
