import ObligationTree

/-!
# THM-M-1026 differential validation probe

This module deliberately does not import `Proof`. It reconstructs the complete
stable-law-to-attraction branch from the frozen statement and independently
checks the branch interface. The generalized-CLT necessity direction remains
an explicit open obligation.
-/

noncomputable section

open Filter MeasureTheory

namespace Stage1Instances.THM_M_1026.Validation

/-- Stability supplies total positive normalizers, with harmless defaults at
the two indices ignored by convergence at `atTop`. -/
theorem independentlyReconstructedStableNormalizers
    {nu : Measure Real} (hstable : IsStableLaw nu) :
    exists a b : Nat -> Real, (forall n, 0 < a n) /\
      forall n, 2 <= n -> normalizedLaw (convPow nu n) (a n) (b n) = nu := by
  choose a b hab using hstable.2.2
  let scale : Nat -> Real := fun n => if hn : 2 <= n then a n hn else 1
  let center : Nat -> Real := fun n => if hn : 2 <= n then b n hn else 0
  refine ⟨scale, center, ?_, ?_⟩
  · intro n
    by_cases hn : 2 <= n
    · simpa [scale, hn] using (hab n hn).1
    · simp [scale, hn]
  · intro n hn
    simpa [scale, center, hn] using (hab n hn).2

/-- Eventual equality to a fixed measure implies the frozen bounded-test weak
convergence predicate. -/
theorem independentlyReconstructedWeakLimit
    {mu : Nat -> Measure Real} {nu : Measure Real}
    (hmu : forall n, 2 <= n -> mu n = nu) : WeaklyConverges mu nu := by
  intro f
  refine Filter.Tendsto.congr' ?_
    (tendsto_const_nhds : Tendsto (fun _ : Nat => ∫ x, f x ∂nu) atTop
      (nhds (∫ x, f x ∂nu)))
  filter_upwards [eventually_ge_atTop 2] with n hn
  rw [hmu n hn]

/-- Differential reconstruction of the exact frozen converse terminal. -/
theorem independentlyReconstructedConverse :
    Stage1Instances.THM_M_1026.ObligationTree.ConverseTerminal := by
  intro nu hprob _ hstable
  obtain ⟨a, b, ha, hab⟩ := independentlyReconstructedStableNormalizers hstable
  refine ⟨nu, hprob, a, b, ha, ?_⟩
  exact independentlyReconstructedWeakLimit hab

/-- Conditional exact-root reconstruction which keeps the unproved necessity
direction visible as a premise while independently recomposing the biconditional. -/
theorem independentlyReconstructedConditionalRoot
    (necessity : Stage1Instances.THM_M_1026.ObligationTree.NecessityTerminal) :
    Stage1Instances.THM_M_1026.Statement := by
  intro nu hprob hnondeg
  exact ⟨independentlyReconstructedConverse nu hprob hnondeg,
    necessity nu hprob hnondeg⟩

#print axioms independentlyReconstructedStableNormalizers
#print axioms independentlyReconstructedWeakLimit
#print axioms independentlyReconstructedConverse
#print axioms independentlyReconstructedConditionalRoot

end Stage1Instances.THM_M_1026.Validation
