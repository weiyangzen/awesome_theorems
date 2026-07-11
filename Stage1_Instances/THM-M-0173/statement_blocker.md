# Statement phase blocker

## Requested root

The intake-selected root is the full Atiyah-Singer equality for every elliptic differential
operator between finite-rank smooth complex vector bundles on a compact boundaryless smooth
manifold:

```text
analyticIndex(D) = topologicalIndex(symbol(D))
```

Neither a Dirac specialization nor a cohomological characteristic-class formula is an equivalent
replacement at this gate.

## Pinned-environment audit

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains manifold,
boundaryless-manifold, compact-space, topological vector-bundle, and finite-dimensional APIs. A
source scan found no implementation of the required differential-operator, principal-symbol,
ellipticity, Fredholm-operator index, compactly supported K-theory, or topological-index objects.
The mentions of Fredholm operators in the pinned tree are prose/TODO material or concern the
Fredholm alternative for compact operators, not the index-theorem object model.

`StatementInfrastructure.lean` is therefore only a kernel-checked availability probe. It does not
declare the canonical proposition. Defining a local record with arbitrary integer fields called
the analytic and topological indices would not encode the source theorem and is rejected as a
substitution.

## Exact validation

Base revision: `bd4f335d8afb4d242d9df61f9d79a60034c17dfc`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard projection valid: 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest valid: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0173` | 0 | Rank 127, planned, L0/rework-required, theorem incomplete |
| `rg -n 'Atiyah\\|Singer\\|topological index\\|analytic index\\|Elliptic.*Operator\\|DifferentialOperator\\|Fredholm\\|KTheory\\|K-theory\\|principal symbol' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | No required index-theorem object model; only unrelated/textual Fredholm hits |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0173/StatementInfrastructure.lean` | 0 | The six pinned infrastructure constants elaborate |

## Verdict

The exact-statement gate remains blocked at `M4`. No expression fingerprint or mutation certificate
can truthfully be issued before the missing formal object model is implemented or a compatible
immutable Lean 4 dependency providing it is pinned. The next actionable work is the anchor audit;
if that finds no compatible implementation, construction of these definitions is proof-phase
infrastructure rather than a statement-only wrapper. This node is not self-tested as complete, and
no worker self-test receipt is emitted.
