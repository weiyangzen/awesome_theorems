import Mathlib.Combinatorics.SimpleGraph.Coloring
import Mathlib.Data.Fintype.Powerset

/-!
# THM-M-0967 discovery-only intake probe

These checks authenticate the pinned fixed-cardinality finite-subset and graph-coloring interfaces
adjacent to a future Kneser-graph encoding. `CandidateKneserGraph` is only a definition used to
check that the standard disjointness graph can be represented. It is not the canonical target, a
statement-gate certificate, or a proof of the named theorem.
-/

namespace Stage1Instances.THM_M_0967.Intake

/-- Candidate graph shape: `k`-subsets of `Fin n`, adjacent exactly when disjoint. -/
def CandidateKneserGraph (n k : Nat) : SimpleGraph {s : Finset (Fin n) // s.card = k} :=
  SimpleGraph.fromRel fun s t => Disjoint s.1 t.1

#check Finset.powersetCard
#check Finset.mem_powersetCard
#check Finset.mem_powersetCard_univ
#check Fintype.card_finset_len
#check Finset.disjoint_left
#check SimpleGraph.fromRel
#check SimpleGraph.fromRel_adj
#check SimpleGraph.Coloring
#check SimpleGraph.Colorable
#check SimpleGraph.chromaticNumber
#check SimpleGraph.chromaticNumber_eq_iff_colorable_not_colorable
#check CandidateKneserGraph

#print axioms Finset.mem_powersetCard_univ
#print axioms SimpleGraph.fromRel_adj
#print axioms SimpleGraph.chromaticNumber_eq_iff_colorable_not_colorable

end Stage1Instances.THM_M_0967.Intake
