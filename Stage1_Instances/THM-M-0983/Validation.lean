import Statement

/-!
# THM-M-0983 independent validation probe

This module reconstructs the exact frozen target directly from the pinned
mathlib theorem.  It deliberately does not import `Proof.lean` or
`ObligationTree.lean`.
-/

noncomputable section

open MeasureTheory Filter Finset
open scoped BigOperators MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THM_M_0983.Validation

universe u

theorem independentlyReconstructedTarget :
    Stage1Instances.THM_M_0983.BernoulliStrongLawTarget.{u} := by
  intro Omega _ mu _ X p hint hindep hident _hBernoulli hexpect
  have hpair : Pairwise (Function.onFun (fun f g => f ⟂ᵢ[mu] g) X) :=
    fun _ _ hij => hindep.indepFun hij
  have hlimit := ProbabilityTheory.strong_law_ae_real X hint hpair hident
  simpa [Stage1Instances.THM_M_0983.empiricalFrequency, hexpect] using hlimit

#print axioms independentlyReconstructedTarget

end Stage1Instances.THM_M_0983.Validation
