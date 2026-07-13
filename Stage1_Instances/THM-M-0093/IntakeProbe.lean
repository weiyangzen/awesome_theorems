import Mathlib.Algebra.Lie.Semisimple.Defs
import Mathlib.Algebra.Lie.UniversalEnveloping
import Mathlib.Algebra.Lie.Weights.RootSystem

/-!
# THM-M-0093 discovery-only intake probe

These checks authenticate adjacent pinned semisimple Lie algebra, Cartan, weight-space, root-system,
and universal-enveloping-algebra APIs. They do not define dominant integral highest weights, select
a highest-weight classification statement, or prove THM-M-0093.
-/

#check LieAlgebra.IsSemisimple
#check LieSubalgebra.IsCartanSubalgebra
#check LieModule.IsIrreducible
#check LieModule.weightSpace
#check LieModule.genWeightSpace
#check LieModule.Weight
#check LieModule.iSup_genWeightSpace_eq_top
#check LieAlgebra.rootSpace
#check LieAlgebra.IsKilling.rootSystem
#check UniversalEnvelopingAlgebra
#check LieSubmodule
