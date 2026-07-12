import Mathlib.Analysis.Convex.StdSimplex
import Mathlib.Probability.ProbabilityMassFunction.Basic
import Mathlib.Topology.Semicontinuity.Hemicontinuity

/-!
Discovery-only checks for APIs adjacent to the THM-M-1512 source family.

These declarations do not define a game, best response, or Nash equilibrium, and mathlib's generic
hemicontinuity interface is not Kakutani's fixed-point theorem. They provide no statement or proof
credit for THM-M-1512.
-/

#check stdSimplex
#check convex_stdSimplex
#check isCompact_stdSimplex
#check PMF
#check PMF.hasSum_coe_one
#check UpperHemicontinuous
#check UpperHemicontinuousAt.mem_of_tendsto
#check Function.IsFixedPt
