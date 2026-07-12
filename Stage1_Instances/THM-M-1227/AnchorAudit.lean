import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Distribution.TestFunction
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar

/-!
# THM-M-1227 immutable mathlib anchor audit

These probes identify substrate available at the pinned mathlib revision. They do not state or
prove Leray-Hopf existence. In particular, `TestFunction` is infrastructure for distributions and
weak PDE formulations, not a terminal Navier-Stokes theorem.
-/

open MeasureTheory

namespace Stage1.THM_M_1227.AnchorAudit

#check fderiv
#check integral
#check MeasureTheory.Integrable
#check HasCompactSupport
#check ContDiff
#check TestFunction
#check MeasureTheory.volume
#check Measure.restrict

/-- The audited mathlib surface supplies the finite-dimensional space used by the frozen target. -/
example : Nonempty (Fin 3 -> Real) :=
  inferInstance

/-- The audit's terminal-candidate count is zero; this is metadata, not a proof by absence. -/
def terminalMathlibCandidates : List Lean.Name := []

theorem terminalMathlibCandidates_length :
    (terminalMathlibCandidates : List Lean.Name).length = 0 := by
  rfl

end Stage1.THM_M_1227.AnchorAudit
