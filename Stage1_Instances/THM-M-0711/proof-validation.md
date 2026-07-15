# THM-M-0711 proof-phase validation

Item: `S56-M-0711-PROOF`. Base revision:
`443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`.

## Implemented bodies

`Proof.lean` implements the exact quotient-identity transport through
`PresentedGroup.mk_eq_one_iff`, the generic backwards transfer of computability
through a computable many-one reduction, and the pinned fixed-input halting
theorem in the source-predicate shape used by the frozen route. It composes
those bodies into `FixedPresentationUndecidable` and then the exact
`NovikovBooneTarget`, conditional on an explicit halting-to-identity reduction.

That reduction premise remains visible. No body constructs the finite
presentation, the computable compiler from halting codes to signed words, or
the correctness equivalence. Consequently the conditional declarations are
not an unconditional witness or root proof. Provisional machine credit is
limited to `M0711-N-QUOTIENT`, `M0711-L-HALTING`, and
`M0711-L-MANYONE`; their frozen fingerprints are still planned and require
master reconciliation. `M0711-L-NONCOMP`, `M0711-T-WITNESS`, and
`M0711-ROOT` receive partial-progress classification only.

Lean checked all five local proof declarations and the three pinned terminal
declarations as transitively sorry-free. Every axiom report contains exactly
`propext`, `Classical.choice`, and `Quot.sound`. The source contains no
`sorry`, `admit`, `sorryAx`, added axiom or constant, unsafe or external
declaration, `implemented_by`, or `native_decide` shortcut.

## Commands and results

Commands ran in the worker clone on 2026-07-15 (Asia/Shanghai). The existing
canonical pinned mathlib sources and build artifacts were reused read-only. No
update, build, dependency clone or fetch, network validation, or `.lake`
mutation was performed.

```text
bash Stage1_Instances/THM-M-0711/check_proof.sh
  exit 0
  isolated Statement.olean, ObligationTree.olean, and Proof.lean elaboration
  passed at --trust=0; eight declarations reported sorry-free; axioms were
  [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0711/check_proof.py
  exit 0
  exact declarations, frozen hashes and pins, receipt/blocker boundary,
  prohibited-device scan, and worker packet passed

python3 Stage1_Instances/THM-M-0711/check_obligation_tree.py
  exit 0
  17 obligations and 38 typed edges passed; root remains open M4

python3 Docs/tools/check_stage1_standard.py
  exit 0
  15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0
  1546 unique targets at ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0711
  exit 0
  rank 751, planned, L0/rework_required, theorem_complete false

git diff --check -- Stage1_Instances/THM-M-0711 \
  .stage1-worker-selftest.json
  exit 0; no whitespace errors
```

The top-level `lake env lean` entrypoint was temporarily unavailable because
the unrelated shared `flt-regular` checkout could not resolve `HEAD`. The
narrow replay did not repair or bypass a moving dependency: the recipe used
Lake inside the pinned clean mathlib package only to select the same Lean
binary and compiled dependency closure, corrected stale nested package-path
prefixes in the process environment, and wrote target oleans to an ephemeral
directory. The receipt binds the Lean binary, mathlib revision/tree, terminal
source blobs, sources, and oleans used by that replay. This environment
limitation keeps the result nonrelease evidence.

The first failed proof gate is `M0711-B-REDUCTION`. The remaining root cut is
`M0711-B-REDUCTION` plus the independent `M0711-S-FOUNDATION` gate. The exact
root stays `[H1, M4, R4]`; accepted state, source/readability closure,
validation, hermetic and independent replay, release, audit completion, and
theorem completion remain open.
