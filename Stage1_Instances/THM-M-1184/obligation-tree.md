# THM-M-1184 obligation tree

This is the frozen version-1 architecture for the exact compact-metric,
continuous real-cost statement in `Statement.lean`. It does not claim either
inequality package or the root theorem.

The proof route has two root branches. The weak branch integrates the
pointwise potential constraint against a coupling, rewrites through both
marginals, and lifts the result through `sSup` and `sInf`. The strong branch
uses compact convex separation, extracts continuous coordinate potentials,
proves the no-gap approximation lemma, and passes to the reverse inequality.
`root_of_duality_packages` kernel-checks that these two exact uniform
interfaces compose by antisymmetry into the canonical target.

The machine-readable authority is `obligation-registry.json`; all proof,
refinement, provenance, evidence, trust, documentation, and workflow edges are
in `typed-graphs.json`. Every leaf has a semantic ledger and a budget at most
100. The bridge labels do not conceal proof credit: separation, marginal
integration, potential extraction, and the order-limit passage remain distinct
open obligations.

## M1184-ROOT

Root vector: `[H3, M2, R4]`. Minimal open root cut sets include the weak
package and the strong package. Source review, trust closure, and independent
readability review also remain open release boundaries.

## Status boundary

The conditional composition is not a Kantorovich-duality proof. No H0, R0,
M0, audit completion, theorem completion, or release credit is asserted.
