import Mathlib.Analysis.Matrix.PosDef
import Mathlib.Combinatorics.SimpleGraph.Clique
import Mathlib.Combinatorics.SimpleGraph.LapMatrix

/-!
# THM-M-0890 pinned formal-anchor audit

These declarations are the retained pinned interfaces nearest to Hoffman's ratio bound. They
provide independent-set extrema, regular adjacency action, ordered Hermitian eigenvalues, and
positive-semidefinite quadratic forms. None states the ratio bound, and this module deliberately
contains no theorem purporting to prove the frozen target.
-/

namespace Stage1Instances.THM_M_0890.AnchorAudit

#check SimpleGraph.indepNum
#check SimpleGraph.IsIndepSet.card_le_indepNum
#check SimpleGraph.exists_isNIndepSet_indepNum
#check SimpleGraph.maximumIndepSet_card_eq_indepNum
#check SimpleGraph.IsRegularOfDegree
#check SimpleGraph.adjMatrix_mulVec_const_apply_of_regular
#check SimpleGraph.isHermitian_adjMatrix
#check Matrix.IsHermitian.eigenvalues₀
#check Matrix.IsHermitian.eigenvalues₀_antitone
#check Matrix.PosSemidef.submatrix
#check Matrix.posSemidef_iff_dotProduct_mulVec
#check Matrix.IsHermitian.posSemidef_iff_eigenvalues_nonneg

#print axioms SimpleGraph.IsIndepSet.card_le_indepNum
#print axioms SimpleGraph.exists_isNIndepSet_indepNum
#print axioms SimpleGraph.maximumIndepSet_card_eq_indepNum
#print axioms SimpleGraph.adjMatrix_mulVec_const_apply_of_regular
#print axioms Matrix.IsHermitian.eigenvalues₀_antitone
#print axioms Matrix.PosSemidef.submatrix
#print axioms Matrix.posSemidef_iff_dotProduct_mulVec
#print axioms Matrix.IsHermitian.posSemidef_iff_eigenvalues_nonneg

/-! Scope guards: the retained interfaces stop strictly below the target. -/

example {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] (k : Nat) (hreg : G.IsRegularOfDegree k) (v : V) :
    (G.adjMatrix Real).mulVec (Function.const V 1) v = k := by
  simpa using
    (SimpleGraph.adjMatrix_mulVec_const_apply_of_regular (G := G) (a := (1 : Real)) hreg)

example {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] : Antitone (G.isHermitian_adjMatrix Real).eigenvalues₀ :=
  (G.isHermitian_adjMatrix Real).eigenvalues₀_antitone

end Stage1Instances.THM_M_0890.AnchorAudit
