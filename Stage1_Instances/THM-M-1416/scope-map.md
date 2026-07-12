# Scope map

## Catalog scope preserved

- Target identity: `THM-M-1416`, named `Bowen-Margulis测度` (Bowen-Margulis measure).
- Subject boundary: a measure associated with hyperbolic dynamics.
- Catalog attribution and date: Rufus Bowen / Grigory Margulis, 1970.
- Literal catalog gloss: `双曲系统的测度` ("measure of/for hyperbolic systems").

This is all the mathematical scope fixed by the repository. An object name and a field gloss do not
determine a theorem. In particular, intake does not expand the name into an existence-and-uniqueness
claim from memory.

## Decisions required before statement freeze

| Surface | Unresolved decision | Why it changes the proposition |
|---|---|---|
| Root kind | definition/construction, existence, uniqueness, maximal entropy, ergodicity, mixing, support, or equidistribution | These have different conclusions and proof obligations |
| System | geodesic flow, Anosov flow, Anosov diffeomorphism, basic Axiom A set, suspension, symbolic system, or another hyperbolic model | The phase space, time action, and hypotheses differ |
| Geometry | compact negatively curved manifold, pinched variable curvature, CAT(-1)/proper hyperbolic space quotient, or no geometric model | Boundary, curvature, properness, and quotient assumptions are substantive |
| Dynamics | discrete map versus continuous flow; invertibility; topological mixing versus transitivity versus nonwandering restriction | Invariance, uniqueness, and mixing conclusions need different premises |
| Hyperbolicity | uniform splitting, Axiom A/basic-set formulation, expansivity/specification, or symbolic coding assumptions | None follows from the word "hyperbolic" alone |
| Measure | finite Borel/Radon measure, invariant probability measure, measure class, or locally finite lift | Normalization, descent, finiteness, and target types differ |
| Construction | Patterson-Sullivan boundary density, stable/unstable conditional measures, Markov coding, periodic-orbit limit, or variational characterization | Construction equivalence is theorem-level mathematics |
| Entropy | topological entropy, measure-theoretic entropy, pressure/equilibrium state, and chosen normalization | "Measure of maximal entropy" needs exact entropy APIs and equality/supremum conventions |
| Edge cases | empty basic set, zero entropy, noncompact/infinite measure, multiple components, arithmetic length spectrum, exceptional orbits | Each can change existence, uniqueness, or mixing claims |

An approved source correction must freeze all domains and universes, ordered binders, hypotheses,
conclusion, regularity and compactness assumptions, normalization, and exceptional cases before the
statement phase elaborates any Lean expression.

## Candidate families not credited

- Existence and uniqueness of a measure of maximal entropy for a topologically mixing Axiom A
  system or basic hyperbolic set.
- Construction of a geodesic-flow invariant measure from a Patterson-Sullivan density.
- Ergodicity, mixing, Bernoulli properties, full support, or entropy characterization of a
  source-specified Bowen-Margulis measure.
- Weak-star equidistribution of weighted or unweighted periodic-orbit measures.
- Identification of symbolic and geometric constructions under a coding map.

No family in this list is selected, stated, or credited at intake.

## Explicit exclusions

- Hyperbolic dynamical systems (`THM-M-1411`), Anosov diffeomorphisms (`THM-M-1412`), Axiom A
  systems (`THM-M-1413`), spectral decomposition (`THM-M-1414`), and Markov partitions
  (`THM-M-1415`) are neighboring roots, not substitutes.
- SRB measures (`THM-M-1417`), Lyapunov exponents (`THM-M-1418`), Oseledets' theorem
  (`THM-M-1419`), Pesin theory (`THM-M-1420`), and Pesin's entropy formula (`THM-M-1421`) are
  separately scheduled.
- Topological entropy (`THM-M-1403`), measure-theoretic entropy (`THM-M-1404`), and the variational
  principle are ingredients or related claims, not the Bowen-Margulis target by themselves.
- A generic invariant probability measure, a Dirac measure on a fixed orbit, or a structure that
  assumes the desired invariance, maximality, uniqueness, or mixing conclusion as a field cannot
  identify or close this target.
- The untrusted catalog label `已验证` supplies neither human-source nor Lean kernel evidence.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib exposes general measures, probability
measures, measure-preserving and ergodic maps, flows, and Bowen-Dinaburg topological cover entropy.
The intake-only bounded search found no Bowen-Margulis, maximal-entropy-measure, Patterson-Sullivan,
or geodesic-flow target declaration. These are substrate and discovery facts only, not a complete
anchor audit, statement elaboration, or proof.
