import Statement

/-!
# THM-M-0487 conditional obligation composition

This module checks the exact cutoff transports and child-to-root composition frozen by registry
version 1. The analytic and finite-range packages are explicit premises. No implementation of
either deep package, finite certificate, or unbounded weak Goldbach proof is supplied here.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0487.ObligationTree

/-- Canonical witness predicate used by both range packages. -/
def ThreePrimeRepresentation (n : Nat) : Prop :=
  exists p q r : Nat,
    Nat.Prime p ∧ Nat.Prime q ∧ Nat.Prime r ∧ n = p + q + r

/-- First input handled by the source's analytic argument. -/
def analyticCutoff : Nat := 10 ^ 27

/-- Exact inclusive upper endpoint reported by the Helfgott-Platt finite result. -/
def publishedFiniteUpper : Nat := 8875694145621773516800000000000

/-- The open analytic child, including the cutoff endpoint. -/
def AnalyticRangePackage : Prop :=
  forall n : Nat, analyticCutoff ≤ n -> Odd n -> ThreePrimeRepresentation n

/-- The open finite child needed by the root composition. -/
def FiniteRangePackage : Prop :=
  forall n : Nat, 5 < n -> n < analyticCutoff -> Odd n -> ThreePrimeRepresentation n

/-- Exact exhaustive cutoff split consumed by the root composition. -/
def CutoffPartitionPackage : Prop :=
  forall n : Nat, n < analyticCutoff ∨ analyticCutoff ≤ n

/-- Exact mathematical interval interface claimed by the finite-source lead. -/
def FiniteUpperBoundPackage : Prop :=
  forall n : Nat, 5 < n -> n ≤ publishedFiniteUpper -> Odd n ->
    ThreePrimeRepresentation n

/-- Exact inclusion needed to restrict the published interval to the root's finite side. -/
def FiniteCoveragePackage : Prop :=
  forall n : Nat, n < analyticCutoff -> n ≤ publishedFiniteUpper

/-- The local witness predicate is definitionally the canonical existential conclusion. -/
theorem threePrimeRepresentation_iff (n : Nat) :
    ThreePrimeRepresentation n <->
      exists p q r : Nat,
        Nat.Prime p ∧ Nat.Prime q ∧ Nat.Prime r ∧ n = p + q + r :=
  Iff.rfl

/-- Every input lies in exactly the finite side or the inclusive analytic side. -/
theorem cutoff_cases : CutoffPartitionPackage :=
  fun n => lt_or_ge n analyticCutoff

/-- The analytic cutoff lies strictly above the root's lower boundary. -/
theorem five_lt_analyticCutoff : 5 < analyticCutoff := by
  decide

/-- Kernel-checked decimal endpoint fact; it does not validate the published computation. -/
theorem analyticCutoff_le_publishedFiniteUpper :
    analyticCutoff ≤ publishedFiniteUpper := by
  decide

/-- Checked normalization showing that the published interval contains the finite cutoff side. -/
theorem finiteCoverage_of_publishedUpper : FiniteCoveragePackage := by
  intro n hcutoff
  exact le_trans (Nat.le_of_lt hcutoff) analyticCutoff_le_publishedFiniteUpper

/-- Checked restriction from the exact coverage child and upper theorem to the finite child. -/
theorem finiteRange_of_publishedFiniteUpper
    (coverage : FiniteCoveragePackage)
    (finiteUpper : FiniteUpperBoundPackage) : FiniteRangePackage := by
  intro n hn hcutoff hodd
  exact finiteUpper n hn (coverage n hcutoff) hodd

/-- Checked exhaustive, disjoint cutoff recomposition into the exact frozen target. -/
theorem root_of_analytic_and_finite
    (cutoffPartition : CutoffPartitionPackage)
    (analytic : AnalyticRangePackage)
    (finite : FiniteRangePackage) :
    Stage1Instances.THM_M_0487.WeakGoldbachTarget := by
  intro n hn hodd
  rcases cutoffPartition n with hfinite | hanalytic
  · exact finite n hn hfinite hodd
  · exact analytic n hanalytic hodd

/-- The two range children are an exact logical decomposition of the frozen root. -/
theorem root_iff_analytic_and_finite :
    Stage1Instances.THM_M_0487.WeakGoldbachTarget <->
      AnalyticRangePackage ∧ FiniteRangePackage := by
  constructor
  · intro root
    constructor
    · intro n hcutoff hodd
      exact root n (lt_of_lt_of_le five_lt_analyticCutoff hcutoff) hodd
    · intro n hn _ hodd
      exact root n hn hodd
  · rintro ⟨analytic, finite⟩
    exact root_of_analytic_and_finite cutoff_cases analytic finite

#check threePrimeRepresentation_iff
#check cutoff_cases
#check analyticCutoff_le_publishedFiniteUpper
#check finiteCoverage_of_publishedUpper
#check finiteRange_of_publishedFiniteUpper
#check root_of_analytic_and_finite
#check root_iff_analytic_and_finite
#print axioms threePrimeRepresentation_iff
#print axioms cutoff_cases
#print axioms analyticCutoff_le_publishedFiniteUpper
#print axioms finiteCoverage_of_publishedUpper
#print axioms finiteRange_of_publishedFiniteUpper
#print axioms root_of_analytic_and_finite
#print axioms root_iff_analytic_and_finite

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0487.WeakGoldbachTarget

end Stage1Instances.THM_M_0487.ObligationTree
