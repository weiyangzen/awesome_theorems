import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic

open scoped ENNReal MeasureTheory

namespace Stage1Instances.THM_M_1286

open MeasureTheory Set Filter

abbrev Euclidean (n : ℕ) := Fin n → ℝ

/-- The distributional weak-gradient convention used by the frozen target. -/
def HasWeakGradient {n : ℕ} (u : Euclidean n → ℝ) (g : Euclidean n → Euclidean n) : Prop :=
  ∀ (i : Fin n) (φ : Euclidean n → ℝ), ContDiff ℝ ⊤ φ → HasCompactSupport φ →
    (∫ x, u x * (fderiv ℝ φ x) (Pi.single i 1)) = -(∫ x, g x i * φ x)

/-- Finite positive superlevel sets, the whole-space "vanishes at infinity" convention. -/
def VanishesAtInfinity {n : ℕ} (u : Euclidean n → ℝ) : Prop :=
  ∀ t : ℝ, 0 < t → volume {x | t < u x} ≠ ∞

/-- Equimeasurability expressed by equality of every positive superlevel measure. -/
def Equimeasurable {n : ℕ} (u v : Euclidean n → ℝ) : Prop :=
  ∀ t : ℝ, 0 < t → volume {x | t < u x} = volume {x | t < v x}

/-- A nonnegative function which depends antitonically on distance from the origin. -/
def IsSymmetricDecreasing {n : ℕ} (u : Euclidean n → ℝ) : Prop :=
  (∀ x, 0 ≤ u x) ∧ ∀ x y, ‖x‖ ≤ ‖y‖ → u y ≤ u x

/-- Exact finite-`p`, whole-space Polya-Szego target selected by the intake. -/
def PolyaSzegoTarget : Prop :=
  ∀ (n : ℕ) (p : ℝ≥0∞), 1 ≤ n → 1 ≤ p → p ≠ ∞ →
    ∀ (u : Euclidean n → ℝ) (g : Euclidean n → Euclidean n),
      (∀ x, 0 ≤ u x) → AEStronglyMeasurable u volume → MemLp u p volume →
      VanishesAtInfinity u → HasWeakGradient u g → MemLp g p volume →
      ∃ uStar : Euclidean n → ℝ, ∃ gStar : Euclidean n → Euclidean n,
        AEStronglyMeasurable uStar volume ∧ MemLp uStar p volume ∧
        IsSymmetricDecreasing uStar ∧ Equimeasurable u uStar ∧
        HasWeakGradient uStar gStar ∧ MemLp gStar p volume ∧
        eLpNorm gStar p volume ≤ eLpNorm g p volume

/-- Expanded spelling used to check that no condition is hidden by the root name. -/
def ExpandedTarget : Prop :=
  ∀ (n : ℕ) (p : ℝ≥0∞), 1 ≤ n → 1 ≤ p → p ≠ ∞ →
    ∀ (u : Euclidean n → ℝ) (g : Euclidean n → Euclidean n),
      (∀ x, 0 ≤ u x) → AEStronglyMeasurable u volume → MemLp u p volume →
      (∀ t : ℝ, 0 < t → volume {x | t < u x} ≠ ∞) →
      (∀ (i : Fin n) (φ : Euclidean n → ℝ), ContDiff ℝ ⊤ φ → HasCompactSupport φ →
        (∫ x, u x * (fderiv ℝ φ x) (Pi.single i 1)) = -(∫ x, g x i * φ x)) →
      MemLp g p volume →
      ∃ uStar : Euclidean n → ℝ, ∃ gStar : Euclidean n → Euclidean n,
        AEStronglyMeasurable uStar volume ∧ MemLp uStar p volume ∧
        ((∀ x, 0 ≤ uStar x) ∧ ∀ x y, ‖x‖ ≤ ‖y‖ → uStar y ≤ uStar x) ∧
        (∀ t : ℝ, 0 < t → volume {x | t < u x} = volume {x | t < uStar x}) ∧
        (∀ (i : Fin n) (φ : Euclidean n → ℝ), ContDiff ℝ ⊤ φ → HasCompactSupport φ →
          (∫ x, uStar x * (fderiv ℝ φ x) (Pi.single i 1)) =
            -(∫ x, gStar x i * φ x)) ∧
        MemLp gStar p volume ∧ eLpNorm gStar p volume ≤ eLpNorm g p volume

theorem polyaSzegoTarget_iff_expandedTarget : PolyaSzegoTarget ↔ ExpandedTarget := by
  rfl

-- Scope mutations: each proposition deliberately changes one frozen boundary.
def MutationAllowsDimensionZero : Prop :=
  ∀ (n : ℕ) (p : ℝ≥0∞), 1 ≤ p → p ≠ ∞ →
    ∀ (u : Euclidean n → ℝ) (g : Euclidean n → Euclidean n),
      (∀ x, 0 ≤ u x) → AEStronglyMeasurable u volume → MemLp u p volume →
      VanishesAtInfinity u → HasWeakGradient u g → MemLp g p volume → True

def MutationAllowsInfiniteExponent : Prop :=
  ∀ (n : ℕ) (p : ℝ≥0∞), 1 ≤ n → 1 ≤ p →
    ∀ (u : Euclidean n → ℝ) (g : Euclidean n → Euclidean n),
      (∀ x, 0 ≤ u x) → AEStronglyMeasurable u volume → MemLp u p volume →
      VanishesAtInfinity u → HasWeakGradient u g → MemLp g p volume → True

def MutationDropsVanishing : Prop :=
  ∀ (n : ℕ) (p : ℝ≥0∞), 1 ≤ n → 1 ≤ p → p ≠ ∞ →
    ∀ (u : Euclidean n → ℝ) (g : Euclidean n → Euclidean n),
      (∀ x, 0 ≤ u x) → AEStronglyMeasurable u volume → MemLp u p volume →
      HasWeakGradient u g → MemLp g p volume → True

def MutationReversesEnergy : Prop :=
  ∀ (n : ℕ) (p : ℝ≥0∞), 1 ≤ n → 1 ≤ p → p ≠ ∞ →
    ∀ (u : Euclidean n → ℝ) (g : Euclidean n → Euclidean n),
      (∀ x, 0 ≤ u x) → AEStronglyMeasurable u volume → MemLp u p volume →
      VanishesAtInfinity u → HasWeakGradient u g → MemLp g p volume →
      ∃ uStar : Euclidean n → ℝ, ∃ gStar : Euclidean n → Euclidean n,
        AEStronglyMeasurable uStar volume ∧ MemLp uStar p volume ∧
        IsSymmetricDecreasing uStar ∧ Equimeasurable u uStar ∧
        HasWeakGradient uStar gStar ∧ MemLp gStar p volume ∧
        eLpNorm g p volume ≤ eLpNorm gStar p volume

#check PolyaSzegoTarget
#print PolyaSzegoTarget
#check MutationAllowsDimensionZero
#check MutationAllowsInfiniteExponent
#check MutationDropsVanishing
#check MutationReversesEnergy

end Stage1Instances.THM_M_1286
