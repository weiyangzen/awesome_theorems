import Mathlib.RingTheory.DedekindDomain.SInteger

/-!
# THM-M-0402: canonical Evertse S-unit statement

This module freezes the S-unit specialization of Theorem 1 in Evertse's 1984
paper.  Projective scaling is removed by requiring coordinate zero to be one.
The paper's infinite places are implicit in mathlib's finite-prime S-unit
model; `S` records its finite places.  This file states, but does not prove,
the finiteness theorem.
-/

set_option autoImplicit false

noncomputable section

open scoped BigOperators
open scoped NumberField
open IsDedekindDomain

namespace Stage1Instances.THMM0402

universe u

variable {K : Type u} [Field K] [NumberField K]

/-- Homogeneous coordinates whose entries are S-units. -/
abbrev SUnitTuple
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K)))
    (n : Nat) : Type u :=
  Fin (n + 1) -> S.unit K

/-- The field element underlying one S-unit coordinate. -/
def coordinateValue
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K))) {n : Nat}
    (x : SUnitTuple (K := K) S n) (i : Fin (n + 1)) : K :=
  ((x i : Kˣ) : K)

/-- Sum of the coordinates indexed by `I`. -/
def coordinateSum
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K))) {n : Nat}
    (x : SUnitTuple (K := K) S n) (I : Finset (Fin (n + 1))) : K :=
  ∑ i ∈ I, coordinateValue (K := K) S x i

/--
Normalized nondegenerate projective S-unit solutions of
`x₀ + ... + xₙ = 0`.

The condition at coordinate zero selects one representative of each
projective point.  Nondegeneracy says that every nonempty proper subsum is
nonzero, exactly as in equation (8) of the primary source.
-/
def NormalizedNondegenerateSolutions
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K))) (n : Nat) :
    Set (SUnitTuple (K := K) S n) :=
  {x |
    coordinateValue (K := K) S x 0 = 1 ∧
    coordinateSum (K := K) S x Finset.univ = 0 ∧
    ∀ I : Finset (Fin (n + 1)), I.Nonempty -> I ⊂ Finset.univ ->
      coordinateSum (K := K) S x I ≠ 0}

/--
The exact target selected by the repository's "S-unit equation solution
count" metadata: for every positive projective dimension and finite support,
there are finitely many nondegenerate projective S-unit solutions.

This is Theorem 1 of Evertse (1984), pages 226--227, specialized to
`(c,d) = (1,0)` and expressed using the unique representative with `x₀ = 1`.
-/
def EvertseSUnitStatement : Prop :=
  ∀ (n : Nat), 0 < n ->
    ∀ S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K)), S.Finite ->
      (NormalizedNondegenerateSolutions (K := K) S n).Finite

/-- Checked unfolding of membership in the canonical solution set. -/
theorem mem_normalizedNondegenerateSolutions_iff
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K))) (n : Nat)
    (x : SUnitTuple (K := K) S n) :
    x ∈ NormalizedNondegenerateSolutions (K := K) S n ↔
      coordinateValue (K := K) S x 0 = 1 ∧
      coordinateSum (K := K) S x Finset.univ = 0 ∧
      ∀ I : Finset (Fin (n + 1)), I.Nonempty -> I ⊂ Finset.univ ->
        coordinateSum (K := K) S x I ≠ 0 :=
  Iff.rfl

/-- Exact-type fixture for the ordered canonical target surface. -/
theorem evertseSUnitStatement_exact_type :
    EvertseSUnitStatement (K := K) =
      (∀ (n : Nat), 0 < n ->
        ∀ S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K)), S.Finite ->
          (NormalizedNondegenerateSolutions (K := K) S n).Finite) :=
  rfl

end Stage1Instances.THMM0402

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THMM0402.EvertseSUnitStatement
