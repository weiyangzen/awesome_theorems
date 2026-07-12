import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic

/-!
# THM-M-1200: exact Rankine-Hugoniot statement

This module freezes the weak interface-defect formulation selected at intake.
It contains no proof of the Rankine-Hugoniot theorem.
-/

namespace Stage1Instances.THM_M_1200

open MeasureTheory

/-- The coefficient of the distribution supported on the straight interface
`x = s * t` for the two constant states. -/
def jumpCoefficient (f : Real → Real) (uL uR s : Real) : Real :=
  f uR - f uL - s * (uR - uL)

/-- The weak interface defect paired with a spacetime test function. -/
noncomputable def interfaceDefect
    (f : Real → Real) (uL uR s : Real) (phi : Real × Real → Real) : Real :=
  jumpCoefficient f uL uR s * ∫ t : Real, phi (t, s * t)

/-- The discontinuity has zero weak defect against every smooth compactly
supported spacetime test function. -/
def InterfaceDefectVanishes (f : Real → Real) (uL uR s : Real) : Prop :=
  ∀ phi : Real × Real → Real,
    ContDiff Real ⊤ phi → HasCompactSupport phi →
      interfaceDefect f uL uR s phi = 0

/-- The canonical scalar, one-dimensional Rankine-Hugoniot target. -/
def RankineHugoniotTarget : Prop :=
  ∀ (f : Real → Real) (uL uR s : Real),
    InterfaceDefectVanishes f uL uR s ↔
      s * (uR - uL) = f uR - f uL

/-- The same jump law written as equality of the flux in the moving frame. -/
def MovingFrameFluxTarget : Prop :=
  ∀ (f : Real → Real) (uL uR s : Real),
    InterfaceDefectVanishes f uL uR s ↔
      f uR - s * uR = f uL - s * uL

/-- Checked transport to the moving-frame-flux encoding. -/
theorem rankineHugoniotTarget_iff_movingFrameFluxTarget :
    RankineHugoniotTarget ↔ MovingFrameFluxTarget := by
  simp only [RankineHugoniotTarget, MovingFrameFluxTarget]
  constructor <;> intro h f uL uR s
  · rw [h]
    constructor <;> intro equality <;> linarith
  · rw [h]
    constructor <;> intro equality <;> linarith

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationOnlyForwardDirection : Prop :=
  ∀ (f : Real → Real) (uL uR s : Real),
    InterfaceDefectVanishes f uL uR s →
      s * (uR - uL) = f uR - f uL

def mutationStationaryInterface : Prop :=
  ∀ (f : Real → Real) (uL uR : Real),
    InterfaceDefectVanishes f uL uR 0 ↔ f uR = f uL

def mutationNondegenerateStatesOnly : Prop :=
  ∀ (f : Real → Real) (uL uR s : Real), uL ≠ uR →
    (InterfaceDefectVanishes f uL uR s ↔
      s * (uR - uL) = f uR - f uL)

def mutationFluxQuantifiedAfterStates : Prop :=
  ∀ (uL uR s : Real), ∀ f : Real → Real,
    InterfaceDefectVanishes f uL uR s ↔
      s * (uR - uL) = f uR - f uL

/-- Equal states have zero interface coefficient for every speed and flux. -/
theorem equal_states_boundary (f : Real → Real) (u s : Real) :
    jumpCoefficient f u u s = 0 := by
  simp [jumpCoefficient]

/-- Changing a test function only on the interface is invisible whenever the
two interface traces agree pointwise. -/
theorem interface_representative_boundary
    (f : Real → Real) (uL uR s : Real) (phi psi : Real × Real → Real)
    (h : ∀ t : Real, phi (t, s * t) = psi (t, s * t)) :
    interfaceDefect f uL uR s phi = interfaceDefect f uL uR s psi := by
  simp only [interfaceDefect]
  congr 1
  apply integral_congr_ae
  filter_upwards [] with t
  exact h t

end Stage1Instances.THM_M_1200

set_option pp.explicit true in
#print Stage1Instances.THM_M_1200.RankineHugoniotTarget
