import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace

import Statement

/-!
# THM-M-1520 conditional root composition

This file checks the final interface only. `LiouvilleAnalyticPackage` is an explicit
premise standing for the open analytic obligation tree; it is not a proof of that
package.
-/

open MeasureTheory

namespace Stage1.THM_M_1520

/-- The result delivered by the analytic subtree, before unfolding the public root. -/
def LiouvilleAnalyticPackage : Prop :=
  forall (n : Nat) (H : PhaseSpace n -> Real) (Phi : Real -> PhaseSpace n -> PhaseSpace n),
    ContDiff Real 2 H ->
    (forall z, ContDiff Real 1 (fun t => Phi t z)) ->
    (forall t z, HasDerivAt (fun s => Phi s z) (hamiltonianVectorField H (Phi t z)) t) ->
    (forall z, Phi 0 z = z) ->
    (forall s t z, Phi (s + t) z = Phi s (Phi t z)) ->
    forall t, MeasurePreserving (Phi t) volume volume

/-- Exact conditional composition. The substantive analytic package remains a premise. -/
theorem liouvilleStatement_of_analyticPackage
    (analytic : LiouvilleAnalyticPackage) : LiouvilleStatement := by
  exact analytic

#print axioms liouvilleStatement_of_analyticPackage

end Stage1.THM_M_1520
