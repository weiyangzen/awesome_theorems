# Scope map

## Included topic boundary

- Infinite cardinals and a source-specified definition of measurable cardinal.
- Ultrafilters on a carrier of the relevant cardinality.
- The exact completeness, nonprincipality, uniformity, and measure conventions in the source.
- A concrete equivalence, existence claim, or consequence explicitly named by that source.

## Ambiguities to resolve at statement freeze

1. The standard characterization of an uncountable cardinal by a nonprincipal, kappa-complete
   ultrafilter on kappa.
2. An equivalence between that characterization and a nontrivial kappa-additive zero-one measure.
3. Ulam's consequence that a measurable cardinal is (strongly) inaccessible, or a related theorem.
4. An assertion that a measurable cardinal exists, which is a large-cardinal assumption rather
   than a theorem of the ordinary base theory.

The source must fix whether "kappa-complete" means closure under intersections indexed by sets of
cardinality strictly below kappa, and whether an ultrafilter is nonprincipal or uniform. It must
also fix universes, the representation of kappa by a type, boundary cardinals, and both directions
of any claimed equivalence.

## Explicit exclusions

- Measurability from measure theory or measurable functions/spaces.
- Mere existence of an ultrafilter, the ultrafilter lemma, or a principal ultrafilter.
- Strongly compact, supercompact, Woodin, inaccessible, or weakly compact cardinals as substitutes.
- Assuming a packaged `MeasurableCardinal` predicate and returning one of its fields tautologically.
- Treating the repository label `已验证`, the year, or attribution as statement/proof evidence.

No canonical Lean target is frozen at intake because the source record does not identify a unique
proposition.
