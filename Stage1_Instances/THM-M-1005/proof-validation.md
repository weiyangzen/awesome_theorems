# THM-M-1005 proof-phase validation

Item: `S56-M-1005-PROOF`

Base revision: `bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`

Validation date: `2026-07-14` (`Asia/Shanghai`)

## Implemented proof

`DoobLp.lean` vendors the complete real-valued analytic proof through
`MeasureTheory.maximal_ineq_Lp` from mathlib PR `#39349`, immutable commit
`4b63335c679c15aab74a00d37714d41aa99d701d`. The Apache-2.0 copyright header is
preserved. The source is truthfully classified as a closed, unmerged submission labeled
LLM-generated, not an accepted theorem in pinned mathlib. The unrelated Banach corollary was omitted.

The vendored body supplies the frozen layer-cake, Fubini, Holder, constant, truncation, and rpow
inversion obligations. `Proof.lean` applies it to the proved absolute-value submartingale,
transports `p.toReal` back to the exact finite `ENNReal` exponent, and inhabits the unchanged
`Stage1Instances.THM_M_1005.Statement`. A second declaration consumes that body through the root
composer frozen in `ObligationTree.lean` before proof search.

The executable source contains no `sorry`, `admit`, custom axiom, `sorryAx`, unsafe/opaque
declaration, native oracle, external declaration, or `implemented_by`. Lean reports exactly
`propext`, `Classical.choice`, and `Quot.sound` for the vendored terminal and exact root.

## Commands and results

Validation used the automation-provided canonical `.lake` symlink read-only. No `lake update`,
`lake build`, dependency clone/fetch, installation, or `.lake` mutation ran.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1005` | 0 | rank 285, planned, theorem incomplete |
| `cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-1005/check_proof.sh` | 0 | isolated statement, obligation tree, vendored proof, and exact wrapper elaborated; all six axiom reports were exactly `propext`, `Classical.choice`, `Quot.sound` |
| `python3 -B Stage1_Instances/THM-M-1005/check_proof.py` | 0 | exact target, frozen inputs, provenance, source hashes, license, receipt, placeholder boundary, and worker packet passed |
| `python3 -B Stage1_Instances/THM-M-1005/check_obligation_tree.py` | 0 | frozen denominator and 48 typed edges remained unchanged; accepted pre-proof root remained open pending master acceptance |
| `python3 -B Stage1_Instances/THM-M-1005/check_statement.py` | 0 | canonical expression SHA-256 `32343e66034f94d4afabc10f4d15cbae77daf650c757023a2142aafba50366e5`; four mutations distinguished |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386...ea95`, tree `bdc39a31...c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned dependency worktree remained clean |
| `python3 -m json.tool` on proof receipt, resolved blocker, and worker self-test | 0 | all structured artifacts parsed |
| `git diff --check -- Stage1_Instances/THM-M-1005 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This is provisional proof-phase evidence and proposes root `M0-L` only after master acceptance,
because the terminal proof body is vendored into the repository rather than imported as a wrapper.
The authoritative accepted state remains `H2/M3/R4`; neither the generated checklist nor task DAG
was edited. Validation, release, H0, R0, full transitive provenance and TCB closure, hermetic cold
replay, independent verification, and deterministic release evidence remain open. No audit or
theorem completion is claimed.
