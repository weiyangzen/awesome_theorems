import Mathlib.Tactic.Linarith.Oracle.SimplexAlgorithm

/-!
# THM-M-1493 discovery-only intake probe

These checks authenticate pinned rational matrix, tableau, pivot-loop, LP reduction, and linarith
certificate-oracle interfaces adjacent to a future source-selected simplex-method theorem. They do
not select the catalog's exact proposition or prove general LP correctness, completeness,
termination, optimality, infeasibility detection, unboundedness detection, or complexity.
-/

#check Mathlib.Tactic.Linarith.SimplexAlgorithm.DenseMatrix
#check Mathlib.Tactic.Linarith.SimplexAlgorithm.SparseMatrix
#check Mathlib.Tactic.Linarith.SimplexAlgorithm.Tableau
#check Mathlib.Tactic.Linarith.SimplexAlgorithm.doPivotOperation
#check Mathlib.Tactic.Linarith.SimplexAlgorithm.checkSuccess
#check Mathlib.Tactic.Linarith.SimplexAlgorithm.chooseEnteringVar
#check Mathlib.Tactic.Linarith.SimplexAlgorithm.chooseExitingVar
#check Mathlib.Tactic.Linarith.SimplexAlgorithm.choosePivots
#check Mathlib.Tactic.Linarith.SimplexAlgorithm.runSimplexAlgorithm
#check Mathlib.Tactic.Linarith.SimplexAlgorithm.stateLP
#check Mathlib.Tactic.Linarith.SimplexAlgorithm.extractSolution
#check Mathlib.Tactic.Linarith.SimplexAlgorithm.findPositiveVector
#check Mathlib.Tactic.Linarith.CertificateOracle.simplexAlgorithmSparse
#check Mathlib.Tactic.Linarith.CertificateOracle.simplexAlgorithmDense
