import Mathlib.Logic.Basic

/-!
# THM-M-0769: axiom of choice

This module freezes the indexed-family formulation of the axiom of choice.
It records a proposition only; it does not supply an inhabitant of that
proposition or claim theorem completion.
-/

universe u v

namespace Stage1Instances.THM_M_0769

/-- Every dependent family of nonempty sorts has a simultaneous selector. -/
def AxiomOfChoiceTarget : Prop :=
  ∀ (ι : Sort u) (A : ι → Sort v),
    (∀ i, Nonempty (A i)) → Nonempty (∀ i, A i)

/-- Pointwise presentation of the same indexed-family statement. -/
def PointwiseChoiceTarget (ι : Sort u) (A : ι → Sort v) : Prop :=
  (∀ i, Nonempty (A i)) → Nonempty (∀ i, A i)

/-- Checked binder-grouping transport for the canonical target. -/
theorem axiomOfChoiceTarget_iff_pointwise :
    AxiomOfChoiceTarget.{u, v} ↔
      ∀ (ι : Sort u) (A : ι → Sort v), PointwiseChoiceTarget ι A := by
  rfl

-- Structural mutations are elaborated and compared by `check_statement.py`.
def mutationRemovedFiberNonempty : Prop :=
  ∀ (ι : Sort u) (A : ι → Sort v), Nonempty (∀ i, A i)

def mutationChangedDomain : Prop :=
  ∀ (ι : Type u) (A : ι → Type v),
    (∀ i, Nonempty (A i)) → Nonempty (∀ i, A i)

def mutationChangedBinderScope : Prop :=
  ∀ (ι : Sort u),
    Nonempty ((A : ι → Sort v) → (∀ i, Nonempty (A i)) → (∀ i, A i))

def mutationExcludedEmptyIndex : Prop :=
  ∀ (ι : Type u) [Nonempty ι] (A : ι → Sort v),
    (∀ i, Nonempty (A i)) → Nonempty (∀ i, A i)

end Stage1Instances.THM_M_0769

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0769.AxiomOfChoiceTarget
