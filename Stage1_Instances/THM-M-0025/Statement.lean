import Mathlib.Algebra.Polynomial.Basic
import Mathlib.RingTheory.Noetherian.Defs

/-!
# THM-M-0025 canonical Lean statement

This module freezes the commutative, one-indeterminate Hilbert basis theorem statement selected at
intake. It checks the finite-generation encoding and the required statement mutations, but does
not import or invoke a proof of the Hilbert basis theorem.
-/

namespace Stage1Instances.THM_M_0025

universe u

/-- A polynomial ring in one indeterminate over a commutative Noetherian ring is Noetherian. -/
def HilbertBasisTheoremTarget : Prop :=
  forall {R : Type u} [CommRing R] [IsNoetherianRing R],
    IsNoetherianRing (Polynomial R)

/-- Direct expansion using finite generation of every ideal on both sides. -/
def IdealFiniteGenerationTarget : Prop :=
  forall {R : Type u} [CommRing R],
    (forall I : Ideal R, I.FG) ->
      forall J : Ideal (Polynomial R), J.FG

/-- Checked transport between the typeclass and finite-generation formulations. -/
theorem hilbertBasisTheoremTarget_iff_idealFiniteGenerationTarget :
    HilbertBasisTheoremTarget.{u} <-> IdealFiniteGenerationTarget.{u} := by
  constructor
  · intro h R _ hR
    letI : IsNoetherianRing R := (isNoetherianRing_iff_ideal_fg R).2 hR
    exact (isNoetherianRing_iff_ideal_fg (Polynomial R)).1 (h (R := R))
  · intro h R _ _
    apply (isNoetherianRing_iff_ideal_fg (Polynomial R)).2
    exact h (R := R) ((isNoetherianRing_iff_ideal_fg R).1 inferInstance)

/-! Structural mutations elaborate as propositions but receive no statement-identity credit. -/

def mutationRemovedNoetherianHypothesis : Prop :=
  forall {R : Type u} [CommRing R],
    IsNoetherianRing (Polynomial R)

def mutationChangedDomainToField : Prop :=
  forall {K : Type u} [Field K] [IsNoetherianRing K],
    IsNoetherianRing (Polynomial K)

def mutationChangedBinderScope : Prop :=
  forall {R : Type u} [CommRing R] [IsNoetherianRing R],
    exists J : Ideal (Polynomial R), J.FG

def mutationExcludedZeroRing : Prop :=
  forall {R : Type u} [CommRing R] [Nontrivial R] [IsNoetherianRing R],
    IsNoetherianRing (Polynomial R)

variable
  (hRemoved : mutationRemovedNoetherianHypothesis.{u})
  (hDomain : mutationChangedDomainToField.{u})
  (hScope : mutationChangedBinderScope.{u})
  (hBoundary : mutationExcludedZeroRing.{u})

#check_failure (show HilbertBasisTheoremTarget.{u} from hRemoved)
#check_failure (show HilbertBasisTheoremTarget.{u} from hDomain)
#check_failure (show HilbertBasisTheoremTarget.{u} from hScope)
#check_failure (show HilbertBasisTheoremTarget.{u} from hBoundary)

/-- A subsingleton commutative Noetherian ring is in scope although it cannot be nontrivial. -/
theorem subsingleton_boundary_has_no_nontrivial
    (R : Type u) [CommRing R] [IsNoetherianRing R] [Subsingleton R] :
    Not (Nontrivial R) := by
  intro h
  rcases h.exists_pair_ne with ⟨a, b, hab⟩
  exact hab (Subsingleton.elim a b)

#check hilbertBasisTheoremTarget_iff_idealFiniteGenerationTarget
#print axioms hilbertBasisTheoremTarget_iff_idealFiniteGenerationTarget
#print axioms subsingleton_boundary_has_no_nontrivial

set_option pp.universes true in
set_option pp.explicit true in
#print HilbertBasisTheoremTarget

end Stage1Instances.THM_M_0025
