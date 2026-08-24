# Full study: Erdős Problem 1047

## Frozen statement

The claim asks whether every component of a sufficiently small polynomial sublevel set is convex when the number of components equals the number of distinct roots. Its frozen answer is false. The exact provider declaration is `Erdos1047.erdos_1047` at revision `2270d31e8dd611521f979de6d86da364930b7669`; the durable downstream alias is `S6-CLM-00006497` / `S6-VAR-00006437`.

## Construction and hypotheses

The witness polynomial is `X^6-X`, the threshold is `0.582`, and the claimed root/component count is six. Monicity follows from the leading term. Root distinctness follows by factoring into `X(X^5-1)` and using separability; the exceptional case that zero might also root `X^5-1` is discharged by direct evaluation. Positivity of the threshold is numeric.

## Separation argument

For radius `(1/6)^(1/5)`, a reverse-triangle estimate gives a modulus strictly above the threshold. A corresponding bound holds on five symmetry-related rays. These barriers leave an inner disk and five angular sectors. The sublevel set is contained in their union; the regions are open and pairwise disjoint. Every connected component containing a root is contained in one region, while each region contains its assigned root. This gives injectivity and surjectivity of the six root components.

## Failure of convexity

The zero component contains a real radial point and its rotation by `2π/5`, because both radial segments stay in the sublevel set. Direct certified arithmetic shows their midpoint has polynomial modulus above `0.582`. Convexity would place the midpoint in the component and therefore in the sublevel set, contradicting that calculation.

## Composition, outputs, and downstream use

The construction produces all hypotheses of the universal proposition and a component violating its output. It therefore refutes the proposition and closes the biconditional with `answer(False)`. The Stage6 alias may use the theorem only after Master verifies exact semantic binding, trust-zero elaboration, current trace, empty H/M/R cuts, and strict dominance.

## Exceptional cases and trust boundary

Boundary equality on the separating circle and rays is handled explicitly by strict modulus bounds. Argument discontinuity on the negative real axis is isolated in the sector proof. The provider declaration itself is admitted and is never used as proof authority. Worker-produced hashes and audits are proposals; the Lean kernel establishes local closure, and the canonical Master alone accepts integration.
