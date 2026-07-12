# THM-M-0665 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 20 canonical obligations before the proof phase assigns any closure
credit. Seventeen are root-relevant machine obligations; `X-SOURCE`, `X-UPSTREAM`, and `X-TCB` are
informational human-source, provenance, and trust overlays. All 20 require readable coverage. The
root fingerprint is inherited from the elaborated statement; planned child fingerprints bind each
human statement to its proposed formal target. A correction, split, merge, exclusion, eligibility,
or risk change requires registry version 2 and an append-only delta.

The anchor audit found no terminal Pila-Wilkie proof body. Consequently this phase records no closed
obligation and does not upgrade the root from `M3`.

## Typed proof route

```text
M0665-ROOT  exact first-version quantitative target [open M3]
`-- M0665-T-ASSEMBLE  exact composition interface not yet formalized
    |-- M0665-N-ALGEBRAIC  isolate the transcendental locus
    |-- M0665-N-HEIGHT  finite bounded-height rational grid
    |-- M0665-B-DIMENSION  induction on definable dimension
    |   `-- M0665-L-DROP  hypersurface intersection lowers dimension
    |       |-- M0665-B-CHARTS
    |       |   `-- M0665-C-PARAM  controlled definable parametrization
    |       `-- M0665-C-HYPERSURFACE
    |           |-- M0665-L-DERIVATIVE  analytic determinant bound
    |           `-- M0665-L-ARITHMETIC  denominator bound forces vanishing
    `-- M0665-L-COUNT  choose parameters and sum lower-dimensional bounds
        |-- M0665-C-PARAM
        |-- M0665-C-HYPERSURFACE
        `-- M0665-L-DROP
```

## root

`M0665-ROOT` is exactly `Stage1Instances.THM_M_0665.PilaWilkie`, including every structure,
definability, positivity, threshold, finiteness, and cardinality binder.

## s-exact

`M0665-S-EXACT` owns the exact scope of the language and structure, the definable set, positive
epsilon, positive constant depending on prior binders, and every natural threshold at least one.

## s-defs

`M0665-S-DEFS` owns the source fidelity of affine height, rational embedding, o-minimal expansion,
and the algebraic part. The current Lean definitions elaborate, but their independent comparison to
Definitions 1.3 and 1.5 is still `H1`.

## s-boundary

`M0665-S-BOUNDARY` keeps dimension zero, empty sets, and zero-dimensional sets in scope. It records
the deliberate exclusion of nonpositive epsilon and `T = 0`; only two narrow boundary facts are
currently kernel checked.

## s-transport

`M0665-S-TRANSPORT` is the checked `pilaWilkie_iff` expansion. It is a statement transport, not a
second semantic obligation or a proof of the counting result.

## s-foundation

`M0665-S-FOUNDATION` reserves the classical, choice, real-analysis, finite-cardinality, kernel, and
dependency trust decision. A transitive axiom report cannot exist until proof declarations exist.

## n-algebraic

`M0665-N-ALGEBRAIC` isolates the complement of the union of connected positive-dimensional
semialgebraic subsets. It must prove that the chosen formal normalization matches the source's
algebraic part and does not discard transcendental points.

## n-height

`M0665-N-HEIGHT` supplies the finite ambient grid of rational points of coordinatewise affine height
at most `T`, including denominator, coercion, and `Set.ncard` compatibility lemmas.

## b-dimension

`M0665-B-DIMENSION` performs induction on o-minimal dimension, discharges dimension zero, and
requires every recursive intersection to have strictly smaller dimension.

## b-charts

`M0665-B-CHARTS` is the exhaustive finite chart branch. It prevents a single parametrization call
from hiding cell decomposition, smoothness strata, chart coverage, or uniformity.

## c-param

`M0665-C-PARAM` is the controlled parametrization engine. It constructs finitely many `C^r` maps
with derivative bounds at an order chosen from epsilon and the ambient dimension. This is a major
open formalization boundary, not a library primitive.

## c-hypersurface

`M0665-C-HYPERSURFACE` constructs a bounded-degree auxiliary hypersurface through each local cluster
of bounded-height rational points. Its two explicit children own the analytic and arithmetic halves
of the determinant method.

## l-derivative

`M0665-L-DERIVATIVE` uses Taylor expansion and chart derivative control to make the interpolation
determinant quantitatively small.

## l-arithmetic

`M0665-L-ARITHMETIC` controls determinant denominators using affine height and proves that a
sufficiently small rational determinant must vanish exactly.

## l-drop

`M0665-L-DROP` proves that intersection with an auxiliary hypersurface is either already covered by
the algebraic part or has lower definable dimension, enabling the induction without losing points.

## l-count

`M0665-L-COUNT` chooses polynomial degree, differentiability order, and box scale, then combines the
finite chart count and inductive contributions into one positive constant and the exact
`c * T ^ epsilon` estimate for every `T >= 1`.

## t-assemble

`M0665-T-ASSEMBLE` is the eventual exact root composition. It has no checked certificate in this
phase because its children have planned, not elaborated, signatures. Inventing abstract children
would not bind exact fingerprints and would create false composition evidence.

## x-source

`M0665-X-SOURCE` pins Theorem 1.8 and Definitions 1.3 and 1.5 of Pila-Wilkie (2006). Independent
inspection, errata review, and proof-node pinpointing remain open.

## x-upstream

`M0665-X-UPSTREAM` binds the immutable anchor audit. Pinned mathlib provides statement ingredients,
while three external o-minimal candidates provide no compatible terminal counting proof. None earns
proof credit.

## x-tcb

`M0665-X-TCB` remains open for transitive source, compiled-artifact, executable, axiom, and replay
closure after proof artifacts exist.

## Graph and status boundary

Proof requirements have reciprocal `composes` edges. Refinement, source/body provenance, evidence,
trust, documentation, and workflow are distinct graphs. Every preliminary budget is at most 100,
but these estimates are neither proof evidence nor accepted readability.

The frozen first proof-phase cut set is `C-PARAM`, `L-DERIVATIVE`, `L-ARITHMETIC`, `L-DROP`, and
`L-COUNT`. This phase claims no accepted node, human-source review, formal proof, composition
certificate, transitive trust closure, audit completion, theorem completion, or release readiness.
