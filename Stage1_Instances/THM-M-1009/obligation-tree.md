# THM-M-1009 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 15 obligations before proof-phase closure is
observed. Ten are root-relevant machine obligations; five are source,
provenance, trust, documentation, and workflow overlays. All require readable
coverage. A correction, split, merge, eligibility change, exclusion, or risk
change requires registry version 2 and an append-only ID delta.

## Typed proof route

```text
M1009-ROOT
`-- M1009-T-ASSEMBLE
    |-- M1009-S-EVENTS
    |-- M1009-S-DIVERGE
    |-- M1009-B-ZERO
    |-- M1009-L-TAIL
    |   `-- M1009-L-SECOND-MOMENT
    |       `-- M1009-N-COUNT
    |-- M1009-L-RATIO
    `-- M1009-L-CONTINUITY
```

## root

`M1009-ROOT` is exactly the statement-phase lower bound. No independence or
positive-denominator assumption is added, and no probability-one corollary is
substituted.

## s-events

`M1009-S-EVENTS` owns the probability-space binders and pointwise measurable
event hypothesis.

## s-diverge

`M1009-S-DIVERGE` owns divergence to `atTop` of the real initial-segment
probability sums.

## b-zero

`M1009-B-ZERO` records the `n = 0` branch and Lean's ordinary real division by
zero. `ObligationTree.zero_ratio` checks the selected convention.

## n-count

`M1009-N-COUNT` introduces the finite indicator count and must identify its
first moment with the single sum and its second moment with the ordered double
intersection sum. These identities are substantive proof work, not notation.

## l-second-moment

`M1009-L-SECOND-MOMENT` is the finite Paley-Zygmund/Cauchy-Schwarz lower bound
for the probability that the count is positive. Its statement and proof must
handle a zero second moment without adding a denominator premise.

## l-tail

`M1009-L-TAIL` applies the finite bound to shifted windows and passes from a
finite union to the measurable tail union.

## l-ratio

`M1009-L-RATIO` is the main analytic bridge: it must compare shifted-window
ratios with the frozen initial-segment ratio and establish the required filter
limsup inequality under divergence. This is not supplied by a nearby
Borel-Cantelli declaration.

## l-continuity

`M1009-L-CONTINUITY` identifies the decreasing intersection of measurable
tail unions with `limsup A atTop` and applies continuity from above.

## t-assemble

`M1009-T-ASSEMBLE` composes the four mathematical leaves into the exact root.
The Lean `root_compose` declaration checks only the binder-level conditional
interface; its premise remains open and therefore proves no unconditional
lower bound.

## x-source

`M1009-X-SOURCE` remains `H1`: the primary paper's exact formula, theorem/page,
assumptions, corrections, and relationship to later Kochen-Stone terminology
still require review.

## x-anchor

`M1009-X-ANCHOR` points to the immutable anchor audit. The independent and
Levy Borel-Cantelli results remain infrastructure only and receive no root
proof credit.

## x-tcb

`M1009-X-TCB` owns the Lean kernel, pinned dependency, axiom, artifact, and
replay boundary. Release-grade closure is outside this phase.

## d-readable

`M1009-D-READABLE` requires a public reconstruction linked to every semantic
leaf, including imported mathematical bridges.

## w-validate

`M1009-W-VALIDATE` owns node-scoped exact-type, placeholder, axiom,
provenance, composition, and freshness recipes.

## Status boundary

The registry records no closed obligation. The frozen proof cut set is
`L-SECOND-MOMENT`, `L-TAIL`, `L-RATIO`, and `L-CONTINUITY`; each budget is at
most 100 substantive steps. This phase grants no proof, H0, readable-review,
trust, audit-completion, theorem-completion, release, or master-acceptance
credit.
