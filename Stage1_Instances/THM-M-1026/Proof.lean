import ObligationTree

/-!
# THM-M-1026 proof-phase bodies

This module proves the converse half of the frozen generalized central limit
theorem.  A stable law is used as its own attracting law.  Stability supplies
normalizers from index two onward; arbitrary positive defaults cover the two
initial indices, which do not affect convergence at `atTop`.

The necessity half requires the convergence-of-types argument recorded in the
frozen obligation tree and remains open.
-/

noncomputable section

open Filter MeasureTheory

namespace Stage1Instances.THM_M_1026.Proof

/-- Stability supplies total positive normalizing sequences which normalize
every convolution power from index two onward back to the original law. -/
theorem stable_normalizers
    {nu : Measure Real} (hstable : IsStableLaw nu) :
    exists a b : Nat -> Real, (forall n, 0 < a n) /\
      forall n, 2 <= n -> normalizedLaw (convPow nu n) (a n) (b n) = nu := by
  choose a b hab using hstable.2.2
  let a' : Nat -> Real := fun n => if hn : 2 <= n then a n hn else 1
  let b' : Nat -> Real := fun n => if hn : 2 <= n then b n hn else 0
  refine ⟨a', b', ?_, ?_⟩
  · intro n
    by_cases hn : 2 <= n
    · simpa [a', hn] using (hab n hn).1
    · simp [a', hn]
  · intro n hn
    simpa [a', b', hn] using (hab n hn).2

/-- A sequence of measures which is eventually equal to its proposed limit
converges weakly under the frozen bounded-continuous-test definition. -/
theorem weaklyConverges_of_eventually_eq
    {mu : Nat -> Measure Real} {nu : Measure Real}
    (hmu : forall n, 2 <= n -> mu n = nu) : WeaklyConverges mu nu := by
  intro f
  refine Filter.Tendsto.congr' ?_
    (tendsto_const_nhds : Tendsto (fun _ : Nat => ∫ x, f x ∂nu) atTop
      (nhds (∫ x, f x ∂nu)))
  filter_upwards [eventually_ge_atTop 2] with n hn
  rw [hmu n hn]

/-- Every stable law belongs to a nonempty frozen domain of attraction: take
the law itself and the total normalizers furnished by `stable_normalizers`. -/
theorem converseTerminal :
    Stage1Instances.THM_M_1026.ObligationTree.ConverseTerminal := by
  intro nu hprob _ hstable
  obtain ⟨a, b, ha, hab⟩ := stable_normalizers hstable
  refine ⟨nu, hprob, a, b, ha, ?_⟩
  exact weaklyConverges_of_eventually_eq hab

#check stable_normalizers
#check weaklyConverges_of_eventually_eq
#check converseTerminal
#print axioms stable_normalizers
#print axioms weaklyConverges_of_eventually_eq
#print axioms converseTerminal

end Stage1Instances.THM_M_1026.Proof
