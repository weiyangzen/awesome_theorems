# Scope map

## Included topic boundary

- A source-selected Frege proof system, including propositional syntax, inference rules or checker,
  and the presentation-invariance boundary.
- A precisely encoded family of tautologies and its size parameter.
- Frege proof size under a fixed encoding and a precise lower-bound function.
- Every soundness, completeness, explicitness, uniformity, constructibility, and asymptotic
  hypothesis required by the selected result.

## Ambiguities to resolve at statement freeze

1. **System strength:** unrestricted Frege, bounded-depth Frege (including the depth and connective
   basis), intuitionistic Frege, or another restricted variant.
2. **Presentation:** Hilbert rules, sequent-style presentation, lines versus trees/DAGs, permitted
   abbreviations, and the simulation used to compare presentations.
3. **Hard family:** pigeonhole, parity/counting, clique/coloring, or another named or existential
   family of tautologies.
4. **Measure:** lines, symbols, encoded bits, depth, or another proof-size parameter.
5. **Rate and quantifiers:** polynomial, superpolynomial, exponential, or a concrete function;
   pointwise, eventual, infinitely often, or worst-case.
6. **Historical identity:** the year 1985 and Razborov attribution must be checked against an exact
   source rather than used to infer a Frege theorem.

## Explicit exclusions

- A circuit lower bound, monotone-circuit lower bound, or resolution lower bound as a substitute.
- A bounded-depth or otherwise restricted Frege result presented as unrestricted Frege.
- An open lower-bound problem for a strong Frege system presented as an established theorem.
- A generic counting argument or an assumed `LowerBound` predicate repackaged as the result.
- Upper bounds, automatability, proof-search runtime, or extended Frege properties.
- The separate catalog targets for generic proof-complexity lower bounds or extended Frege.
- The repository label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake because the source record does not identify one.
