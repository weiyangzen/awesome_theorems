# THM-M-0996 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 19 canonical obligations before proof-phase closure
is observed. Sixteen are root-relevant machine obligations; the three `X`
records are assurance overlays and receive no proof credit. Every obligation
requires readable coverage. The canonical denominator digest is
`8d3affee638ef1cc6e3fbb2ee9d52fc76212b0a91327f7b42ecba1b4ae8b6e9e`.

The root and statement fingerprints bind the elaborated `Statement.lean`
source. Other signatures are explicitly `planned:v1`, so they remain open
until the proof phase freezes exact Lean declarations. Any correction, split,
merge, exclusion, or eligibility change requires registry version 2 and an
append-only delta.

## Typed proof route

```text
M0996-ROOT  exact Gaussian half-space enlargement comparison [M3]
`-- M0996-T-ASSEMBLE  checked conditional composition
    |-- M0996-L-HALFSPACE  exact half-space profile formula [open]
    |   |-- M0996-C-HALFSPACE  coordinate/thickening representation
    |   |   `-- M0996-N-COORD  orthonormal coordinate transport
    |   `-- M0996-N-PROFILE  frozen Gaussian profile
    `-- M0996-L-GENERAL  arbitrary measurable-set profile bound [open]
        |-- M0996-N-PROFILE
        `-- M0996-L-LIMIT  measurable-set approximation
            `-- M0996-L-INTERPOLATE  Gaussian comparison interpolation
                |-- M0996-L-GRADIENT  semigroup gradient estimate
                `-- M0996-C-SEMIGROUP  Ornstein-Uhlenbeck construction
```

`ObligationTree.lean` checks that the two central profile bounds really compose
to the exact target: it rewrites the half-space thickening, uses the declared
equal initial Gaussian measures, then applies the general-set bound. Both
central bounds are explicit premises. This is a composition certificate, not a
proof of either bound or of Gaussian isoperimetry.

The refinement graph separately records statement, boundary, transport,
foundation, normalization, and dimension-branch analysis. Provenance,
evidence, trust, documentation, and workflow graphs remain non-proof relations,
so an anchor name, source map, or task transition cannot close the root.

## Node ledgers

### m0996-root

Exact selected target from `Statement.lean`. It is open at M3 and requires the
terminal composition route; no root theorem was found in the pinned closure.

### m0996-s-exact

Freezes `stdGaussian`, measurable `A`, a unit-normal affine half-space `H`,
equal Gaussian mass, open `Metric.thickening`, and `0 < r`.

### m0996-s-boundary

Tracks positive radius, zero dimension, and mass endpoints. The equal-measure
half-space form avoids pretending that an inverse-CDF endpoint API is already
available.

### m0996-s-transport

Uses the checked iff `target_iff_expandedStatementShape`; it adds no theorem
content.

### m0996-s-foundation

Requires a later transitive axiom and TCB audit. The conditional harness reports
only `propext`, `Classical.choice`, and `Quot.sound`, but that report is not a
release trust closure.

### m0996-n-profile

Must define the mass-radius Gaussian profile with endpoint behavior. Its exact
formal signature remains planned.

### m0996-n-coord

Must combine the pinned standard-Gaussian coordinate transport with the metric
compatibility needed for thickenings. The existing anchor alone is insufficient.

### m0996-b-dim

Must show exhaustiveness and recomposition of the zero-dimensional vacuity and
positive-dimensional analytic branch.

### m0996-c-halfspace

Must identify a unit-normal affine half-space and its thickening with a
one-dimensional threshold calculation.

### m0996-c-semigroup

Must construct the finite-dimensional Ornstein-Uhlenbeck interpolation and
prove measure preservation and all regularity invariants used downstream.

### m0996-l-halfspace

Central open cut leaf: compute every positive thickening of an equal-mass
half-space in the frozen profile.

### m0996-l-gradient

Must prove the semigroup gradient estimate; it may not be hidden behind the
word "standard" or a broad opaque import.

### m0996-l-interpolate

Must turn the gradient estimate into the Gaussian comparison inequality for
regularized indicators.

### m0996-l-limit

Must pass from regularized objects to every measurable set while preserving
the open-thickening and measure inequality conventions.

### m0996-l-general

Central open cut leaf: prove the profile lower bound for arbitrary measurable
sets. It depends on the interpolation and limiting route above.

### m0996-t-assemble

Kernel-checked conditional composition in `target_of_profile_bounds`. The node
is M3 rather than M0 because its two required mathematical premises are open.

### m0996-x-anchors

Pins the audited Gaussian, coordinate, real-measure, and thickening declarations
as dependency provenance only.

### m0996-x-source

Requires pinpoint primary-source theorem/page, assumptions, errata, and a
node-by-node map. Current discovery citations do not clear H debt.

### m0996-x-tcb

Requires terminal-body provenance, dependency closure, foundation policy,
hermetic replay, and independent verification. It carries no proof credit.

## Status boundary

The remaining root cut set is `M0996-L-HALFSPACE` and `M0996-L-GENERAL`.
Neither is asserted. Exact proof bodies, source/readability acceptance, complete
trust and provenance, hermetic replay, independent review, `AUDIT-Z`,
`THEOREM-Z`, and master acceptance remain open.
