# Scope map

## Received claim

The exact received mathematical wording is `关于中心单代数的指数与次数`, literally "about the
index and degree of central simple algebras." This is a topic phrase, not a truth-valued
proposition. Intake preserves that boundary and does not choose a standard result from memory.

## Terms whose meanings remain open

- **Central simple algebra:** the source must fix a base field, associative unital algebra,
  centrality, simplicity, finite dimensionality, universes, and any characteristic restriction.
- **Degree:** a likely convention is the positive integer whose square is the vector-space
  dimension over the center, but the repository does not state this. Matrix size, dimension, or a
  field-extension degree would give different formal targets.
- **Index:** a likely convention is the degree of the division-algebra representative in a Brauer
  class, but the repository supplies neither the representative theorem nor this definition. Other
  uses of "index" must not be silently excluded.
- **Relation:** no predicate joins the two nouns. Even after definitions are fixed, the result
  could assert divisibility, equality in a special case, shared prime support, invariance under
  extension or Brauer equivalence, or a bound involving an exponent.

## Candidate readings not credited

1. The index of a finite-dimensional central simple algebra divides its degree.
2. Index and degree have the same prime divisors.
3. The Brauer-class index is invariant under replacing an algebra by a matrix algebra over its
   division representative.
4. The exponent divides the index and the index and exponent have the same prime divisors.
5. A period-index or index-degree equality/bound for a restricted class of fields.

These statements have different hypotheses and conclusions. The catalogue does not select one,
and none is the canonical claim at intake.

## Pinned Lean substrate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Algebra.BrauerGroup.Defs` supplies a bundled finite-dimensional central simple algebra
`CSA K`, stable matrix equivalence `IsBrauerEquivalent`, its setoid, and the quotient
`BrauerGroup K`. Those objects could support later definitions after a source statement is chosen.
The bounded search of `Mathlib/Algebra/BrauerGroup` and `Mathlib/Algebra/Central` found no
declaration defining the central-simple-algebra index, degree, or exponent. Absence from that
bounded surface is not a repository-wide or external-corpus nonexistence claim.

## Decisions required at statement freeze

1. Identify and independently inspect an immutable primary or authoritative source with exact
   author, title, edition or scan, theorem and page/section, definitions, proof boundary, and errata.
2. Resolve whether `莫林` / `Sigmund Morill` is correct metadata or a mistranscription; do not infer
   an eponym solely from spelling similarity.
3. Quote the exact asserted relation and fix whether exponent/period data are part of the root.
4. Fix the base field, algebra conventions, finite-dimensionality, characteristic restrictions,
   ordered binders, and every nontrivial typeclass premise.
5. Define degree and index and record their codomains, positivity, existence/choice dependencies,
   treatment of split algebras, and behavior under matrix representatives and scalar extension.
6. Elaborate the exact Lean expression with minimal pinned imports, preserve its expression and
   environment fingerprints, and check all credited alternate encodings and mutations.

## Explicit exclusions

- The Artin-Wedderburn classification, Brauer-group construction, or quotient definition used as
  a substitute for an unstated index-degree theorem.
- An index-exponent theorem substituted merely because both use the word "index".
- A theorem restricted to local, global, finite, or algebraically closed fields without source
  authorization.
- A structure, premise, or definition that assumes the desired relation.
- The untrusted `已验证` label, a theorem-name match, or this discovery probe used as proof credit.

No canonical obligation registry or proof-tree denominator may be frozen until these choices are
resolved by source evidence.
