import Statement
import ObligationTree

/-!
# THM-M-0983 proof-phase bodies

This module discharges the three substantive packages in the frozen obligation
tree from the pinned mathlib strong law, composes them, and proves the exact
statement-phase target.  The Bernoulli-value premise is retained at the target
boundary although the more general real-valued strong law does not need it.
-/

noncomputable section

open MeasureTheory Filter Finset
open scoped BigOperators MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THM_M_0983_Obligations

universe u

/-- Joint independence projects to the pairwise independence consumed by the
pinned real strong law. -/
theorem pairwiseProjection_proof : PairwiseProjectionPackage.{u} := by
  intro Omega _ mu X hindep i j hij
  exact hindep.indepFun hij

/-- The pinned mathlib real strong law has exactly the analytic conclusion in
the frozen strong-law package. -/
theorem strongLaw_proof : StrongLawPackage.{u} := by
  intro Omega _ mu X hint hpair hident
  simpa [empiricalFrequency] using
    (ProbabilityTheory.strong_law_ae_real X hint hpair hident)

/-- Rewrite the almost-sure limit along the supplied expectation equation. -/
theorem expectationTransport_proof : ExpectationTransportPackage.{u} := by
  intro Omega _ mu X p hexpect hlimit
  simpa [hexpect] using hlimit

/-- All logical packages in the frozen proof graph compose without any open
premise. -/
theorem obligationTarget_proof : Target.{u} :=
  root_of_packages pairwiseProjection_proof strongLaw_proof
    expectationTransport_proof

#print axioms pairwiseProjection_proof
#print axioms strongLaw_proof
#print axioms expectationTransport_proof
#print axioms obligationTarget_proof

end Stage1Instances.THM_M_0983_Obligations

namespace Stage1Instances.THM_M_0983

universe u

/-- Placeholder-free proof of the exact proposition frozen in `Statement.lean`.
The unused Bernoulli premise only specializes mathlib's more general IID real
strong law; it is not removed from or weakened in the public target. -/
theorem bernoulliStrongLaw_proof : BernoulliStrongLawTarget.{u} := by
  intro Omega _ mu _ X p hint hindep hident _hBernoulli hexpect
  have hpair : Pairwise (Function.onFun (fun f g => f ⟂ᵢ[mu] g) X) := by
    intro i j hij
    exact hindep.indepFun hij
  have hlimit :=
    ProbabilityTheory.strong_law_ae_real X hint hpair hident
  filter_upwards [hlimit] with omega homega
  simpa [empiricalFrequency, hexpect] using homega

#print axioms bernoulliStrongLaw_proof

end Stage1Instances.THM_M_0983
