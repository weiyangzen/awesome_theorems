import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.Calculus.LocalExtr.Rolle
import Mathlib.LinearAlgebra.LinearIndependent.Lemmas
import Mathlib.Topology.Order.IntermediateValue

/-!
# THM-M-1386 discovery-only intake probe

These checks authenticate pinned calculus, order, and linear-independence interfaces adjacent to a
possible future encoding of Sturm's separation theorem. They neither select the catalog's exact
differential-equation contract nor state or prove THM-M-1386.
-/

#check HasDerivAt.mul
#check HasDerivAt.sub
#check HasDerivAt.div
#check LinearIndependent.pair_iff
#check strictMonoOn_of_hasDerivWithinAt_pos
#check strictAntiOn_of_hasDerivWithinAt_neg
#check intermediate_value_Ioo
#check exists_hasDerivAt_eq_zero
