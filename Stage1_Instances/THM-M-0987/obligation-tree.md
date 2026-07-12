# THM-M-0987 frozen obligation architecture

Item: `S56-M-0987-OBLIGATION_TREE`

Registry version 1 freezes 20 semantic obligations for the exact real-valued iid finite-second-moment CLT. Eligibility was fixed from the statement and audited mathlib body before proof-phase credit. The checked Lean interface only transports an explicit exact bridge premise to the canonical root.

## Typed proof route

```text
M0987-ROOT exact canonical proposition
`-- M0987-T-ASSEMBLE checked conditional transport
    `-- M0987-X-PINNED exact pinned theorem boundary
        `-- M0987-B-MERGE variance split
            |-- M0987-B-ZERO degenerate Gaussian branch
            `-- M0987-B-NONZERO standardized branch
                |-- M0987-N-CENTER
                |-- M0987-N-STANDARDIZE
                |-- M0987-L-GAUSSIAN
                `-- M0987-L-LEVY
                    |-- M0987-L-CHARFUN-SUM
                    `-- M0987-L-POWER-LIMIT
                        `-- M0987-L-TAYLOR
```

The statement layer separately freezes definitions, universe/typeclass context, boundary cases, the checked source-shape transport, and foundation policy. `M0987-X-SOURCE` is a human-source boundary; `M0987-X-PROVENANCE` is a release overlay. Typed source, provenance, trust, documentation, and workflow edges cannot count as proof premises.

## Node ledger

Each heading below is the stable readable anchor recorded by the graph. All nodes remain `H2/R4`; only statement interfaces and the conditional final transport have provisional `M0-L` evidence. The root remains `M3`.

### m0987-root
Exact `CentralLimitTheoremTarget`; no inhabitant is installed.

### m0987-s-defs
Canonical probability, moment, Gaussian, finite-sum, and convergence definitions.

### m0987-s-context
Exact ordered universes, measurable spaces, probability measures, and real observation binders.

### m0987-s-boundary
The `n = 0`, zero-variance, and nonzero-variance cases, with no strengthened assumptions.

### m0987-s-transport
Checked equivalence with the local transcription of the pinned theorem type.

### m0987-s-foundation
Future transitive axiom, kernel, computation, and TCB acceptance certificate.

### m0987-n-center
Center the iid observations by their common expectation.

### m0987-n-standardize
For nonzero variance, scale centered observations to variance one.

### m0987-b-zero
Use variance zero to obtain almost-everywhere constant observations and the degenerate Gaussian limit.

### m0987-b-nonzero
Apply the standardized CLT and scale the limit back to variance `Var[X 0; P]`.

### m0987-b-merge
Exhaust and recompose the equality/inequality split on the variance.

### m0987-l-charfun-sum
Factor the characteristic function of an independent finite sum.

### m0987-l-taylor
Supply the second-order characteristic-function expansion at zero.

### m0987-l-power-limit
Derive convergence of nth powers to `exp (-t^2/2)`.

### m0987-l-levy
Convert characteristic-function convergence to convergence in distribution.

### m0987-l-gaussian
Identify and scale the Gaussian characteristic function.

### m0987-x-pinned
Exact imported `tendstoInDistribution_inv_sqrt_mul_sum_sub` proof boundary. This is the remaining root cut set and receives no proof credit in this phase.

### m0987-t-assemble
Checked conditional transport from the exact bridge premise to the canonical root.

### m0987-x-source
Pending pinpoint primary-source mapping; human-source only.

### m0987-x-provenance
Pending transitive body, dependency, axiom, TCB, license, and replay closure; release-only overlay.

## Freeze boundary

The registry hash fixes inventory and eligibility. Any correction, split, merge, exclusion, or weight change requires registry version 2 and an append-only delta. This phase does not apply the mathlib theorem, close the root, accept full provenance or trust, establish H0/R0, complete the audit, or complete the theorem.
