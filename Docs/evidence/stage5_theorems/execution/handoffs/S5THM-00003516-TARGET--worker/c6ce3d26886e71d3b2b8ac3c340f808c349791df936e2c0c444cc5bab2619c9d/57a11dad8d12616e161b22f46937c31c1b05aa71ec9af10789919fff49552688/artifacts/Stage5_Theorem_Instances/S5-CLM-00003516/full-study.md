# Full study — cubic finite additive convolution

The frozen declaration asks whether the reciprocal of the root interaction
functional `Φ` is superadditive for the finite additive convolution of two
monic real-rooted cubics. The source file is pinned exactly, but the source
proof is `sorry`; this package therefore treats it only as a statement oracle
and gives an independent reduction.

Translation of every root does not change the pairwise differences occurring
in `Φ`. Center a monic real-rooted cubic. In invariant coordinates it is

`f(x) = x^3 - 3 a x - u`, with `a ≥ 0` and `u^2 ≤ 4 a^3`.

The inequality is the discriminant condition for three real roots. Direct
expansion of the definition of degree-three finite additive convolution shows
that the centered invariants add:

`(a,u) ⊞ (b,v) = (a+b,u+v)`.

For distinct roots, a common-denominator calculation in the definition of
`Φ` gives

`1/Φ(f) = (4 a^3-u^2)/(6 a^2)`.

Thus the theorem becomes a rational inequality in four real variables. After
clearing nonnegative denominators its only nontrivial component is weighted
Cauchy:

`a*b*(u+v)^2 ≤ (a+b)*(b*u^2+a*v^2)`.

The gap is the square `(b*u-a*v)^2`. This exact identity is the root proved in
all three Lean surfaces. The repeated-root boundary is not discarded: there
`Φ = ⊤` by definition, reciprocal terms become zero, and the same conclusion
follows by the equality/continuity boundary of the discriminant region.

No provider proof body, claim-specific axiom, local definition, notation,
macro, coercion, namespace alias, unsafe declaration, or placeholder enters
the proof. The numeric provider module and qualified declaration are retained
verbatim in provenance comments because that numeric path is not a canonical
Lake import. The canonical Master must recompute elaborated semantic identity,
complete the exact source-to-target transport, and compile at trust zero.

The structured DAG and the readability ledger contain the exhaustive
hypotheses, inferences, outputs, anchors, downstream uses, exceptional cases,
and trust boundaries. This prose intentionally does not duplicate those
inventories.
