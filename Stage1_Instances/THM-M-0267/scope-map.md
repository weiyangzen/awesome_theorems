# Scope map

## Received claim

`Docs/researches/math_theorems.md:1922-1927` fixes only `阿尔泽拉-阿斯科利定理`, the
attribution Cesare Arzela/Giulio Ascoli, the year 1889, and `函数列紧性的判别准则` ("a
criterion for compactness of sequences of functions"). It supplies no primary citation,
definitions, assumptions, theorem locator, proof boundary, or exact formal artifact.

The words "sequence" and "criterion" do not decide whether the root is a subsequence-extraction
theorem, relative compactness of an arbitrary family, a compactness implication, or an if-and-only-
if characterization. This intake does not choose among them.

## Candidate classical boundary

A familiar scalar sequential form says that a uniformly bounded equicontinuous sequence of
continuous real-valued functions on a compact metric space has a uniformly convergent subsequence.
A more general family form characterizes relative compactness through equicontinuity and pointwise
relative compactness. These are candidate boundaries only, not frozen claims.

The statement phase must source and fix:

- compact metric, compact Hausdorff, locally compact, or another domain;
- scalar, metric, normed, or uniform codomain, including separation and completeness assumptions;
- natural-number sequence versus arbitrary family or set of functions;
- continuous maps, bounded continuous maps, or another carrier;
- uniform, compact-open, uniform-on-compacts, pointwise, or sequential convergence topology;
- uniform boundedness, one common compact range, or pointwise relative compactness;
- pointwise or uniform equicontinuity and the exact quantifier order;
- closedness of the family, compactness of the family or its closure, total boundedness, or
  extraction of a convergent subsequence; and
- sufficiency, necessity, or both directions.

## Pinned Lean candidate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Topology.ContinuousMap.Bounded.ArzelaAscoli` supplies three bounded-continuous-function
forms. The main `BoundedContinuousFunction.arzela_ascoli` concludes compactness of `closure A`
from equicontinuity and a common compact range. The variants `arzela_ascoli₁` and
`arzela_ascoli₂` instead take closedness and conclude compactness of `A`.

Module `Mathlib.Topology.UniformSpace.Ascoli` supplies a general uniform-on-compact framework,
including `ArzelaAscoli.compactSpace_of_isClosedEmbedding`,
`ArzelaAscoli.isCompact_closure_of_isClosedEmbedding`, and
`ArzelaAscoli.isCompact_of_equicontinuous`. The last assumes compactness of the pointwise image and
equicontinuity and concludes compactness in the continuous-map topology. Its file-level TODO says
the converse compact-implies-equicontinuous theorem remains to be proved there.

These are strong exact-topic interfaces, hence provisional `M3`, but none receives root identity,
proof-body, or completion credit at intake.

## Boundary cases to resolve

- Empty domain, empty family, singleton family, or empty family of compact subsets.
- Non-Hausdorff codomain, pseudo-metric points at zero distance, or incomplete codomain.
- A nonclosed family, where compactness of the family and compactness of its closure differ.
- Pointwise compact ranges that do not lie in one common compact subset.
- Compactness versus sequential compactness in a nonmetrizable function space.
- Loss of a boundedness or compact-range hypothesis, failure of equicontinuity at one point, and a
  pointwise limit which is not continuous.

No boundary case is silently excluded before an exact proposition is selected.

## Explicit exclusions

- Dini, Stone-Weierstrass, Banach-Alaoglu, Rellich-Kondrachov, Aubin-Lions, Montel, Prokhorov, or
  Helly selection substituted for Arzela-Ascoli.
- A finite family, finite domain, compact codomain alone, or constant-function toy case.
- A structure or premise which already stores a convergent subsequence or compact closure.
- One pinned declaration selected solely because its name contains `arzela_ascoli`.
- The catalog's untrusted `已验证` label, a URL, or the intake API probe used as proof credit.

## Statement retry condition

An independent source reviewer must admit an immutable primary edition and exact result locator,
map every incorporated definition, ordered binder, premise, conclusion, direction, proof boundary,
translation, correction, and historical attribution, and approve one source-to-Lean root. The
statement phase may then elaborate that root with minimal imports, fingerprint it, compile checked
transports, and run the required domain, hypothesis, binder-scope, and boundary mutations.
