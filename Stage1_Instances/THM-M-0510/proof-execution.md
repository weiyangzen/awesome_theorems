# THM-M-0510 proof-phase validation

Item: `S56-M-0510-PROOF`
Base revision: `7505614b75de56cf10bbd196a4aaa0ca2a117064`

## Implemented body

`Proof.lean` closes the frozen ordinary-partition Euler-product normalization. It defines the
formal power series whose `n`th coefficient is the canonical real-valued `partitionCount n`,
specializes the pinned `Nat.Partition.hasProd_powerSeriesMk_card_restricted` theorem to all
positive parts, proves the geometric-factor cancellation identity, and composes the products to
obtain

```text
ordinaryPartitionSeries * product_i (1 - X^(i+1)) = 1.
```

Together with `coeff_ordinaryPartitionSeries`, this supplies the coefficient convention and
reciprocal Euler denominator required by `M0510-N-EULER-PRODUCT`. The earlier blocker overlooked
the indirect all-parts specialization in `Partition.Glaisher`; the direct `f = 1` specialization
remains a documentation TODO in `Partition.GenFun`, but it is no longer a proof blocker here.

## Boundary

The first remaining machine gate is `M0510-N-COEFFICIENT`: pinned mathlib has generic Cauchy and
modular-form coefficient integrals, but no checked bridge from this formal partition series to the
required complex contour integral. The contour construction, arc split, modular local estimate,
major-arc evaluation, minor-arc bound, and recomposition also remain open. The existing
`root_of_finalAsymptotic` theorem merely returns a hypothesis definitionally equal to the root and
earns no analytic or root credit. The root is not kernel-closed and `theorem_complete=false`.

## Commands and exact results

Validation reused only the pre-existing pinned `.lake` artifacts. No update, build, dependency
clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-0510/check_proof.sh` | 0 | `Statement.lean` and `Proof.lean` elaborated under `--trust=0`; all five declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0510/check_obligation_tree.py` | 0 | Frozen predecessor passed with 17 obligations and 59 typed edges; its pre-proof root remains open M3 |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0510` | 0 | Rank 884; lifecycle `planned`; L0/rework-required; theorem incomplete |
| placeholder scan over `Proof.lean` | 1 | Expected no-match exit; no executable placeholder, bodyless axiom/constant, unsafe/opaque/extern declaration, implementation escape, or native oracle |
| `git diff --check -- Stage1_Instances/THM-M-0510 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors |

This packet proposes `[_]` only for the self-tested proof-phase contribution. Master acceptance,
all downstream validation/release gates, audit completion, and theorem completion remain open.
