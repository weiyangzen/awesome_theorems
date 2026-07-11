# THM-M-0401 proof-phase validation

Item: `S56-M-0401-PROOF`

## Implemented body

`Proof.lean` implements `productTooGood_has_integer_point`, the frozen
`M0401-N-INTEGER-POINT` normalization leaf. From the exact exceptional-denominator
predicate it chooses a nearest integer in every coordinate and returns the positive denominator,
all exact distance/minimality facts, and the unchanged strict product bound. The theorem has no
placeholder and introduces no mathematical premise.

The local definition block is textually identical to the definitions in `Statement.lean`; the
check script elaborates both source files independently because Lean will not emit an `.olean` for
a source outside the Lake package root. This partial proof does not supply the qualitative Subspace
Theorem, height bridge, independence-limit argument, terminal composition, or root proof. Thus the
root remains `M4` and theorem completion is false.

## Commands and exact results

Base revision: `15a5351889f1657f452569fe630c9e39edb81877`. Validation ran on 2026-07-12
Asia/Shanghai.

| command | exit | result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | assurance standard and target-set checks passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and targets passed |
| `python3 scripts/stage1_target.py show THM-M-0401` | 0 | rank 14, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0401/validate_obligation_tree.py` | 0 | frozen 14-node obligation architecture passed; root open M4 |
| `(cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0401/check_proof.sh)` | 0 | statement and proof elaborated; proof reports only `propext`, `Classical.choice`, and `Quot.sound` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean version recorded in the worker self-test summary |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision recorded in the worker self-test summary |
| prohibited-token scan of `Proof.lean` | 1, expected empty | no prohibited proof construct occurs in executable Lean source |
| `git diff --check -- Stage1_Instances/THM-M-0401 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No `lake update`, `lake build`, dependency clone/fetch, network access, or `.lake` mutation was
performed. The pre-existing untracked `Formalizations/Lean/.lake` symlink is the scheduler-provided
canonical artifact reuse surface.

## Remaining cut set

`M0401-C-LINEAR-FORMS`, `M0401-C-HEIGHT-BOUND`, `M0401-L-SUBSPACE-BRIDGE`,
`M0401-L-FINITE-SUBSPACES`, `M0401-L-RELATION-EXTRACTION`,
`M0401-L-INDEPENDENCE-LIMIT`, `M0401-T-SUBSPACE-FINITE`, and
`M0401-T-FINITE-DENOMINATORS` remain without proof bodies. Root composition, provenance,
validation, release, H0, R0, and theorem completion are unclaimed. This is a self-tested partial
proof-phase result pending master acceptance.
