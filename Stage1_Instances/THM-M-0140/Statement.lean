import Mathlib.GroupTheory.Coxeter.Length

/-!
# THM-M-0140 statement diagnostic

This module checks the smallest pinned Coxeter-system API currently available
for the intended Kazhdan-Lusztig basis theorem. It deliberately declares no
canonical target: the source, Hecke-algebra, coefficient, and normalization
conventions needed to identify that target are unresolved.
-/

namespace Stage1Instances.THM_M_0140

#check CoxeterMatrix
#check CoxeterSystem
#check CoxeterSystem.simple
#check CoxeterSystem.wordProd
#check CoxeterSystem.length
#check CoxeterSystem.IsReduced

end Stage1Instances.THM_M_0140
