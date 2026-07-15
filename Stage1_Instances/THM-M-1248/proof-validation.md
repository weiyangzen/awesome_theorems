# THM-M-1248 proof-phase validation

Item: `S56-M-1248-PROOF`

Validated: `2026-07-15T15:48:22+08:00`

Base revision: `80f0191c83a1bb4026c2d490be957cf109464de1`

## Implemented exact body

`Proof.lean` now contains a premise-free local body for the exact frozen Lean
target. The body deliberately does not pretend to formalize the intended
Caffarelli-Kohn-Nirenberg argument. Instead, it proves the semantic defect in
the frozen statement: unqualified `ContDiff Real top` elaborates to analytic
order `omega`, not smooth order `infinity`. Since admissibility gives `n > 0`,
the Euclidean domain is noncompact. A compactly supported analytic function on
this connected domain vanishes identically by analytic uniqueness. The exact
root then holds with `C = 1` because every quantified test function is zero.

This is real kernel evidence for
`Stage1Instances.THM_M_1248.CaffarelliKohnNirenbergTarget` as currently frozen,
not proof credit for the mathematical CKN theorem. A second source mismatch
also remains: the weighted definitions take the radial norm on raw
`Fin n -> Real` (Pi/sup norm) while evaluating the function after Euclidean/L2
transport. No checked transport maps this mixed encoding to the source claim.
Under the weaker-status-wins rule, the receipt proposes `M5` and requires
statement rework rather than `M0`.

## Commands and results

All Lean checks reused the automation-provided pinned `.lake` artifacts
read-only. No `lake update`, `lake build`, dependency clone/fetch/checkout,
network action, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1248` | 0 | Rank 428; `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1248/check_statement.py` | 0 | Existing statement expression and four recorded mutations passed; this structural check did not detect the semantic `top`/`infinity` mismatch. |
| `python3 Stage1_Instances/THM-M-1248/check_obligation_tree.py` | 0 | Existing frozen registry passed with 18 obligations and 43 typed edges; its old weighted route remains unreconciled with the direct vacuity body. |
| `bash Stage1_Instances/THM-M-1248/check_proof.sh` | 0 | Trust-zero Lean elaborated Statement, ObligationTree, and Proof; the helper and exact root are sorry-free and report exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| token-anchored prohibited-construct scan over owned Lean files | 1 expected | No `sorry`, `admit`, `sorryAx`, bodyless `axiom`, `unsafe`, `opaque`, `implemented_by`, `native_decide`, or `extern` token was found. |
| `python3 Stage1_Instances/THM-M-1248/check_proof.py` | 0 | Source markers, content hashes, pins, mismatch boundary, receipt, and worker packet passed. |
| JSON parsing of `proof-receipt.json` and `.stage1-worker-selftest.json` | 0 | Both structured artifacts parsed. |
| `git diff --check -- Stage1_Instances/THM-M-1248 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |

`check_proof.sh` obtains the executable and `LEAN_PATH` with the existing
pinned `lake env`, copies the three modules under `/tmp`, and invokes Lean with
`--trust=0 -t0`. Temporary outputs are removed by a shell trap.

## Status boundary

The proof phase is self-tested for the exact frozen proposition and handed off
as `[_]` for master review. The master must not grant positive CKN proof credit:
the exact source-to-formal statement gate fails, the internal frozen analytic
route is bypassed rather than closed, and the accepted dossier remains
unchanged. Reopen and version `Statement.lean` using smooth order `infinity`
and a consistent Euclidean radial encoding, then re-freeze dependent hashes,
the obligation registry, typed graphs, and proof work. Audit, validation,
release, independent verification, and theorem completion remain open.
