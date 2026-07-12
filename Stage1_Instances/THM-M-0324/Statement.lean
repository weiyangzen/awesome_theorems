import Mathlib.Analysis.Normed.Module.Bases
import Mathlib.LinearAlgebra.Dimension.FreeAndStrongRankCondition

/-!
# THM-M-0324: Enflo no-Schauder-basis statement

This module freezes the conservative consequence selected at intake. It contains
no construction of Enflo's space and no proof of the target.
-/

namespace Stage1Instances.THM_M_0324

universe u

/-- A bundled real Banach space, used so that the existential target does not
leave typeclass metavariables or rely on scoped local instances. -/
structure RealBanachSpace where
  carrier : Type u
  normedAddCommGroup : NormedAddCommGroup carrier
  normedSpace : NormedSpace Real carrier
  completeSpace : CompleteSpace carrier

namespace RealBanachSpace

instance (X : RealBanachSpace.{u}) : NormedAddCommGroup X.carrier :=
  X.normedAddCommGroup

instance (X : RealBanachSpace.{u}) : NormedSpace Real X.carrier :=
  X.normedSpace

instance (X : RealBanachSpace.{u}) : CompleteSpace X.carrier :=
  X.completeSpace

end RealBanachSpace

/-- The selected exact target: some separable infinite-dimensional real Banach
space admits no countable Schauder basis. The two domain conditions prevent a
finite-dimensional or nonseparable representation shortcut. -/
def EnfloNoSchauderBasisTarget : Prop :=
  ∃ X : RealBanachSpace.{u},
    ¬ FiniteDimensional Real X.carrier ∧
    TopologicalSpace.SeparableSpace X.carrier ∧
    ¬ Nonempty (SchauderBasis Real X.carrier)

/-- Equivalent sigma-style presentation, retained only through this checked
transport. -/
def SigmaPresentation : Prop :=
  Nonempty
    {X : RealBanachSpace.{u} //
      ¬ FiniteDimensional Real X.carrier ∧
      TopologicalSpace.SeparableSpace X.carrier ∧
      ¬ Nonempty (SchauderBasis Real X.carrier)}

theorem enfloTarget_iff_sigmaPresentation :
    EnfloNoSchauderBasisTarget.{u} ↔ SigmaPresentation.{u} := by
  constructor
  · rintro ⟨X, hX⟩
    exact ⟨⟨X, hX⟩⟩
  · rintro ⟨⟨X, hX⟩⟩
    exact ⟨X, hX⟩

-- Structural mutations elaborate separately; the checker requires their
-- printed kernel expressions to differ from the canonical target.
def mutationRemovedInfiniteDimension : Prop :=
  ∃ X : RealBanachSpace.{u},
    TopologicalSpace.SeparableSpace X.carrier ∧
    ¬ Nonempty (SchauderBasis Real X.carrier)

def mutationChangedScalarToRat : Prop :=
  ∃ (X : Type u) (_ : NormedAddCommGroup X) (_ : NormedSpace Rat X)
      (_ : CompleteSpace X),
    letI : NormedAddCommGroup X := ‹NormedAddCommGroup X›
    letI : NormedSpace Rat X := ‹NormedSpace Rat X›
    ¬ FiniteDimensional Rat X ∧
    TopologicalSpace.SeparableSpace X ∧
    ¬ Nonempty (SchauderBasis Rat X)

def mutationChangedBinderScope : Prop :=
  ∀ X : RealBanachSpace.{u},
    (¬ FiniteDimensional Real X.carrier) →
    TopologicalSpace.SeparableSpace X.carrier →
    ¬ Nonempty (SchauderBasis Real X.carrier)

def mutationOnlySpecifiedSequenceFails : Prop :=
  ∃ (X : RealBanachSpace.{u}) (b : Nat → X.carrier),
    (¬ FiniteDimensional Real X.carrier) ∧
    TopologicalSpace.SeparableSpace X.carrier ∧
    ¬ ∃ sb : SchauderBasis Real X.carrier, (sb : Nat → X.carrier) = b

/-- The zero-space shortcut is excluded by the infinite-dimensional conjunct. -/
theorem zeroSpaceBoundary :
    FiniteDimensional Real (Fin 0 → Real) := by
  infer_instance

end Stage1Instances.THM_M_0324

set_option pp.explicit true in
#print Stage1Instances.THM_M_0324.EnfloNoSchauderBasisTarget
