import Statement

/-!
# THM-M-1356 conditional obligation composition

This module checks only the final child-to-root interface frozen by the
obligation registry.  Both implications are explicit hypotheses: no proof of
either direction of the Routh-Hurwitz criterion is asserted here.
-/

namespace Stage1Instances.THM_M_1356.ObligationTree

open Stage1Instances.THM_M_1356

/-- Exact forward implication at the frozen binders. -/
def StableToPositiveMinorsTarget : Prop :=
  ∀ (n : Nat), 0 < n → ∀ a : Fin (n + 1) → Real,
    IsPositiveDegreeN a →
      IsStrictlyStable a → ∀ k : Fin n, 0 < hurwitzMinor a k

/-- Exact reverse implication at the frozen binders. -/
def PositiveMinorsToStableTarget : Prop :=
  ∀ (n : Nat), 0 < n → ∀ a : Fin (n + 1) → Real,
    IsPositiveDegreeN a →
      (∀ k : Fin n, 0 < hurwitzMinor a k) → IsStrictlyStable a

/-- Exact pair of implication packages consumed by root composition. -/
def DirectionPackage : Prop :=
  StableToPositiveMinorsTarget ∧ PositiveMinorsToStableTarget

/-- Conditional assembly of both exact implication packages. -/
theorem directionPackage_of_directions
    (forward : StableToPositiveMinorsTarget)
    (reverse : PositiveMinorsToStableTarget) : DirectionPackage :=
  ⟨forward, reverse⟩

/-- Conditional child-to-root composition. Every mathematical child remains
an explicit premise; this declaration only checks their final assembly. -/
theorem root_of_directionPackage
    (directions : DirectionPackage) : RouthHurwitzTarget := by
  intro n hn a ha
  exact ⟨directions.1 n hn a ha, directions.2 n hn a ha⟩

/-- Combined conditional root harness. Both directions are consumed. -/
theorem root_of_directions
    (forward : StableToPositiveMinorsTarget)
    (reverse : PositiveMinorsToStableTarget) : RouthHurwitzTarget :=
  root_of_directionPackage (directionPackage_of_directions forward reverse)

#check StableToPositiveMinorsTarget
#check PositiveMinorsToStableTarget
#check DirectionPackage
#check directionPackage_of_directions
#check root_of_directionPackage
#check root_of_directions

#print axioms directionPackage_of_directions
#print axioms root_of_directionPackage
#print axioms root_of_directions

end Stage1Instances.THM_M_1356.ObligationTree
