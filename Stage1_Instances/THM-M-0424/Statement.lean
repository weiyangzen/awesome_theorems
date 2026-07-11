import Mathlib.Algebra.BrauerGroup.Defs
import Mathlib.RingTheory.TensorProduct.Basic

/-!
# THM-M-0424: exact Brauer-group statement

This module freezes only the field-level group-construction target selected by
the intake. It supplies no inhabitant of the target data and claims no proof.
-/

noncomputable section

namespace Stage1Instances.THM_M_0424

universe u v

variable {K : Type u} [Field K]

/-- The quotient class represented by a finite-dimensional central simple algebra. -/
abbrev BrauerClass (A : CSA.{u, v} K) : BrauerGroup K :=
  Quotient.mk (Brauer.CSA_Setoid K) A

/--
All constructions and compatibility laws asserted by the classical Brauer-group
theorem over a field. Keeping the data bundled prevents an existing unrelated
group structure on the quotient from satisfying the target by itself.
-/
structure BrauerGroupLawData (K : Type u) [Field K] where
  /-- Tensor product, packaged again as a central simple algebra. -/
  tensorRep : CSA.{u, v} K -> CSA.{u, v} K -> CSA.{u, v} K
  /-- The packaged representative has the intended underlying tensor-product algebra. -/
  tensorRep_equiv : forall A B : CSA.{u, v} K,
    Nonempty ((tensorRep A B : Type v) ≃ₐ[K] TensorProduct K A B)
  /-- Tensor representatives respect stable matrix equivalence. -/
  tensor_congr : forall {A A' B B' : CSA.{u, v} K},
    IsBrauerEquivalent A A' -> IsBrauerEquivalent B B' ->
      IsBrauerEquivalent (tensorRep A B) (tensorRep A' B')
  /-- The identity is represented by the base field. -/
  oneRep : CSA.{u, v} K
  oneRep_equiv_base : Nonempty ((oneRep : Type v) ≃ₐ[K] K)
  /-- Inversion is represented by the opposite algebra. -/
  invRep : CSA.{u, v} K -> CSA.{u, v} K
  invRep_equiv_opposite : forall A : CSA.{u, v} K,
    Nonempty ((invRep A : Type v) ≃ₐ[K] MulOpposite A)
  /-- The induced operation makes the quotient an abelian group. -/
  [commGroup : CommGroup (BrauerGroup K)]
  mul_mk : forall A B : CSA.{u, v} K,
    BrauerClass A * BrauerClass B = BrauerClass (tensorRep A B)
  one_mk : (1 : BrauerGroup K) = BrauerClass oneRep
  inv_mk : forall A : CSA.{u, v} K,
    (BrauerClass A)⁻¹ = BrauerClass (invRep A)

/--
The exact target: for every field, stable-equivalence classes of finite-dimensional
central simple algebras carry the abelian group law induced by tensor product,
with the base field as identity and opposite algebras as inverses.
-/
def BrauerGroupStatement : Prop :=
  forall (K : Type u) [Field K], Nonempty (BrauerGroupLawData.{u, v} K)

-- Structural mutations are expressions only; none is asserted.
def mutationRemovedField : Prop :=
  forall (K : Type u) [CommRing K], Nonempty K

def mutationChangedDomainToRat : Prop :=
  Nonempty (BrauerGroupLawData.{0, v} Rat)

def mutationQuotientOnly : Prop :=
  forall (K : Type u) [Field K] (A B : CSA.{u, v} K),
    BrauerClass A = BrauerClass B <-> IsBrauerEquivalent A B

def mutationOmittedInverseCompatibility : Prop :=
  forall (K : Type u) [Field K],
    Nonempty (CSA.{u, v} K -> CSA.{u, v} K -> CSA.{u, v} K)

end Stage1Instances.THM_M_0424

set_option pp.explicit true in
#print Stage1Instances.THM_M_0424.BrauerGroupStatement
