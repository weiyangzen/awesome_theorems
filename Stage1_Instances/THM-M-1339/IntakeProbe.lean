import Mathlib.Analysis.ODE.PicardLindelof

/-!
# THM-M-1339 discovery-only intake probe

These checks authenticate the pinned Picard-Lindelof assumption package and its initial-state
Lipschitz/joint-continuity local-flow results. They do not select the catalog's exact statement,
encode an external parameter, or claim a proof of THM-M-1339.
-/

#check IsPicardLindelof
#check IsPicardLindelof.exists_forall_mem_closedBall_eq_hasDerivWithinAt_lipschitzOnWith
#check IsPicardLindelof.exists_forall_mem_closedBall_eq_hasDerivWithinAt_continuousOn

#print axioms IsPicardLindelof.exists_forall_mem_closedBall_eq_hasDerivWithinAt_lipschitzOnWith
#print axioms IsPicardLindelof.exists_forall_mem_closedBall_eq_hasDerivWithinAt_continuousOn
