import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.Analysis.ODE.Basic
import Mathlib.Dynamics.Flow
import Mathlib.LinearAlgebra.SymplecticGroup
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace

/-!
# THM-M-1375 discovery-only intake probe

These checks authenticate adjacent pinned smoothness, Hamiltonian-coordinate, flow, symplectic,
volume, and measure-preservation APIs. They do not choose an exact Liouville statement, import the
separately owned THM-M-1520 statement, establish a source transport, or prove THM-M-1375.
-/

open MeasureTheory
open scoped ContDiff

#check ContDiff
#check gradient
#check IsIntegralCurve
#check Flow
#check Flow.orbit
#check volume
#check MeasurePreserving
#check MeasurePreserving.map_eq
#check Matrix.symplecticGroup
#check SymplecticGroup.symplectic_det
