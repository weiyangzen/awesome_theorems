# THM-M-0990 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 18 canonical obligations before proof work receives closure credit.
Sixteen are root-relevant machine obligations; `X-SOURCE` and `X-TCB` are informational overlays.
All 18 require readable coverage, and no obligation is excluded. The registry is pinned to the
statement and anchor-audit artifact hashes. Any correction, split, merge, eligibility, exclusion,
or risk change requires registry version 2 with an append-only old/new ID delta.

## Typed proof route

```text
M0990-ROOT [open M3]
`-- M0990-T-ASSEMBLE [checked conditional composition]
    `-- M0990-T-TRIANGULAR-BRIDGE [open]
        |-- M0990-N-CENTER / M0990-N-VARIANCE
        |-- M0990-L-MOMENT-TRANSPORT / M0990-L-INDEPENDENCE
        |-- M0990-L-LYAPUNOV-INF
        |-- M0990-L-CHARFUN-ENTRY
        |-- M0990-L-CHARFUN-PRODUCT
        |-- M0990-L-PRODUCT-LIMIT
        |-- M0990-L-LEVY
        `-- M0990-L-GAUSSIAN
```

## root

`M0990-ROOT` owns the universally quantified proposition in `Statement.lean`: a real-valued
triangular array with joint independence within each row, explicit second and `2 + delta` moments,
eventual positive row variance, the Lyapunov ratio limit, and convergence of normalized centered
row sums to a variable with standard Gaussian law.

## s-exact

`M0990-S-EXACT` preserves every universe, measure and probability instance, binder, hypothesis,
and conclusion. It forbids replacement by the iid CLT, pairwise independence, fixed row length,
variance-sum rather than square-root normalization, or a theorem assuming the desired bridge.

## s-boundary

`M0990-S-BOUNDARY` records that natural-number rows include zero and Lean inverses are totalized.
The positivity hypothesis is only eventual, so the proof must move to an `atTop` tail rather than
silently strengthen positivity to every row.

## s-foundation

`M0990-S-FOUNDATION` owns the classical, noncomputable, kernel, dependency, and axiom boundary.
The conditional composition probe reports `propext`, `Classical.choice`, and `Quot.sound`; full
transitive trust closure remains for validation and release.

## n-center

`M0990-N-CENTER` must show each `centered P X n k` has expectation zero and connect the frozen
definition with the characteristic-function lemmas without changing integrability assumptions.

## n-variance

`M0990-N-VARIANCE` identifies the variance sum after centering and proves total normalized row
variance one on the eventual positive tail. It owns square-root and real-power side conditions.

## l-moment-transport

`M0990-L-MOMENT-TRANSPORT` transports `MemLp 2` and the explicit centered `2 + delta` integrability
through row scaling, producing all finite moments needed by the Taylor estimates.

## l-independence

`M0990-L-INDEPENDENCE` restricts whole-row `iIndepFun` to `range n` and transports independence
through centering and multiplication by the common row scale inverse.

## l-lyapunov-inf

`M0990-L-LYAPUNOV-INF` derives infinitesimality and summed Taylor-remainder control from the exact
Lyapunov ratio. This is a substantive analytic leaf, not a synonym for the input limit.

## l-charfun-entry

`M0990-L-CHARFUN-ENTRY` establishes a second-order characteristic-function expansion for each
normalized entry, with a quantitative `2 + delta` remainder suitable for summing across a row.

## l-charfun-product

`M0990-L-CHARFUN-PRODUCT` uses finite-row independence to factor the characteristic function of
the normalized row sum into the product of entry characteristic functions.

## l-product-limit

`M0990-L-PRODUCT-LIMIT` combines unit total variance, infinitesimality, and remainder control to
prove convergence of the row products to `exp (-t^2 / 2)` for every real frequency.

## l-levy

`M0990-L-LEVY` converts pointwise characteristic-function convergence into convergence in
distribution using the pinned Levy continuity infrastructure. The imported theorem remains a
substantive bridge and receives no closure credit here.

## l-gaussian

`M0990-L-GAUSSIAN` identifies the limiting characteristic function and transports the result to
the exact target variable `Y` through its `HasLaw Y (gaussianReal 0 1) P'` hypothesis.

## t-triangular-bridge

`M0990-T-TRIANGULAR-BRIDGE` is the missing terminal proof body assembling the triangular-array
argument. The anchor audit located no exact pinned Lean declaration, so this node has no terminal
body ID and is the frozen remaining root cut set.

## t-assemble

`M0990-T-ASSEMBLE` is checked by `ObligationTree.root_compose`. It consumes the exact bridge-shaped
root premise and returns the root, but deliberately does not manufacture that premise.

## x-source

`M0990-X-SOURCE` remains `H2`: exact primary edition, theorem/page, conventions, assumptions,
errata, node crosswalk, and independent review remain open.

## x-tcb

`M0990-X-TCB` remains open for transitive declarations, artifacts, executables, axioms, offline
replay, reproducibility, freshness, and independent verification.

## Graph and status boundary

Proof requirements have reciprocal `composes` edges. Refinement, provenance, evidence, trust,
documentation, and workflow are separate typed graphs. Every semantic leaf has a substantive
ledger and a step budget at most 100. The root remains `M3`, with cut set
`M0990-T-TRIANGULAR-BRIDGE`. This architecture phase records no closed obligation and claims no
proof acceptance, H0, R0, audit completion, theorem completion, or release readiness.
