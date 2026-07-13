import Mathlib.Combinatorics.SimpleGraph.Hamiltonian

/-!
# THM-M-0853 discovery-only intake probe

These checks authenticate pinned finite-graph degree and Hamiltonicity interfaces and verify that
several conventional Dirac-statement shapes are expressible. They do not select a canonical source
statement and contain no theorem proof.
-/

#check SimpleGraph.degree
#check SimpleGraph.minDegree
#check SimpleGraph.minDegree_le_degree
#check SimpleGraph.le_minDegree_of_forall_le_degree
#check SimpleGraph.minDegree_lt_card
#check SimpleGraph.Walk.IsHamiltonianCycle
#check SimpleGraph.IsHamiltonian
#check SimpleGraph.IsHamiltonian.mono
#check SimpleGraph.not_isHamiltonian_of_isEmpty
#check SimpleGraph.IsHamiltonian.of_card_eq_one
#check SimpleGraph.not_isHamiltonian_of_card_eq_two

universe u

namespace Stage1Instances.THM_M_0853

section CandidateShapes

variable {V : Type u} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]

-- Twice-degree spelling, avoiding a silent floor division for odd graph orders.
#check (3 <= Fintype.card V ->
  Fintype.card V <= 2 * G.minDegree -> G.IsHamiltonian)

-- Ceiling-style natural-number spelling of the usual half-order lower bound.
#check (3 <= Fintype.card V ->
  (Fintype.card V + 1) / 2 <= G.minDegree -> G.IsHamiltonian)

-- Floor spelling, checked only to expose that it is a distinct candidate.
#check (3 <= Fintype.card V ->
  Fintype.card V / 2 <= G.minDegree -> G.IsHamiltonian)

-- Pointwise twice-degree spelling, avoiding a minimum-degree normalization choice.
#check (3 <= Fintype.card V ->
  (forall v, Fintype.card V <= 2 * G.degree v) -> G.IsHamiltonian)

end CandidateShapes

end Stage1Instances.THM_M_0853
