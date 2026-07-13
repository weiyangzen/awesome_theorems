# Scope map

## Preserved source scope

The repository fixes only the Bishop label, Errett Bishop attribution, year 1959, and the phrase
"necessary and sufficient condition for rational approximation." Bishop's 1959 Bulletin paper is
a close candidate: Theorem 4 concerns uniform rational approximation on a compact subset `C` of
the complex plane having empty interior.

In that candidate, `A` is the algebra of continuous complex-valued functions on `C` that are
uniform limits of rational functions with poles outside `C`; `M` is the minimal boundary of `A`.
The theorem makes four conditions equivalent, including `A = C(C, Complex)`, `M = C`, and the
planar-measure-zero condition on `C \ M`. These facts delimit the likely family; intake does not
promote them to the canonical claim.

## Decisions required at statement freeze

1. Approve an immutable source edition and exact theorem/definition locators, proof boundary,
   corrections, errata, and an independent source review.
2. Confirm that the catalog means Bishop's Bulletin Theorem 4 rather than another approximation or
   function-algebra result bearing Bishop's name.
3. Freeze the ambient complex plane, compactness and empty-interior hypotheses, and whether the
   empty set or other degenerate compacta are included.
4. Define rational functions on the plane and "poles outside `C`," including pole-free polynomials,
   behavior at infinity, cancellation, and evaluation/restriction conventions.
5. Define uniform approximation and whether it is expressed by sequences, metric closure, or the
   topological closure of a subalgebra of continuous maps.
6. Transcribe Bishop's minimal-boundary definition, including the separating closed algebra and
   norm-attainment predicate on the compact metric space `C`.
7. Select the canonical equivalence: universal complex-valued approximation iff `M = C`, iff the
   complement of `M` has planar measure zero, or the complete four-way equivalence including real
   parts and the strong-peak set.
8. Freeze planar measure, real-part approximation, peak-point definitions, binder order, equality
   versus extensional equivalence, and every coercion between `C`, its subtype, and the plane.

## Explicit exclusions

- Bishop's generalized Stone-Weierstrass theorem or the pinned real Stone-Weierstrass theorem.
- Bishop peak-set, antisymmetric-decomposition, minimal-boundary, or function-algebra results that
  do not yield this rational-approximation equivalence.
- Polynomial approximation, simultaneous approximation by a polynomial and its derivatives, or
  Mergelyan's sufficient conditions substituted for Bishop's necessary-and-sufficient result.
- Diophantine rational approximation of real or algebraic numbers.
- A special compact set, only one implication, or a definition/hypothesis that assumes the desired
  density or boundary equality.
- The catalog's untrusted `已验证` label or an adjacent API check used as source or kernel evidence.

## Formal boundary

Pinned mathlib exposes complex numbers, compact sets, continuous maps, closed subalgebras, and
Stone-Weierstrass density interfaces. A bounded local search found no Bishop rational-approximation,
controlled-pole rational-function, minimal-boundary, or Shilov-boundary terminal declaration. The
probe checks only this adjacent substrate. This is intake feasibility evidence, not an exhaustive
anchor audit and not proof of global absence.
