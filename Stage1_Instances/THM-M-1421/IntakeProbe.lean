import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Dynamics.Ergodic.MeasurePreserving
import Mathlib.Dynamics.TopologicalEntropy.CoverEntropy
import Mathlib.Geometry.Manifold.MFDeriv.Defs
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
Discovery-only API checks for a later exact Pesin entropy formula statement.
`Dynamics.coverEntropy` is topological entropy and is checked to document a
nonmatching boundary, not as a substitute for metric entropy.
-/

open MeasureTheory
open scoped BigOperators

#check MeasurePreserving
#check MeasurePreserving.iterate
#check Dynamics.coverEntropy
#check mfderiv
#check integral
#check integral_congr_ae
#check Finset.sum
#check Finset.sum_empty
