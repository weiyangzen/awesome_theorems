# Scope map

## Preserved theorem family

The intake preserves the representation-theory family named by the catalog: orthogonality
relations for group characters. Finiteness is a likely domain and is required by the direct pinned
candidate, but the catalog itself does not state it. The intake does not silently equate the plural
family with one familiar formula.

The most direct pinned Lean candidate is row orthogonality: for irreducible finite-dimensional
representations `V` and `W`, a normalized sum of `character V g * character W (g^-1)` is one when
the representations are isomorphic and zero otherwise. That is a candidate interpretation, not the
frozen root.

## Decisions required at statement freeze

1. Preserve and independently review an authoritative source edition, exact theorem/page,
   incorporated definitions, proof boundary, translation, and errata.
2. Decide whether the root is row orthogonality of irreducible characters, column orthogonality
   over conjugacy classes, or an explicitly delimited package of character relations.
3. Fix the acting object and finiteness data: finite group, a chosen finite enumeration, or another
   source-defined domain.
4. Fix the scalar field. The classical complex formulation and mathlib's algebraically closed
   field with invertible group cardinal are related, but not definitionally the same statement.
5. Fix whether characters are traces of bundled representations, abstract class functions known
   to arise from representations, or members of an enumerated irreducible-character family.
6. Fix irreducibility and equivalence conventions, including whether the Kronecker delta tests
   equality of chosen representatives or existence of a representation isomorphism.
7. Fix normalization: division by the group order versus an unnormalized sum, and scalar inverse
   or invertibility-witness notation.
8. Fix the second factor: evaluation at `g^-1`, complex conjugation, star, or another source-defined
   involution, together with the checked transport between credited forms.
9. Fix binder order, universe and typeclass parameters, conclusion equality, all boundary cases,
   foundation/TCB/computation profiles, and every alternate encoding.

## Boundary cases

Source and statement review must explicitly dispose of the trivial group; isomorphic but not
definitionally equal representations; equal representations; zero-dimensional carriers; scalar
characteristic dividing the group order; absence of the required cardinal inverse; non-algebraically
closed fields; reducible representations; empty or non-complete enumerations of irreducibles; and
the distinction between normalized and unnormalized sums. No case is excluded at intake.

## Explicit substitutions excluded

- The Frobenius endomorphism and finite-field automorphism theorems, Frobenius reciprocity,
  Frobenius group theorems, Frobenius integrability theorem, and Perron-Frobenius theorem share a
  name but are excluded by the catalog's character-orthogonality gloss.
- Orthogonality of characters of a finite abelian group as group homomorphisms is a specialized
  Fourier theorem, not automatically the requested representation-character theorem.
- Dirichlet-character orthogonality is a number-theoretic result with a different domain.
- Matrix-coefficient orthogonality is a related representation theorem, not a group-character
  relation and not a candidate root for this catalog gloss.
- Column orthogonality and completeness of the irreducible character table are not supplied by a
  row-orthogonality theorem alone.
- The Hom-space dimension formula is the direct candidate's proof bridge, not an independently
  selected replacement for the catalog root.
- Schur's lemma and Maschke's theorem are ingredients or neighboring results, not this theorem.
- A character table, finite computation, theorem name, API probe, or the catalog's `已验证` label
  supplies no source or proof credit.
- A hypothesis or structure that stores the desired orthogonality equation is circular.

## Formal boundary

Pinned mathlib's two `char_orthonormal` declarations are direct formal leads for one reading. Intake
does not freeze their type as canonical, credit their proof bodies, establish minimal imports, or
perform the downstream source, anchor, provenance, trust, and composition audits. The canonical
Lean expression and its fingerprint remain null.
