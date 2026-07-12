# Scope map

## Intended construction family

- A smooth finite-dimensional manifold `M` and a natural degree `k`.
- Smooth real differential forms `Omega^k(M)` and the exterior derivative
  `d_k : Omega^k(M) -> Omega^(k+1)(M)`.
- Closed forms `ker d_k`, exact forms `im d_(k-1)`, and the quotient
  `H_dR^k(M; R) = ker d_k / im d_(k-1)`.
- The complex condition `d_k (d_(k-1) omega) = 0`, needed to place exact forms among closed
  forms and make the quotient meaningful.

This is a construction scope, not yet a canonical theorem. The statement phase must select an
actual proposition, such as existence/well-definedness of the graded cohomology object, rather
than presenting a definition as if it were a proved comparison theorem.

## Decisions required at statement freeze

The next phase must freeze the exact primary-source result or definition; coefficient ring; smooth
manifold model, dimension, Hausdorff and countability assumptions; boundary convention; regularity
of forms; degree indexing at `k = 0`; quotient as a module, vector space, or graded algebra; binder
order and universes; and whether functoriality or the wedge-product structure belongs to the root.
It must identify a concrete Lean differential-form complex and verify `d^2 = 0` without assuming
the desired cohomology construction as package data.

## Explicit exclusions

- The de Rham theorem comparing de Rham and singular cohomology (`THM-M-0543`).
- Hodge theory or unique harmonic representatives (`THM-M-0544`).
- The Poincare lemma, compact-support cohomology, relative cohomology, or sheaf hypercohomology as
  substitutes for the unqualified construction.
- Algebraic de Rham cohomology or the p-adic de Rham period rings in mathlib.
- A generic quotient whose closedness, exactness, equivalence relation, or `d^2 = 0` property is
  supplied as an assumption field and then credited as the target.
- The repository metadata value `已验证` as primary-source or kernel evidence.

The exact statement gate remains downstream and open. This intake intentionally creates no Lean
declaration and claims no proof from adjacent or abstract artifacts.
