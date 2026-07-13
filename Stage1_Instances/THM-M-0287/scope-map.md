# Scope map

## Preserved theorem family

The intake preserves the classical measure-theoretic Lusin family relating measurable functions
to continuity outside an arbitrarily small exceptional set. It does not choose a canonical
proposition. Candidate readings, none credited as the repository target, include:

- Lusin's printed 1912 interval statement: a measurable real-valued function on `[0,1]` restricts
  continuously to a perfect nowhere-dense set of Lebesgue measure greater than `1 - epsilon`;
- a finite-measure or finite-on-a-measurable-set theorem producing a large closed subset;
- a Radon or Polish-space form producing a large compact subset on which `ContinuousOn f K`;
- a form producing a globally continuous function `g` agreeing with `f` outside a set of measure
  less than epsilon; and
- an almost-everywhere measurable or separable metric-valued generalization.

## Decisions required at statement freeze

1. Select and preserve a lawful immutable primary-source edition and exact theorem passage, then
   map incorporated definitions, assumptions, proof boundary, translation, corrections or errata,
   and independent review.
2. Decide whether the root is the historical interval theorem or a source-selected generalization;
   a modern textbook statement cannot silently replace the catalog's 1912 attribution.
3. Fix the domain: `[0,1]`, a measurable subset, a finite-measure space, or a topological measure
   space; also fix the topology, measurable space, and regularity, separation, compactness, and
   countability assumptions.
4. Fix the codomain and measurability notion: real, extended real, or metric-valued; pointwise
   measurable, Borel-measurable, strongly measurable, or almost-everywhere measurable.
5. Fix the exact output: perfect/closed/compact set, relative continuity or `ContinuousOn`, or a
   global continuous representative; specify pointwise versus almost-everywhere agreement.
6. Fix the epsilon type, positivity and strictness, measure orientation, set-difference/complement
   convention, ordered binders, implicit instances, and the treatment of null or infinite values.

## Boundary and degenerate cases

No case is excluded before the proposition is selected. The statement phase must decide empty and
null domains, zero measure, infinite total measure, epsilon at zero or above the total mass,
functions infinite on a null set, nonmeasurable domains, non-Hausdorff spaces, nonseparable
codomains, and whether the selected large set may be empty, all of the domain, or required to be
nowhere dense.

## Explicit exclusions

- Egorov's theorem about almost-everywhere versus almost-uniform convergence.
- Lusin separation and Lusin-Souslin image/measurable-embedding theorems from descriptive set
  theory.
- Density of continuous functions in `L^p`, approximation in norm or measure, simple-function
  approximation, or measure regularity alone.
- The polynomial-series and almost-everywhere primitive theorems that also appear in Lusin's 1912
  note.
- A structure, hypothesis, axiom, proxy predicate, or global continuous function that assumes the
  desired conclusion.
- The catalog's `已验证` label, a title match, source URL, bounded search, or API probe as proof.

## Pinned Lean boundary

At the pinned mathlib revision, `Measurable.exists_continuous` changes the source topology to make
a Borel-measurable map continuous; it is not a large-measure restriction theorem.
`MeasurableSet.exists_isCompact_diff_lt` provides compact inner regularity but says nothing about
continuity of a measurable function. `Continuous.measurable` supplies only the reverse elementary
direction, and `ContinuousMap.toAEEqFun` maps continuous functions into an almost-everywhere class.
The bounded exact-topic search found no usual measure-theoretic Lusin declaration. These are
discovery-only substrates and do not move the root above `M4`.
