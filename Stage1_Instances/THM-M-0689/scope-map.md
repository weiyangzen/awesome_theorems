# Scope map

## Included topic boundary

- A source-selected propositional proof system with an explicit proof-checking relation.
- A precisely encoded family of tautologies or contradictions and its size parameter.
- Proof length/size under a fixed encoding and a precise lower-bound function.
- All uniformity, soundness, completeness, constructibility, and asymptotic hypotheses required by
  the selected theorem.

## Ambiguities to resolve at statement freeze

The repository record does not select any of the data that determines a proof-complexity theorem:

1. **Proof system:** resolution, Frege, bounded-depth Frege, extended Frege, cutting planes,
   polynomial calculus, or another Cook-Reckhow system.
2. **Hard family:** pigeonhole principles, Tseitin contradictions, clique/coloring formulas, random
   formulas, or another explicit or existential family.
3. **Measure:** number of lines, symbols, clauses, monomials, degree, width, or encoded bit length.
4. **Rate and quantifiers:** polynomial, superpolynomial, exponential, quasipolynomial, or a
   particular function; pointwise, infinitely often, or eventually; explicit-family or worst-case.
5. **Historical claim:** the supplied year and attribution do not locate a theorem, edition, theorem
   number, or page and must be checked rather than used to choose a result.

## Explicit exclusions

- Cook-Levin, Haken's pigeonhole lower bound, or any adjacent catalog entry as a substitute.
- A generic counting observation or an assumed lower-bound predicate repackaged as a theorem.
- Upper bounds, proof-search complexity, automated-prover runtime, or model-checking complexity.
- Lower bounds for an unspecified "proof" object or representation-dependent length without a
  fixed encoding and invariance/robustness boundary.
- Open lower-bound questions for strong Frege systems presented as established theorems.
- The repository label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake because the source record does not identify one.
