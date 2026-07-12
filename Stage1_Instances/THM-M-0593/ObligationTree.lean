import Statement

/-! Checked conditional composition for the frozen THM-M-0593 architecture. -/

namespace Stage1Instances.THMM0593

open MeasureTheory Set

def ZeroCodomainBranch : Prop :=
  forall (m : Nat) (f : EuclideanSpace Real (Fin m) -> EuclideanSpace Real (Fin 0))
      (R : Set (EuclideanSpace Real (Fin m))),
    IsOpen R -> ContDiffOn Real (⊤ : ℕ∞) f R ->
      (volume : Measure (EuclideanSpace Real (Fin 0))) (f '' criticalPointsOn f R) = 0

def LowDimensionBranch : Prop :=
  forall (m n : Nat) (f : EuclideanSpace Real (Fin m) -> EuclideanSpace Real (Fin n))
      (R : Set (EuclideanSpace Real (Fin m))),
    m < n -> IsOpen R -> ContDiffOn Real (⊤ : ℕ∞) f R ->
      (volume : Measure (EuclideanSpace Real (Fin n))) (f '' criticalPointsOn f R) = 0

def HardDimensionBranch : Prop :=
  forall (m n : Nat) (f : EuclideanSpace Real (Fin m) -> EuclideanSpace Real (Fin n))
      (R : Set (EuclideanSpace Real (Fin m))),
    0 < n -> n <= m -> IsOpen R -> ContDiffOn Real (⊤ : ℕ∞) f R ->
      (volume : Measure (EuclideanSpace Real (Fin n))) (f '' criticalPointsOn f R) = 0

/-- The exact root follows from the exhaustive dimension branches. -/
theorem root_of_sard_branches
    (zero : ZeroCodomainBranch)
    (low : LowDimensionBranch)
    (hard : HardDimensionBranch) : SardTarget := by
  intro m n f R hopen hsmooth
  by_cases hn : n = 0
  · subst n
    exact zero m f R hopen hsmooth
  by_cases hmn : m < n
  · exact low m n f R hmn hopen hsmooth
  · exact hard m n f R (Nat.pos_of_ne_zero hn) (Nat.le_of_not_gt hmn) hopen hsmooth

#print axioms root_of_sard_branches

end Stage1Instances.THMM0593
