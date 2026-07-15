import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0841 proof-phase bodies

This module proves the exact sparse-to-dense complement transport frozen by the obligation tree.
It also checks the dense-family and root compositions with every mathematical premise visible.
The deep `DenseBase` and `DenseStep` arguments remain open; no root closure is claimed here.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0841_Proof

open scoped SimpleGraph
open Stage1Instances.THM_M_0841
open Stage1Instances.THM_M_0841_Obligations

/-- Real normalization of the exact finite complete-graph edge count. -/
theorem cast_choose_two (n : Nat) :
    (n.choose 2 : Real) = ((n : Real) ^ 2 - (n : Real)) / 2 := by
  have hdvd : 2 ∣ n * (n - 1) :=
    even_iff_two_dvd.mp (Nat.even_mul_pred_self n)
  have hdiv : n * (n - 1) / 2 * 2 = n * (n - 1) :=
    Nat.div_mul_cancel hdvd
  rw [Nat.choose_two_right]
  apply (eq_div_iff (by norm_num : (2 : Real) ≠ 0)).mpr
  have hcast := congrArg (fun x : Nat => (x : Real)) hdiv
  push_cast at hcast
  rw [hcast]
  by_cases h : n = 0
  · simp [h]
  · have hn : 1 ≤ n := Nat.one_le_iff_ne_zero.mpr h
    rw [Nat.cast_sub hn]
    ring

/-- A graph and its complement partition all unordered pairs of distinct vertices. -/
theorem card_edgeFinset_compl (n : Nat) (G : SimpleGraph (Fin n))
    [DecidableRel G.Adj] :
    (Gᶜ).edgeFinset.card = n.choose 2 - G.edgeFinset.card := by
  have hgraph : Gᶜ = ⊤ \ G := (top_sdiff (x := G)).symm
  have hedges : (Gᶜ).edgeFinset = (⊤ \ G).edgeFinset := by
    ext e
    rw [SimpleGraph.mem_edgeFinset, SimpleGraph.mem_edgeFinset, hgraph]
  calc
    (Gᶜ).edgeFinset.card = (⊤ \ G).edgeFinset.card := congrArg Finset.card hedges
    _ = (⊤ : SimpleGraph (Fin n)).edgeFinset.card - G.edgeFinset.card := by
      rw [SimpleGraph.edgeFinset_sdiff,
        Finset.card_sdiff_of_subset (SimpleGraph.edgeFinset_mono le_top)]
    _ = n.choose 2 - G.edgeFinset.card := by
      simpa using congrArg (fun x => x - G.edgeFinset.card)
        (SimpleGraph.card_edgeFinset_top_eq_card_choose_two (V := Fin n))

/-- Exact implementation of the frozen sparse/dense transport. -/
theorem sparseFromDense : SparseFromDense := by
  intro dense epsilon r hepsilon hepsilon_one hr
  obtain ⟨N, _hNpos, hN⟩ :=
    dense r hr (epsilon / 2) (by positivity) (by linarith) hr
  obtain ⟨M, hM⟩ := exists_nat_gt (1 / epsilon)
  refine ⟨max N (max 1 M), by omega, ?_⟩
  intro n hn G _inst hG
  apply hN n (by omega) Gᶜ
  have hMlt : M < n := by omega
  have _hnpos : 0 < n := by omega
  have _hnRpos : (0 : Real) < n := by positivity
  have hepsilon_n : 1 < epsilon * n := by
    have hcast : (M : Real) < n := by exact_mod_cast hMlt
    have h := hM.trans hcast
    rwa [div_lt_iff₀ hepsilon, mul_comm] at h
  have hle : G.edgeFinset.card ≤ n.choose 2 := by
    simpa using G.card_edgeFinset_le_card_choose_two
  rw [card_edgeFinset_compl, Nat.cast_sub hle, cast_choose_two]
  nlinarith

/-- Frozen strong-induction composition with the two deep premises explicit. -/
theorem denseFamily_of_base_step (base : DenseBase) (step : DenseStep) : DenseFamily :=
  denseFamily_compose base step

/-- Exact conditional root composition.  Only the still-open base and induction step are premises;
the complement transport is discharged by `sparseFromDense`. -/
theorem erdosStone_of_dense_base_step (base : DenseBase) (step : DenseStep) : ExactRoot :=
  sparseFromDense (denseFamily_of_base_step base step)

#check card_edgeFinset_compl
#check cast_choose_two
#check sparseFromDense
#check denseFamily_of_base_step
#check erdosStone_of_dense_base_step

assert_no_sorry card_edgeFinset_compl
assert_no_sorry cast_choose_two
assert_no_sorry sparseFromDense
assert_no_sorry denseFamily_of_base_step
assert_no_sorry erdosStone_of_dense_base_step

#print sorries cast_choose_two card_edgeFinset_compl sparseFromDense
  denseFamily_of_base_step erdosStone_of_dense_base_step
#print axioms card_edgeFinset_compl
#print axioms cast_choose_two
#print axioms sparseFromDense
#print axioms denseFamily_of_base_step
#print axioms erdosStone_of_dense_base_step

end Stage1Instances.THM_M_0841_Proof
