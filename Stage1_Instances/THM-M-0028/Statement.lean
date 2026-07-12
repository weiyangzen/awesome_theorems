import Mathlib.RingTheory.Finiteness.Defs

/-!
# THM-M-0028 canonical Lean statement

This module freezes the modern unital commutative specialization of Noether's ascending-chain
theorem selected at intake. It checks the ideal/regular-submodule and monotone-function encodings
and the required statement mutations, but it does not import or invoke the ascending-chain theorem
or construct an inhabitant of the target.
-/

namespace Stage1Instances.THM_M_0028

universe u

/-- If every ideal of a commutative ring is finitely generated, every ascending ideal chain
eventually stabilizes. -/
def IdealAscendingChainTarget : Prop :=
  forall {R : Type u} [CommRing R],
    (forall I : Ideal R, I.FG) ->
      forall f : Nat →o Ideal R,
        exists n, forall m, n <= m -> f n = f m

/-- The regular-submodule spelling adjacent to mathlib's generic Noetherian-module interface. -/
def RegularSubmoduleAscendingChainTarget : Prop :=
  forall {R : Type u} [CommRing R],
    (forall I : Submodule R R, I.FG) ->
      forall f : Nat →o Submodule R R,
        exists n, forall m, n <= m -> f n = f m

/-- The source-like spelling as a function plus an explicit monotonicity hypothesis. -/
def MonotoneIdealSequenceTarget : Prop :=
  forall {R : Type u} [CommRing R],
    (forall I : Ideal R, I.FG) ->
      forall f : Nat -> Ideal R, Monotone f ->
        exists n, forall m, n <= m -> f n = f m

/-- `Ideal R` is definitionally the regular submodule `Submodule R R`. -/
theorem idealAscendingChainTarget_iff_regularSubmoduleAscendingChainTarget :
    IdealAscendingChainTarget.{u} <-> RegularSubmoduleAscendingChainTarget.{u} :=
  Iff.rfl

/-- Checked transport between `OrderHom` chains and functions with a monotonicity hypothesis. -/
theorem idealAscendingChainTarget_iff_monotoneIdealSequenceTarget :
    IdealAscendingChainTarget.{u} <-> MonotoneIdealSequenceTarget.{u} := by
  constructor
  · intro h R _ hfg f hf
    let g : Nat →o Ideal R := ⟨f, hf⟩
    exact h hfg g
  · intro h R _ hfg f
    exact h hfg f f.monotone

/-! Structural mutations elaborate as propositions but receive no statement-identity credit. -/

def mutationRemovedFiniteGenerationHypothesis : Prop :=
  forall {R : Type u} [CommRing R],
    forall f : Nat →o Ideal R,
      exists n, forall m, n <= m -> f n = f m

def mutationChangedDomainToField : Prop :=
  forall {K : Type u} [Field K],
    (forall I : Ideal K, I.FG) ->
      forall f : Nat →o Ideal K,
        exists n, forall m, n <= m -> f n = f m

def mutationChangedBinderScope : Prop :=
  forall {R : Type u} [CommRing R],
    (forall I : Ideal R, I.FG) ->
      exists n, forall f : Nat →o Ideal R,
        forall m, n <= m -> f n = f m

def mutationExcludedZeroRing : Prop :=
  forall {R : Type u} [CommRing R] [Nontrivial R],
    (forall I : Ideal R, I.FG) ->
      forall f : Nat →o Ideal R,
        exists n, forall m, n <= m -> f n = f m

variable
  (hRemoved : mutationRemovedFiniteGenerationHypothesis.{u})
  (hDomain : mutationChangedDomainToField.{u})
  (hScope : mutationChangedBinderScope.{u})
  (hBoundary : mutationExcludedZeroRing.{u})

#check_failure (show IdealAscendingChainTarget.{u} from hRemoved)
#check_failure (show IdealAscendingChainTarget.{u} from hDomain)
#check_failure (show IdealAscendingChainTarget.{u} from hScope)
#check_failure (show IdealAscendingChainTarget.{u} from hBoundary)

/-- A subsingleton commutative ring is in scope although it cannot be nontrivial. -/
theorem subsingleton_boundary_has_no_nontrivial
    (R : Type u) [CommRing R] [Subsingleton R] :
    Not (Nontrivial R) := by
  intro h
  rcases h.exists_pair_ne with ⟨a, b, hab⟩
  exact hab (Subsingleton.elim a b)

#check idealAscendingChainTarget_iff_regularSubmoduleAscendingChainTarget
#check idealAscendingChainTarget_iff_monotoneIdealSequenceTarget
#print axioms idealAscendingChainTarget_iff_regularSubmoduleAscendingChainTarget
#print axioms idealAscendingChainTarget_iff_monotoneIdealSequenceTarget
#print axioms subsingleton_boundary_has_no_nontrivial

set_option pp.universes true in
set_option pp.explicit true in
#print IdealAscendingChainTarget

end Stage1Instances.THM_M_0028
