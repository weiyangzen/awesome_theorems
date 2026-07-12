import Mathlib.Analysis.InnerProductSpace.Basic

/-!
# THM-M-1524: exact Heisenberg-Robertson statement

This module freezes the statement boundary only. In particular, it models an
unbounded observable together with its dense domain rather than replacing it
by an everywhere-defined linear map.
-/

noncomputable section

open scoped ComplexConjugate

universe u

namespace Stage1Instances.THM_M_1524

/-- A densely defined (not necessarily bounded) complex-linear operator. -/
structure Observable (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H] where
  domain : Submodule ℂ H
  toLinearMap : domain →ₗ[ℂ] H
  dense_domain : Dense (domain : Set H)

namespace Observable

variable {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- Apply an observable to a vector equipped with a domain witness. -/
def apply (A : Observable H) (x : H) (hx : x ∈ A.domain) : H :=
  A.toLinearMap ⟨x, hx⟩

/-- Symmetry on the operator's own domain. -/
def IsSymmetric (A : Observable H) : Prop :=
  ∀ (x y : H) (hx : x ∈ A.domain) (hy : y ∈ A.domain),
    inner ℂ (A.apply x hx) y = inner ℂ x (A.apply y hy)

/--
Self-adjointness, expressed without assuming a pre-existing unbounded-adjoint
API: the vectors admitting an adjoint value are exactly `A.domain`, and that
value is `A` itself.
-/
def IsSelfAdjoint (A : Observable H) : Prop :=
  A.IsSymmetric ∧
    ∀ (y z : H),
      (∀ (x : H) (hx : x ∈ A.domain), inner ℂ (A.apply x hx) y = inner ℂ x z) ↔
        ∃ hy : y ∈ A.domain, A.apply y hy = z

/-- The expectation of an observable in a vector in its domain. -/
def expectation (A : Observable H) (ψ : H) (hψ : ψ ∈ A.domain) : ℂ :=
  inner ℂ (A.apply ψ hψ) ψ

/-- Standard deviation, defined as the norm of the centered observable vector. -/
def deviation (A : Observable H) (ψ : H) (hψ : ψ ∈ A.domain) : ℝ :=
  ‖A.apply ψ hψ - A.expectation ψ hψ • ψ‖

/-- The commutator applied where both operator products are defined. -/
def commutatorApply (A B : Observable H) (ψ : H)
    (hA : ψ ∈ A.domain) (hB : ψ ∈ B.domain)
    (hAB : B.apply ψ hB ∈ A.domain) (hBA : A.apply ψ hA ∈ B.domain) : H :=
  A.apply (B.apply ψ hB) hAB - B.apply (A.apply ψ hA) hBA

/-- The canonical commutation relation on the common product domain. -/
def CanonicalCommutationRelation (Q P : Observable H) (hbar : ℝ) : Prop :=
  ∀ (x : H) (hQ : x ∈ Q.domain) (hP : x ∈ P.domain)
    (hQP : P.apply x hP ∈ Q.domain) (hPQ : Q.apply x hQ ∈ P.domain),
      Q.commutatorApply P x hQ hP hQP hPQ = (Complex.I * (hbar : ℂ)) • x

end Observable

/-- Robertson's uncertainty inequality with every unbounded-product domain explicit. -/
def RobertsonTarget : Prop :=
  ∀ (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A B : Observable H) (ψ : H)
    (hA : ψ ∈ A.domain) (hB : ψ ∈ B.domain)
    (hAB : B.apply ψ hB ∈ A.domain) (hBA : A.apply ψ hA ∈ B.domain),
      A.IsSelfAdjoint → B.IsSelfAdjoint → ‖ψ‖ = 1 →
        ‖inner ℂ (A.commutatorApply B ψ hA hB hAB hBA) ψ‖ / 2 ≤
          A.deviation ψ hA * B.deviation ψ hB

/-- Position-momentum specialization under the canonical commutation relation. -/
def HeisenbergCCRTarget : Prop :=
  ∀ (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (Q P : Observable H) (ψ : H) (hbar : ℝ)
    (hQ : ψ ∈ Q.domain) (hP : ψ ∈ P.domain)
    (hQP : P.apply ψ hP ∈ Q.domain) (hPQ : Q.apply ψ hQ ∈ P.domain),
      Q.IsSelfAdjoint → P.IsSelfAdjoint → 0 ≤ hbar → ‖ψ‖ = 1 →
        Q.CanonicalCommutationRelation P hbar →
          hbar / 2 ≤ Q.deviation ψ hQ * P.deviation ψ hP

/-- The exact target: Robertson's bound and its canonical-pair corollary. -/
def HeisenbergUncertaintyTarget : Prop :=
  RobertsonTarget.{u} ∧ HeisenbergCCRTarget.{u}

/-- Checked expansion of the selected two-part target. -/
theorem target_iff_components :
    HeisenbergUncertaintyTarget.{u} ↔
      RobertsonTarget.{u} ∧ HeisenbergCCRTarget.{u} :=
  Iff.rfl

-- Structural mutations: each elaborates but is intentionally not the target.
def mutationEverywhereDefined : Prop :=
  ∀ (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A B : H →ₗ[ℂ] H) (ψ : H), ‖ψ‖ = 1 → True

def mutationSymmetricOnly : Prop :=
  ∀ (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A B : Observable H), A.IsSymmetric → B.IsSymmetric → True

def mutationNoProductDomains : Prop :=
  ∀ (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A B : Observable H) (ψ : H), ψ ∈ A.domain → ψ ∈ B.domain → True

def mutationUnnormalized : Prop :=
  ∀ (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (A B : Observable H) (ψ : H), A.IsSelfAdjoint → B.IsSelfAdjoint → True

end Stage1Instances.THM_M_1524

set_option pp.explicit true in
#print Stage1Instances.THM_M_1524.HeisenbergUncertaintyTarget
