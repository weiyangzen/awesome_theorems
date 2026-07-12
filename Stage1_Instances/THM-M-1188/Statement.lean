import Mathlib.Analysis.InnerProductSpace.Laplacian

/-!
# THM-M-1188: exact weak maximum principle statement for the heat equation

This module freezes the classical finite-dimensional Euclidean statement. It
contains no proof of the maximum principle.
-/

namespace Stage1Instances.THM_M_1188

open scoped InnerProductSpace
open Laplacian

/-- Euclidean space of dimension `n`, with its standard inner product norm. -/
abbrev Euclidean (n : Nat) := EuclideanSpace ℝ (Fin n)

/-- The closed space-time cylinder `closure U x [0, T]`. -/
def closedCylinder {n : Nat} (U : Set (Euclidean n)) (T : ℝ) :
    Set (Euclidean n × ℝ) :=
  closure U ×ˢ Set.Icc 0 T

/-- The initial face together with the lateral boundary. The terminal interior
face is deliberately not boundary data. -/
def parabolicBoundary {n : Nat} (U : Set (Euclidean n)) (T : ℝ) :
    Set (Euclidean n × ℝ) :=
  (closure U ×ˢ ({0} : Set ℝ)) ∪ (frontier U ×ˢ Set.Icc 0 T)

/-- The heat subsolution inequality on `U x (0, T]`. -/
def IsHeatSubsolution {n : Nat} (U : Set (Euclidean n)) (T : ℝ)
    (u : Euclidean n × ℝ → ℝ) : Prop :=
  ∀ x ∈ U, ∀ t ∈ Set.Ioc 0 T,
    deriv (fun s : ℝ ↦ u (x, s)) t -
      (@Laplacian.laplacian (Euclidean n → ℝ) (Euclidean n → ℝ)
        InnerProductSpace.instLaplacian (fun y : Euclidean n ↦ u (y, t))) x ≤ 0

/-- The classical spatial and temporal regularity used by the target. -/
def HasClassicalHeatRegularity {n : Nat} (U : Set (Euclidean n)) (T : ℝ)
    (u : Euclidean n × ℝ → ℝ) : Prop :=
  ContinuousOn u (closedCylinder U T) ∧
  (∀ t ∈ Set.Ioc 0 T, ContDiffOn ℝ 2 (fun x : Euclidean n ↦ u (x, t)) U) ∧
  (∀ x ∈ U, ContDiffOn ℝ 1 (fun t : ℝ ↦ u (x, t)) (Set.Ioc 0 T))

/-- The canonical weak maximum principle for the classical heat operator.

The conclusion is the attained-maximum form: one point of the parabolic
boundary dominates every point of the closed cylinder.
-/
def HeatEquationWeakMaximumPrincipleTarget : Prop :=
  ∀ (n : Nat), 1 ≤ n → ∀ (U : Set (Euclidean n)), U.Nonempty → IsOpen U →
    Bornology.IsBounded U → ∀ (T : ℝ), 0 < T →
      ∀ u : Euclidean n × ℝ → ℝ,
        HasClassicalHeatRegularity U T u → IsHeatSubsolution U T u →
          ∃ b ∈ parabolicBoundary U T, ∀ z ∈ closedCylinder U T, u z ≤ u b

/-- Pointwise spelling of the same attained-boundary-maximum assertion. -/
def PointwiseMaximumForm : Prop :=
  ∀ (n : Nat), 1 ≤ n → ∀ (U : Set (Euclidean n)), U.Nonempty → IsOpen U →
    Bornology.IsBounded U → ∀ (T : ℝ), 0 < T →
      ∀ u : Euclidean n × ℝ → ℝ,
        HasClassicalHeatRegularity U T u → IsHeatSubsolution U T u →
          ∃ b, b ∈ parabolicBoundary U T ∧
            ∀ z, z ∈ closedCylinder U T → u z ≤ u b

/-- Checked transport to the direct pointwise encoding. -/
theorem target_iff_pointwiseMaximumForm :
    HeatEquationWeakMaximumPrincipleTarget ↔ PointwiseMaximumForm :=
  Iff.rfl

-- Structural mutations are elaborated and expression-compared by the validator.
def mutationRemovedSubsolution : Prop :=
  ∀ (n : Nat), 1 ≤ n → ∀ (U : Set (Euclidean n)), U.Nonempty → IsOpen U →
    Bornology.IsBounded U → ∀ (T : ℝ), 0 < T →
      ∀ u : Euclidean n × ℝ → ℝ,
        HasClassicalHeatRegularity U T u →
          ∃ b ∈ parabolicBoundary U T, ∀ z ∈ closedCylinder U T, u z ≤ u b

def mutationChangedDomainToOneDimension : Prop :=
  ∀ (U : Set (Euclidean 1)), U.Nonempty → IsOpen U → Bornology.IsBounded U →
    ∀ (T : ℝ), 0 < T → ∀ u : Euclidean 1 × ℝ → ℝ,
      HasClassicalHeatRegularity U T u → IsHeatSubsolution U T u →
        ∃ b ∈ parabolicBoundary U T, ∀ z ∈ closedCylinder U T, u z ≤ u b

def mutationChangedBinderScope : Prop :=
  ∀ (n : Nat), 1 ≤ n → ∀ (U : Set (Euclidean n)), U.Nonempty → IsOpen U →
    Bornology.IsBounded U → ∀ (T : ℝ), 0 < T →
      ∀ u : Euclidean n × ℝ → ℝ,
        HasClassicalHeatRegularity U T u → IsHeatSubsolution U T u →
          ∀ z ∈ closedCylinder U T, ∃ b ∈ parabolicBoundary U T, u z ≤ u b

/-- Mutation that incorrectly treats the entire terminal face as boundary. -/
def mutationIncludesTerminalFace : Prop :=
  ∀ (n : Nat), 1 ≤ n → ∀ (U : Set (Euclidean n)), U.Nonempty → IsOpen U →
    Bornology.IsBounded U → ∀ (T : ℝ), 0 < T →
      ∀ u : Euclidean n × ℝ → ℝ,
        HasClassicalHeatRegularity U T u → IsHeatSubsolution U T u →
          ∃ b ∈ parabolicBoundary U T ∪ (closure U ×ˢ ({T} : Set ℝ)),
            ∀ z ∈ closedCylinder U T, u z ≤ u b

/-- The initial face is included in the parabolic boundary. -/
theorem initialFace_mem_parabolicBoundary {n : Nat} {U : Set (Euclidean n)}
    {T : ℝ} {x : Euclidean n} (hx : x ∈ closure U) :
    (x, 0) ∈ parabolicBoundary U T := by
  exact Or.inl ⟨hx, Set.mem_singleton 0⟩

end Stage1Instances.THM_M_1188

set_option pp.explicit true in
#print Stage1Instances.THM_M_1188.HeatEquationWeakMaximumPrincipleTarget
