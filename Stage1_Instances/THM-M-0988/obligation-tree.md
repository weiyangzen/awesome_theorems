# THM-M-0988 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 18 canonical obligations before the proof phase assigns closure credit.
Sixteen are root-relevant machine obligations; `X-SOURCE` and `X-TCB` are informational overlays.
All 18 require readable coverage. No obligation is excluded merely because pinned mathlib already
contains an exact theorem. Any correction, split, merge, eligibility, exclusion, or risk change
requires registry version 2 and an append-only delta.

## Typed proof route

```text
M0988-ROOT  exact frozen iid CLT [open M1]
`-- M0988-T-ASSEMBLE  checked conditional composition
    `-- M0988-X-PINNED  exact pinned terminal theorem bridge [open]
        |-- M0988-B-ZERO  variance = 0
        |   `-- M0988-C-DEGENERATE  almost-sure constant route
        `-- M0988-B-NONZERO  variance != 0
            |-- M0988-N-CENTER / M0988-N-SCALE
            |-- M0988-C-STANDARD
            |   |-- M0988-L-MOMENTS
            |   |-- M0988-L-IID
            |   `-- M0988-L-CHARFUN
            `-- M0988-L-TRANSPORT
```

## root

`M0988-ROOT` is the universally quantified proposition from `Statement.lean`, including independent
source and target probability spaces, finite second moment, iid hypotheses, centered `sqrt n`
normalization, and the Gaussian law with variance `Var[X 0; P]`.

## s-exact

`M0988-S-EXACT` owns the exact universes, binders, typeclasses, hypotheses, and conclusion. It rules
out standard-normal-only, triangular-array, finite-iid, and nonzero-variance substitutions.

## s-boundary

`M0988-S-BOUNDARY` retains both variance branches. At `n = 0`, Lean's totalized inverse makes the
term defined; changing or deleting that first value is not needed for convergence along `atTop`.

## s-foundation

`M0988-S-FOUNDATION` owns the kernel and axiom policy. The anchor observed `propext`,
`Classical.choice`, and `Quot.sound`; the transitive release audit remains open.

## n-center

`M0988-N-CENTER` isolates centering by the common expectation, including integrability and the use
of identical distribution to identify coordinate expectations.

## n-scale

`M0988-N-SCALE` owns division by `sqrt Var[X 0; P]` in the nonzero branch and the algebra needed to
relate `sqrt (n * variance)` to the requested normalization.

## b-zero

`M0988-B-ZERO` is the explicit `variance = 0` branch. It must show every coordinate is almost surely
the common expectation, hence every centered normalized sum has the degenerate zero law.

## b-nonzero

`M0988-B-NONZERO` is the complementary branch. It standardizes the summands, applies the unit
variance CLT, and scales the limit back. Together the two branches are exhaustive.

## c-degenerate

`M0988-C-DEGENERATE` constructs the zero-law convergence through
`tendstoInDistribution_of_identDistrib` and identifies the target Gaussian when variance is zero.

## c-standard

`M0988-C-STANDARD` constructs `(X k - E[X 0]) / sqrt Var[X 0; P]` and the correspondingly divided
target variable. Its moment, iid, and Gaussian-law invariants are material obligations.

## l-moments

`M0988-L-MOMENTS` supplies integrability, zero mean, and unit second moment for the standardized
reference summand, using the finite-second-moment premise and nonzero variance.

## l-iid

`M0988-L-IID` transports family independence and identical distribution through the common affine
normalization map.

## l-charfun

`M0988-L-CHARFUN` owns the unit-variance characteristic-function CLT and its Levy-convergence
boundary. A short invocation remains a substantive imported bridge, not a primitive citation.

## l-transport

`M0988-L-TRANSPORT` applies continuous multiplication by `sqrt variance` and verifies both the
random-variable expression and Gaussian-law target after scaling back.

## x-pinned

`M0988-X-PINNED` is the exact pinned declaration
`ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub` at mathlib revision `8a178386`.
It is one canonical terminal body; legacy and external aliases cannot add duplicate proof credit.

## t-assemble

`M0988-T-ASSEMBLE` is checked by `ObligationTree.root_compose`. It consumes the exact bridge premise
and returns the exact root, but does not prove that premise in this phase.

## x-source

`M0988-X-SOURCE` remains `H2`: exact primary-source edition, theorem/page, assumptions, errata, and
independent review have not yet been accepted.

## x-tcb

`M0988-X-TCB` remains open for transitive declaration, compiled-artifact, executable, axiom,
reproducibility, and independent-verification closure.

## Graph and status boundary

Proof requirements have reciprocal `composes` edges. Refinement, provenance, evidence, trust,
documentation, and workflow are separate typed graphs. Every semantic leaf has a substantive
ledger and budget at most 100. The frozen root cut set is `M0988-X-PINNED`; this phase deliberately
records no closed obligation and claims no proof acceptance, H0, R0, audit completion, theorem
completion, release readiness, or master acceptance.
