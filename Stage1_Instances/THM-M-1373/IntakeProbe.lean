import Mathlib.Analysis.ODE.Basic
import Mathlib.Dynamics.Flow
import Mathlib.LinearAlgebra.SymplecticGroup

/-!
# THM-M-1373 discovery-only intake probe

These checks authenticate pinned ODE, flow, canonical symplectic-matrix, and symplectic-group
interfaces adjacent to possible Hamiltonian-system encodings. They do not choose a mathematical
proposition, define a Hamiltonian system, or prove THM-M-1373.
-/

#check IsIntegralCurveOn
#check IsIntegralCurveAt
#check IsIntegralCurve
#check Flow
#check Flow.orbit
#check HasDerivWithinAt
#check Matrix.mulVec
#check Matrix.J
#check Matrix.J_transpose
#check Matrix.J_squared
#check Matrix.symplecticGroup
#check SymplecticGroup.J_mem
#check SymplecticGroup.symplectic_det
