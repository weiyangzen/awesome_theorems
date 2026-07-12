# Scope map

## Repository claim

The repository supplies only the name "Kasparov KK-theory", the gloss "bivariant K-theory of
operator algebras", attribution to Gennadi Kasparov, and the date 1980. A mathematical theory is not
itself a proposition. The intake consequently preserves this literal scope and marks the selection
of a unique theorem as the first statement-phase blocker.

## Provisional mathematical center

The strongest non-substitutive candidate for a foundational theorem is the Kasparov product. A
source-qualified target is expected to quantify over graded C*-algebras and construct a product

`KK(A,D) x KK(D,B) -> KK(A,B)`

with the relevant bilinearity, functoriality, associativity, and identity-class properties. The
selected primary statement must determine which of these are one theorem, which are corollaries,
and whether separability, countable generation, sigma-unitality, equivariance, grading, or
nonunital conventions are hypotheses. This paragraph is a discovery scope, not an exact statement.

## Decisions required before statement freeze

- Select a unique primary-source edition and pinpoint theorem, including corrections or errata.
- Fix ordinary versus equivariant KK-theory and real versus complex C*-algebras.
- Fix grading, separability, sigma-unitality, unitality, and countability assumptions for `A`, `D`,
  `B`, and the Hilbert modules.
- Fix the definition of a Kasparov cycle, compact operators, homotopy/degenerate-cycle quotient,
  and the equivalence relation that forms each KK-group.
- State whether the canonical conclusion is product existence and well-definedness alone or the
  complete associativity/unit package, with ordered binders and all side conditions.
- Audit zero and trivially graded algebras, identity classes, suspension conventions, coefficient
  variables, universes, classical choice, quotients, and extensionality.

## Explicit exclusions

- Defining `KK(A,B)` without proving a foundational structural theorem.
- Ordinary topological K-theory, K-homology, the Universal Coefficient Theorem, Bott periodicity,
  or the Baum-Connes conjecture as substitutes for the repository label.
- A theorem saying a pre-supplied binary operation is associative, or a structure that assumes the
  Kasparov product and its laws as fields.
- A special case such as finite-dimensional algebras, trivially graded algebras, or `A = C` unless
  the selected source claim itself has that scope.
- The repository's untrusted `已验证` label as source, Lean, or proof evidence.

No canonical Lean target is frozen by this intake. The statement phase must either expose the real
C*-algebra, Hilbert-module, cycle, quotient, and product interfaces or record a precise missing-API
blocker; it must not replace them with an abstract terminal package.
