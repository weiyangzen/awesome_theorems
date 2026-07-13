import Proof

/-!
# THM-M-1141 validation probes

This module adds no analytic Harnack proof. It checks the exact frozen root
expression and rechecks the two proof-phase bookkeeping packages through
separately written bodies over the imported proof interfaces. These are
same-worker, import-dependent probes, not independent implementations. The
local Harnack estimate, compact chain, uniform comparison, and root remain open.
-/

open Set
open InnerProductSpace

namespace Stage1Instances.THM_M_1141.Validation

open Stage1Instances.THM_M_1141

/-- A second exact-type check of positivity and denominator nonvanishing on the
compact subset. This is same-worker, import-dependent evidence only. -/
theorem positiveDenominatorsDirect
    {n : Nat} {Omega K : Set (Space n)} {u : Space n -> Real}
    (hKOmega : Set.Subset K Omega)
    (hupos : forall z : Space n, Omega z -> 0 < u z) :
    forall x : Space n, K x -> And (0 < u x) (Not (u x = 0)) := by
  intro x hx
  have hux : 0 < u x := hupos x (hKOmega hx)
  exact And.intro hux (ne_of_gt hux)

/-- A second exact-type induction over the proof module's chain interface. It
deliberately proves only the abstract propagation package. -/
theorem comparisonChainEndpointDirect {alpha : Type*} {u : alpha -> Real}
    {A : Real} (hA : 1 <= A) {x z : alpha} {points : List alpha}
    (chain : ComparisonChain A u x points z) :
    SymmetricComparison (A ^ points.length) u x z := by
  induction chain with
  | nil x =>
      exact And.intro (by simp) (by simp)
  | @cons x y z tail hxy chain ih =>
      rw [List.length_cons, pow_succ']
      exact hxy.trans (by linarith) (by positivity) ih

#check HarnackInequality
#check UniformValueComparison
#check harnackInequality_of_analytic_package

#print axioms positiveDenominatorsDirect
#print axioms comparisonChainEndpointDirect
#print axioms harnackInequality_of_analytic_package

end Stage1Instances.THM_M_1141.Validation
