import Mathlib.Algebra.ContinuedFractions.Computation.Basic
import Mathlib.Analysis.Analytic.Composition
import Mathlib.Dynamics.FixedPoints.Basic
import Mathlib.NumberTheory.DiophantineApproximation.ContinuedFractions

/-!
# THM-M-1433 discovery-only intake probe

These checks authenticate adjacent pinned continued-fraction, analytic, fixed-point, and conjugacy
APIs. They neither define the Brjuno condition nor select or prove a linearization theorem.
-/

#check GenContFract.of
#check GenContFract.dens
#check GenContFract.convs
#check Real.convergent
#check Real.convs_eq_convergent
#check AnalyticAt
#check AnalyticAt.comp
#check Function.IsFixedPt
#check Function.Semiconj
#check Function.Semiconj.iterate_right
