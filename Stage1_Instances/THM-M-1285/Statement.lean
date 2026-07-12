import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace

/-!
# THM-M-1285: Schwarz symmetric decreasing rearrangement statement

This module freezes the existence-and-equimeasurability target selected by the
intake. It states no construction or proof of the rearrangement.
-/

namespace Stage1Instances.THM_M_1285

open MeasureTheory Metric
open scoped ENNReal

/-- Euclidean `n`-space with its standard inner-product norm and volume. -/
abbrev Euclidean (n : Nat) := EuclideanSpace ℝ (Fin n)

/-- A function is radial when it is constant on every sphere centered at zero. -/
def IsRadial {n : Nat} (g : Euclidean n → ENNReal) : Prop :=
  ∀ x y, ‖x‖ = ‖y‖ → g x = g y

/-- A function is nonincreasing as the distance from zero increases. -/
def IsRadiallyNonincreasing {n : Nat} (g : Euclidean n → ENNReal) : Prop :=
  ∀ x y, ‖x‖ ≤ ‖y‖ → g y ≤ g x

/-- Positive strict superlevel sets of `f` and `g` have equal volume. -/
def Equimeasurable {n : Nat} (f g : Euclidean n → ENNReal) : Prop :=
  ∀ t : ENNReal, 0 < t →
    volume {x | t < g x} = volume {x | t < f x}

/-- The canonical Schwarz symmetric decreasing rearrangement target.

The `ENNReal` codomain represents nonnegativity intrinsically. The finiteness
hypothesis is imposed exactly on positive strict superlevel sets. The witness
is required to be measurable, radial, radially nonincreasing, and
equimeasurable with the input.
-/
def SchwarzRearrangementTarget : Prop :=
  ∀ (n : Nat), 0 < n → ∀ f : Euclidean n → ENNReal,
    Measurable f →
      (∀ t : ENNReal, 0 < t → volume {x | t < f x} ≠ ∞) →
        ∃ fstar : Euclidean n → ENNReal,
          Measurable fstar ∧ IsRadial fstar ∧
            IsRadiallyNonincreasing fstar ∧ Equimeasurable f fstar

/-- The same target with equimeasurability expanded at the use site. -/
def ExpandedTarget : Prop :=
  ∀ (n : Nat), 0 < n → ∀ f : Euclidean n → ENNReal,
    Measurable f →
      (∀ t : ENNReal, 0 < t → volume {x | t < f x} ≠ ∞) →
        ∃ fstar : Euclidean n → ENNReal,
          Measurable fstar ∧ IsRadial fstar ∧
            IsRadiallyNonincreasing fstar ∧
              ∀ t : ENNReal, 0 < t →
                volume {x | t < fstar x} = volume {x | t < f x}

/-- Checked definitional transport to the expanded encoding. -/
theorem schwarzRearrangementTarget_iff_expandedTarget :
    SchwarzRearrangementTarget ↔ ExpandedTarget :=
  Iff.rfl

-- Structural mutations, elaborated separately and compared by the validator.
def mutationIncludesDimensionZero : Prop :=
  ∀ (n : Nat) (f : Euclidean n → ENNReal),
    Measurable f →
      (∀ t : ENNReal, 0 < t → volume {x | t < f x} ≠ ∞) →
        ∃ fstar : Euclidean n → ENNReal,
          Measurable fstar ∧ IsRadial fstar ∧
            IsRadiallyNonincreasing fstar ∧ Equimeasurable f fstar

def mutationRemovedFiniteSuperlevels : Prop :=
  ∀ (n : Nat), 0 < n → ∀ f : Euclidean n → ENNReal,
    Measurable f → ∃ fstar : Euclidean n → ENNReal,
      Measurable fstar ∧ IsRadial fstar ∧
        IsRadiallyNonincreasing fstar ∧ Equimeasurable f fstar

def mutationUsesNonStrictSuperlevels : Prop :=
  ∀ (n : Nat), 0 < n → ∀ f : Euclidean n → ENNReal,
    Measurable f →
      (∀ t : ENNReal, 0 < t → volume {x | t ≤ f x} ≠ ∞) →
        ∃ fstar : Euclidean n → ENNReal,
          Measurable fstar ∧ IsRadial fstar ∧ IsRadiallyNonincreasing fstar ∧
            ∀ t : ENNReal, 0 < t →
              volume {x | t ≤ fstar x} = volume {x | t ≤ f x}

def mutationRemovedRadialMonotonicity : Prop :=
  ∀ (n : Nat), 0 < n → ∀ f : Euclidean n → ENNReal,
    Measurable f →
      (∀ t : ENNReal, 0 < t → volume {x | t < f x} ≠ ∞) →
        ∃ fstar : Euclidean n → ENNReal,
          Measurable fstar ∧ IsRadial fstar ∧ Equimeasurable f fstar

end Stage1Instances.THM_M_1285

set_option pp.explicit true in
#print Stage1Instances.THM_M_1285.SchwarzRearrangementTarget
