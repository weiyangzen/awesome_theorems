# THM-M-1177 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 21 root-relevant obligations against the exact statement and completed
anchor audit. Eighteen obligations form the machine denominator; the source, provenance, and TCB
surfaces are separately typed boundaries. Eligibility was fixed without treating nearby mathlib
ingredients as ABP closure. Any correction, split, merge, or eligibility change requires a
version-2 append-only delta.

## Typed proof route

```text
M1177-ROOT [open M4]
`-- M1177-T-ASSEMBLE [conditional composition checked]
    |-- M1177-B-SPLIT
    |-- M1177-B-DEGENERATE [open]
    `-- M1177-T-POSITIVE [open]
        |-- M1177-B-POSITIVE
        |-- M1177-L-SUP
        |   |-- M1177-L-SLOPE-BALL
        |   |   `-- M1177-C-CONTACT
        |   `-- M1177-L-BALL-VOLUME
        `-- M1177-L-INTEGRAL
            |-- M1177-L-GRADIENT-IMAGE
            |   `-- M1177-C-CONTACT
            |-- M1177-L-AREA
            |   `-- M1177-L-HESSIAN
            `-- M1177-L-OPERATOR
                |-- M1177-L-HESSIAN
                `-- M1177-L-DET-TRACE
```

## Node ledger

<a id="m1177-root"></a>
### M1177-ROOT
The root is exactly `AlexandrovBakelmanPucciTarget`, including the existential dimensional
constant, determinant weight, frozen upper contact set, sign convention, and all regularity and
integrability hypotheses. It remains `[H1, M4, R3]`.

<a id="m1177-s-data"></a>
### M1177-S-DATA
This interface owns the definitions and exact ordered premises. It prevents later proof work from
silently substituting a uniformly elliptic, viscosity, whole-domain, unit-ball, or sharp-constant
variant.

<a id="m1177-s-foundation"></a>
### M1177-S-FOUNDATION
This release boundary owns the selected classical foundation, derivative and integral APIs,
transitive axioms, and the prohibition on oracle or numerical evidence. It remains open.

<a id="m1177-b-split"></a>
### M1177-B-SPLIT
The proof splits exhaustively on `sSup (u '' Omega) <= 0`. This is a real branch because the frozen
statement permits empty domains and because the right-hand side's nonnegativity must be justified.

<a id="m1177-b-degenerate"></a>
### M1177-B-DEGENERATE
The nonpositive-maximum branch must derive the exact bound, including nonnegativity of diameter,
the dimensional constant, and the real-power weighted integral. It is not closed by the logical
case split alone.

<a id="m1177-b-positive"></a>
### M1177-B-POSITIVE
The positive branch owns all prerequisites for the geometric normal-map argument, without assuming
the desired estimate.

<a id="m1177-c-contact"></a>
### M1177-C-CONTACT
Construct affine upper supports and retain their touching points in the exact `upperContactSet`
defined in `Statement.lean`. Measurability and the relationship to a convex envelope must be made
explicit during implementation.

<a id="m1177-l-slope-ball"></a>
### M1177-L-SLOPE-BALL
Show that a Euclidean ball of slopes, with radius controlled by the positive maximum divided by the
domain diameter, is represented by supporting slopes. This owns the boundary geometry and bounded
domain argument.

<a id="m1177-l-gradient-image"></a>
### M1177-L-GRADIENT-IMAGE
At differentiability points, identify a supporting slope with the gradient and turn the slope-ball
inclusion into a gradient-image inclusion on the contact set.

<a id="m1177-l-area"></a>
### M1177-L-AREA
Control the measure of that image by the integral of `abs (det (D2 u))`. The audited Jacobian
theorems require injectivity, so noninjectivity or multiplicity is an explicit bridge obligation.

<a id="m1177-l-hessian"></a>
### M1177-L-HESSIAN
Prove that an upper-contact point has negative semidefinite Hessian under the frozen `ContDiffOn`
encoding. This supplies the sign condition needed by the determinant estimate.

<a id="m1177-l-det-trace"></a>
### M1177-L-DET-TRACE
For positive-definite `A` and negative-semidefinite `D2 u`, establish the exact determinant/trace
AM-GM inequality. The scalar `Real.geom_mean_le_arith_mean` anchor does not close this matrix bridge.

<a id="m1177-l-operator"></a>
### M1177-L-OPERATOR
Combine the matrix inequality with `trace (A * hessian u) >= f` and sign information at contact
points to bound the Hessian determinant by `(max (-f) 0)^n / det A`.

<a id="m1177-l-integral"></a>
### M1177-L-INTEGRAL
Integrate the pointwise bound on the measurable contact set and reconcile absolute determinants,
the frozen integrability premise, and the exact real-valued integral.

<a id="m1177-l-ball-volume"></a>
### M1177-L-BALL-VOLUME
Evaluate the slope-ball measure and isolate a nonnegative constant depending only on `n`, with
dimension zero excluded by the canonical binder.

<a id="m1177-l-sup"></a>
### M1177-L-SUP
Combine ball inclusion, image measure, determinant integration, and algebraic rearrangement to
obtain the positive supremum bound with the frozen `Real.rpow` normalization.

<a id="m1177-t-positive"></a>
### M1177-T-POSITIVE
This terminal package composes the contact construction and analytic leaves into the exact
positive-maximum interface. Every child remains open.

<a id="m1177-t-assemble"></a>
### M1177-T-ASSEMBLE
`ObligationTree.lean` kernel-checks that one constant satisfying both exhaustive branch packages
proves the exact root. This closes only conditional composition, not either branch.

<a id="m1177-x-source"></a>
### M1177-X-SOURCE
Primary editions, pinpoint premises, errata, and the node-by-node proof crosswalk remain at `H1` and
require independent review.

<a id="m1177-x-provenance"></a>
### M1177-X-PROVENANCE
This overlay owns terminal declaration bodies, imports, wrappers, aliases, evidence, and proof-body
deduplication. The prior component anchors have no root credit.

<a id="m1177-x-tcb"></a>
### M1177-X-TCB
This overlay owns transitive dependencies and axioms, reproducibility, freshness, invalidation,
revocation, and independent verification. It remains open.

## Status boundary

Every semantic ledger has an architectural budget at most 100, but no open mathematical node is
claimed proved or readable at `R0`. The minimal machine cut set after conditional composition is
`M1177-B-DEGENERATE` plus `M1177-T-POSITIVE`. This phase supplies no H0, M0 root, audit completion,
theorem completion, release evidence, or master acceptance.
