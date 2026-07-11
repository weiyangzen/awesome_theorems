import Mathlib.GroupTheory.Coxeter.Length

/-!
# THM-M-0140 statement infrastructure

This module checks only the Coxeter-system objects available in the pinned
environment. It deliberately declares no Kazhdan-Lusztig target: the source
and coefficient conventions needed to identify that target are not yet
frozen.
-/

namespace Stage1Instances.THMM0140

#check CoxeterMatrix
#check CoxeterSystem
#check CoxeterSystem.simple
#check CoxeterSystem.wordProd
#check CoxeterSystem.length
#check CoxeterSystem.IsReduced

end Stage1Instances.THMM0140
