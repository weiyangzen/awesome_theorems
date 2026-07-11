# Scope map

## Included subject boundary

- Ext in an abelian category (or a source-supported specialization such as modules) with the
  existence assumptions needed to define derived functors.
- A short exact sequence in either Ext argument and the induced connecting morphisms.
- Both standard variance directions are candidates: covariant in the second argument and
  contravariant in the first.
- Exactness, degree shift, naturality, the degree-zero boundary, and zero/low-degree cases must be
  frozen explicitly by the statement phase.

## Required statement decisions

The metadata says only "the long exact sequence of the Ext functor." It does not decide whether the
root quantifies over a short exact sequence in the first or second argument, whether both directions
are conjoined, or whether "long exact" means an indexed exact complex or every adjacent six-term
window. It also omits the ambient category and enough-injective/projective assumptions.

The statement phase must select an exact primary-source formulation, record all ordered binders and
hypotheses, and justify its relation to mathlib's categorical API. It must not silently strengthen a
one-variance source theorem into a conjunction of both directions.

## Explicit exclusions

- Tor long exact sequences, spectral sequences, and a generic delta-functor theorem as substitutes.
- A single connecting homomorphism without exactness and naturality obligations.
- An abstract proposition whose desired conclusion is assumed as a hypothesis.
- `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_102.lean` as accepted rev-5.6 evidence; it is
  discovery input until exact-statement, trust, provenance, and build gates are rerun.
