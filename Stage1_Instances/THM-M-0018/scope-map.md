# Scope map

## Preserved theorem family

The intake preserves the real-closed-field family indicated by the catalog's authors, date, and
gloss. A later statement phase may select a root only after an immutable source passage and its
incorporated definitions have been independently reviewed. Candidate components, none yet credited
as the theorem, include:

- an orderability or formal-reality criterion for a field;
- a characterization of real closed fields through their algebraic closures;
- equivalent square and odd-degree-polynomial conditions;
- existence of a real closure for a field with a chosen order; and
- uniqueness of that closure up to an order-preserving equivalence over the base field.

## Decisions required at statement freeze

1. Select the exact primary-source paper, theorem (`Satz`) and page range, all incorporated
   definitions, proof boundary, correction history, and an independent source reviewer.
2. Decide whether the root quantifies over an abstract field, an ordered field, an extension, an
   algebraic closure, or a field together with a chosen ordering.
3. Fix whether formal reality, `-1` not being a sum of squares, or existence of an ordering is a
   hypothesis or a conclusion, and provide checked transports among any credited forms.
4. Fix the definition of real closed: maximal algebraic ordered extension, no proper algebraic
   formally real extension, finite nontrivial algebraic closure, algebraic closedness after
   adjoining a root of `X^2 + 1`, or the square/odd-polynomial presentation.
5. For a closure characterization, freeze the chosen algebraic closure object, algebraicity,
   nontriviality, finiteness, degree exactly two, the element representing a square root of `-1`,
   and the meaning of "obtained by adjoining".
6. For existence or uniqueness, freeze the base ordering, its extension, the embedding over the
   base field, order preservation, algebraicity, and the exact direction and strength of uniqueness.
7. Freeze universe levels, ordered binders, typeclass hypotheses, logical strength, and whether
   characteristic zero is assumed or derived from formal reality.

## Degenerate and boundary cases

Source review must explicitly handle a base field that is already algebraically closed; a trivial
or infinite algebraic closure; characteristic two or positive characteristic; `-1` already a
square or a sum of squares; the zero or trivial ring (if the selected `Field` convention does not
already exclude it); multiple possible field orderings; a closure without a chosen compatible
order; and uniqueness as an unstructured field equivalence versus an ordered equivalence over the
base.

## Substitution exclusions

- The characteristic-`p` Artin-Schreier classification of cyclic degree-`p` extensions by
  polynomials `X^p - X - a` is a distinct theorem and cannot replace this real-closed-field item.
- Tarski quantifier elimination, completeness, decidability, and model completeness for real closed
  fields, including target `THM-M-0669`, are later model-theoretic results rather than this target.
- Hilbert's seventeenth problem, a real Nullstellensatz, and special theorems only about `Real` and
  `Complex` are not substitutes.
- Merely restating the fields of mathlib's `IsRealClosed` class, or assuming the desired ordering,
  closure, equivalence, or algebraic closedness in a structure field, is not a proof.
- Generic semireal, ordering, polynomial-root, algebraic-closure, or finite-dimensional APIs alone
  provide no theorem credit.
- `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_018.lean` belongs to `THM-M-0405` (the Bilu
  theorem), not to this target; the shared numeric suffix grants no evidence.
- The catalog's untrusted `verified` label supplies no human-source or machine-proof evidence.

No canonical statement, Lean expression fingerprint, alternate encoding, mutation result,
obligation registry, discovery protocol, or proof state is frozen at intake.
