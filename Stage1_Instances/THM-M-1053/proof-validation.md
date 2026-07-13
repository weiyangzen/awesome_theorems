# THM-M-1053 Proof-Phase Validation

Item: `S56-M-1053-PROOF`. Base revision:
`309f58b7a54d36653b3483a543c6378eea53882c`.

## Implemented Bodies

The complete `MaximalErgodic.lean` and `Birkhoff.lean` proof modules are
vendored from Apache-2.0 project `marcmorningstar/lean4-ergodic-theory` at
commit `ed3fa6b8a30594eeb791160563942ba115581aa0`. The compatibility delta is
limited to the target-local sibling import and the pinned-mathlib spelling
`integrable_finset_sum`; both files carry modification notices, and the full
upstream license and exact provenance are included.

`Proof.lean` uses conditional expectation onto the invariant measurable space
to implement the frozen `GeneralInvariantLimitPackage`. The general Birkhoff
theorem proves almost-everywhere convergence, while `integrable_condExp` and
`condExp_invariants_comp_self` prove the witness's integrability and
invariance. The exact unchanged `StatementShape` root is then proved directly:
in the ergodic branch, uniqueness of limits compares the general conditional-
expectation limit with the port's independently proved space-integral limit.

## Frozen-Graph Defect

The pre-proof `ErgodicLimitIdentificationPackage` is false as written. It says
that every integrable invariant `g` equals the integral of an unrelated
integrable `f`; it omits an integral-preservation relation between them.
`not_ergodicLimitIdentificationPackage` remains a kernel-checked counterexample
using `f = 0` and `g = 1` on the one-point ergodic probability space.

Consequently the exact root is kernel inhabited, but the frozen proof graph is
not closed through all of its declared edges. It remains open at
`M1053-L-DENSE-CLASS` (the successful proof uses a different analytic route)
and `M1053-L-ERGODIC-IDENTIFICATION` (the frozen target is false) until the
integration lane accepts registry v2 or an append-only correction. No worker
edit was made to the frozen registry, typed graph, execution DAG, or blueprint
checklist.

## Obligation Map

| Frozen semantic node | Implementing body or boundary |
|---|---|
| `M1053-L-MAXIMAL` | `ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg` and its local supporting lemmas in `MaximalErgodic.lean` |
| `M1053-L-DENSE-CLASS` | route mismatch: the successful vendored proof uses invariant conditional expectation and one-sided maximal estimates rather than the frozen dense-class decomposition |
| `M1053-L-AE-CONVERGENCE` | `ErgodicTheory.tendsto_birkhoffAverage_ae` |
| `M1053-L-LIMIT-INTEGRABLE` | `integrable_condExp` in `generalInvariantLimitPackage_proof` |
| `M1053-L-LIMIT-INVARIANT` | `ErgodicTheory.condExp_invariants_comp_self` |
| `M1053-T-GENERAL` | `Stage1.THM_M_1053.generalInvariantLimitPackage_proof` |
| `M1053-L-ERGODIC-IDENTIFICATION` | inconsistent frozen target, refuted by `not_ergodicLimitIdentificationPackage`; the correct identification is internal to `tendsto_birkhoffAverage_ae_integral` and the exact-root uniqueness argument |
| `M1053-X-EXTERNAL` | locally vendored, provenance-reconstructable `MaximalErgodic.lean` and `Birkhoff.lean` |
| `M1053-ROOT` | `Stage1.THM_M_1053.statementShape_proof`, an exact-type alternate composition |

## Commands And Results

Validation ran in this worker clone on 2026-07-14 using only the existing
pinned Lake environment. No update, build, clone, fetch, or mutation of
`.lake` was performed.

```text
python3 Stage1_Instances/THM-M-1053/check_proof.py
  exit 0
  Fresh trust-level-zero temporary elaboration passed for Statement,
  ObligationTree, MaximalErgodic, Birkhoff, and Proof. Three vendored terminal
  declarations and three local declarations were sorry-free and reported only
  [propext, Classical.choice, Quot.sound]. Exact StatementShape passed; the
  checker reported the inconsistent frozen identification child graph-open.

python3 Stage1_Instances/THM-M-1053/check_obligation_tree.py
  exit 0
  Frozen 16-obligation registry and 35 typed edges passed; the pre-proof
  closure projection remains intentionally unchanged and root-open.

python3 Docs/tools/check_stage1_standard.py
  exit 0
  15 assurance groups and all 1546 uniform-L0 targets passed.

python3 scripts/stage1_target.py check
  exit 0
  1546 unique ordered targets, ranks 1 through 1546.

python3 scripts/stage1_target.py show THM-M-1053
  exit 0
  Rank 245, planned, L0/rework-required, theorem_complete=false.

python3 -m json.tool Stage1_Instances/THM-M-1053/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for both files.

git diff --check -- Stage1_Instances/THM-M-1053 \
  .stage1-worker-selftest.json
  exit 0; no whitespace errors.
```

## Status Boundary

This is self-tested proof-node evidence proposing only `[_]`, pending master
acceptance and graph correction. It establishes a placeholder-free kernel proof
of the exact canonical root in the current pinned environment; it does not
establish frozen-graph closure, an accepted state, H0/R0, complete transitive
trust and provenance, hermetic replay, independent verification, audit
completion, or theorem completion.
