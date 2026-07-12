# THM-M-1036 frozen obligation architecture

Registry version 1 freezes 18 semantic obligations before proof work. Machine,
human-source, and readable denominators are serialized in
`obligation-registry.json`; reciprocal typed edges and full node records are in
`typed-graphs.json`. All nodes remain root-relevant. Source and provenance
overlays cannot earn machine-proof credit.

## Proof spine

The root consumes two exact packages through the kernel-checked
`root_of_existence_and_uniqueness` composition. Existence follows the standard
Picard route: construct iterates, preserve analytic invariants, prove the
successive-difference estimate, obtain convergence, and pass both integrals to
the limit. Uniqueness derives a two-solution estimate, applies Gronwall, and
uses path continuity to upgrade timewise equality to indistinguishability.

## Node ledger

Each heading below is the stable public target referenced by the structured
node. Exact planned signatures, outputs, debts, owners, validation recipes, and
status boundaries live in `typed-graphs.json`.

### m1036-root
Exact canonical target; open.
### m1036-s-definitions
Frozen Lean vocabulary; elaborated, but not a proof.
### m1036-s-boundary
Positive horizon, endpoints, zero dimensions, and equality convention.
### m1036-s-foundation
Kernel, imports, axioms, classical policy, and trust closure.
### m1036-x-integral-semantics
Standard time/Ito integral construction and checked laws.
### m1036-c-picard
Picard iterate construction.
### m1036-l-picard-invariants
Adaptedness, measurability, continuity, and integrability invariants.
### m1036-l-picard-estimate
Successive-iterate quantitative estimate.
### m1036-l-picard-convergence
Process-space and pathwise convergence.
### m1036-c-limit-solution
Limit passage and `StrongSolution` construction.
### m1036-l-uniqueness-estimate
Two-solution difference inequality.
### m1036-l-gronwall
Exact-domain Gronwall bridge.
### m1036-l-indistinguishable
One-conull-event equality at every horizon time.
### m1036-t-existence
Complete strong-existence package.
### m1036-t-uniqueness
Complete pathwise-uniqueness package.
### m1036-t-assemble
Checked conditional composition into the exact root.
### m1036-x-source
Primary-source node crosswalk; no machine credit.
### m1036-x-provenance
Terminal-body and trust provenance; informational overlay only.

## Critical modeling boundary

The frozen `IntegralSemantics` structure exposes `standard_time_integral` and
`standard_ito_integral` merely as propositions; it contains no equations or
laws connecting those propositions to its two operations. Consequently no
standard integral theorem may be assumed from those fields. The
`M1036-X-INTEGRAL-SEMANTICS` bridge must provide a real construction and checked
transport. If that cannot inhabit the exact frozen target, the statement must
be versioned and re-fingerprinted rather than silently strengthened.

The root remains `[H2, M3, R3]`. This phase freezes architecture and a truthful
root cut set only; it does not prove existence, uniqueness, or theorem
completion.
