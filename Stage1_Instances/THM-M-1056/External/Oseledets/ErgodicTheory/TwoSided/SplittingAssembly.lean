/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.TwoSided.Invertible
import ErgodicTheory.TwoSided.SpectralRank
import ErgodicTheory.TwoSided.StrongExport
import ErgodicTheory.TwoSided.KingmanMeans
import ErgodicTheory.TwoSided.RestrictedCocycle
import ErgodicTheory.TwoSided.RestrictedExponent
import ErgodicTheory.TwoSided.Transversality
import ErgodicTheory.TwoSided.Reflection
import ErgodicTheory.TwoSided.MeasurableInf
import Mathlib.Algebra.DirectSum.Module
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas

/-!
# The two-sided Oseledets splitting

This is the two-sided Oseledets multiplicative ergodic theorem.  It assembles the
forward and backward one-sided Oseledets filtrations into a single measurable,
`A`-equivariant **splitting** `ℝᵈ = E₁(x) ⊕ ⋯ ⊕ E_k(x)` with two-sided growth: for a
nonzero `v ∈ Eᵢ(x)` the forward cocycle grows at rate `λᵢ` and the backward cocycle at
rate `−λᵢ`.

The pieces consumed are:

* `oseledets_filtration_dims`, instantiated for the forward system `(T, A)` and (via
  `backwardData_of`) for the backward system `(T.symm, backwardGen A T)`, giving the
  forward data `lam0`, `V` and the backward data `mu0`, `W`, each with its dimension
  formula;
* `ae_crux` and `ae_counting` (the transversality crux and the resulting counting
  bound);
* `sum_mu0_eq_neg_sum_lam0`, `reflect_of_counting_and_sum` and the reflection
  corollaries (`numExp_eq_of_counting`, `expEnum_eq_neg_rev_of_counting`,
  `backward_count_eq_of_counting`), which align the backward index to the forward one
  (`l = k`, `μ_{sᵢ} = −λᵢ`);
* `MeasurableSubspace.inf` for the measurability of the intersection bundle.

The internal-direct-sum structure is obtained from a pure telescoping-flag lattice lemma
(`flag_iSupIndep_and_iSup`): the split subspaces `Eᵢ = V i.castSucc ⊓ W (sidx i).castSucc`
satisfy `V i.castSucc = Eᵢ ⊔ V i.succ` and `Eᵢ ⊓ V i.succ = ⊥`, which telescope a
`⊤`-to-`⊥` flag into an internal direct sum.

## Main results

* `ErgodicTheory.oseledets_splitting_dim_zero` — the trivial `d = 0` case.
* `ErgodicTheory.oseledets_splitting` — the headline two-sided splitting theorem.

## References

* V. I. Oseledets, *A multiplicative ergodic theorem. Lyapunov characteristic numbers for
  dynamical systems*, Trans. Moscow Math. Soc. **19** (1968), 197–231.
* D. Ruelle, *Ergodic theory of differentiable dynamical systems*,
  Publ. Math. IHÉS **50** (1979), 27–58.
* L. Arnold, *Random Dynamical Systems*, Springer Monographs in Mathematics, 1998.
-/

open MeasureTheory Filter Topology Matrix DirectSum
open scoped Matrix.Norms.L2Operator RealInnerProductSpace

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ}

/-! ### A pure telescoping-flag lattice lemma -/

section Flag

variable {α : Type*} [CompleteLattice α] [IsModularLattice α]

omit [IsModularLattice α] in
/-- **`iSup` over `Fin (k+1)` splits off the head.** -/
private theorem iSup_fin_succ {k : ℕ} (E : Fin (k + 1) → α) :
    ⨆ i : Fin (k + 1), E i = E 0 ⊔ ⨆ i : Fin k, E i.succ := by
  apply le_antisymm
  · refine iSup_le fun i => ?_
    refine Fin.cases ?_ ?_ i
    · exact le_sup_left
    · intro i'
      exact le_sup_of_le_right (le_iSup (fun i : Fin k => E i.succ) i')
  · refine sup_le (le_iSup E 0) (iSup_le fun i' => le_iSup E i'.succ)

/-- **Cons step for independence.** If the tail family `i ↦ E i.succ` is independent and the
head `E 0` is disjoint from the tail supremum, then `E` is independent. -/
private theorem iSupIndep_cons {k : ℕ} (E : Fin (k + 1) → α)
    (htail : iSupIndep fun i : Fin k => E i.succ)
    (hdis : Disjoint (E 0) (⨆ i : Fin k, E i.succ)) :
    iSupIndep E := by
  rw [iSupIndep_def]
  intro i
  refine Fin.cases ?_ ?_ i
  · have hbound : (⨆ (j : Fin (k + 1)) (_ : j ≠ 0), E j) ≤ ⨆ i : Fin k, E i.succ := by
      refine iSup_le fun j => iSup_le fun hj => ?_
      obtain ⟨j', rfl⟩ := Fin.exists_succ_eq.mpr hj
      exact le_iSup (fun i : Fin k => E i.succ) j'
    exact hdis.mono_right hbound
  · intro i'
    rw [iSupIndep_def] at htail
    have htaili := htail i'
    -- Abbreviations: the tail bound `B` and the restricted tail sup `C`.
    set B : α := ⨆ i : Fin k, E i.succ with hB
    set C : α := ⨆ (j' : Fin k) (_ : j' ≠ i'), E j'.succ with hC
    -- The whole sup `⨆ j≠i'.succ, E j` is bounded by `E 0 ⊔ C`.
    have hbound : (⨆ (j : Fin (k + 1)) (_ : j ≠ i'.succ), E j) ≤ E 0 ⊔ C := by
      refine iSup_le fun j => ?_
      refine Fin.cases ?_ ?_ j
      · exact iSup_le fun _ => le_sup_left
      · intro j''
        refine iSup_le fun hj => ?_
        have hj'' : j'' ≠ i' := fun h => hj (congrArg Fin.succ h)
        exact le_sup_of_le_right (le_iSup_of_le j'' (le_iSup_of_le hj'' le_rfl))
    refine Disjoint.mono_right hbound ?_
    -- `C ≤ B` and `E i'.succ ≤ B`, so use modularity to peel off `E 0`.
    have hCB : C ≤ B := iSup_le fun j' => iSup_le fun _ => le_iSup (fun i : Fin k => E i.succ) j'
    have hiB : E i'.succ ≤ B := le_iSup (fun i : Fin k => E i.succ) i'
    -- `(E 0 ⊔ C) ⊓ B = C` by modularity (`C ≤ B`, `E 0 ⊓ B = ⊥`).
    have hmod : (E 0 ⊔ C) ⊓ B = C := by
      rw [sup_comm, sup_inf_assoc_of_le _ hCB, disjoint_iff.mp hdis, sup_bot_eq]
    rw [disjoint_iff]
    calc E i'.succ ⊓ (E 0 ⊔ C)
        = E i'.succ ⊓ B ⊓ (E 0 ⊔ C) := by rw [inf_eq_left.mpr hiB]
      _ = E i'.succ ⊓ ((E 0 ⊔ C) ⊓ B) := by rw [inf_assoc, inf_comm B]
      _ = E i'.succ ⊓ C := by rw [hmod]
      _ = ⊥ := disjoint_iff.mp htaili

/-- **Telescoping-flag lattice lemma.** A descending flag `V` from `V 0` to `⊥` with
complements `E i` satisfying `V i.castSucc = E i ⊔ V i.succ` and `E i ⊓ V i.succ = ⊥`
telescopes into `iSupIndep E ∧ ⨆ i, E i = V 0`. -/
private theorem flag_iSupIndep_and_iSup {k : ℕ} (V : Fin (k + 1) → α) (E : Fin k → α)
    (hbot : V (Fin.last k) = ⊥)
    (hsup : ∀ i : Fin k, V i.castSucc = E i ⊔ V i.succ)
    (hdis : ∀ i : Fin k, E i ⊓ V i.succ = ⊥) :
    iSupIndep E ∧ ⨆ i, E i = V 0 := by
  induction k with
  | zero =>
    refine ⟨iSupIndep_subsingleton _, ?_⟩
    rw [iSup_of_empty]
    rw [show (0 : Fin 1) = Fin.last 0 from rfl, hbot]
  | succ k ih =>
    set vprime : Fin (k + 1) → α := fun j => V j.succ with hV'
    set E' : Fin k → α := fun j => E j.succ with hE'
    have hbot' : vprime (Fin.last k) = ⊥ := by
      rw [hV']; simp only
      rw [show (Fin.last k).succ = Fin.last (k + 1) from rfl, hbot]
    have hsup' : ∀ i : Fin k, vprime i.castSucc = E' i ⊔ vprime i.succ := by
      intro i
      rw [hV', hE']; simp only
      rw [show (i.castSucc).succ = (i.succ).castSucc from rfl]
      exact hsup i.succ
    have hdis' : ∀ i : Fin k, E' i ⊓ vprime i.succ = ⊥ := fun i => by
      rw [hE', hV']; simp only; exact hdis i.succ
    obtain ⟨hindep', hsupeq'⟩ := ih vprime E' hbot' hsup' hdis'
    refine ⟨iSupIndep_cons E hindep' ?_, ?_⟩
    · rw [show (⨆ i : Fin k, E i.succ) = ⨆ i : Fin k, E' i from rfl, hsupeq',
        show vprime 0 = V (Fin.succ 0) from rfl, disjoint_iff]
      have := hdis 0
      rwa [show (0 : Fin (k + 1)).succ = Fin.succ 0 from rfl] at this
    · rw [iSup_fin_succ,
        show (⨆ i : Fin k, E i.succ) = ⨆ i : Fin k, E' i from rfl, hsupeq',
        show vprime 0 = V (Fin.succ 0) from rfl]
      have := hsup 0
      rw [show (0 : Fin (k + 1)).castSucc = 0 from rfl] at this
      rw [← this]

end Flag

/-! ### The aligned backward index and the transported backward equivariance -/

/-- The backward filtration index aligned to the forward level `i`, so that its exponent is
`−λᵢ`: `sidx i = cast (Fin.rev i)` under `numExp mu0 d = numExp lam0 d`. -/
noncomputable def sidx {lam0 mu0 : ℕ → ℝ}
    (hrefl : ∀ j : ℕ, j < d → mu0 j = -lam0 (d - 1 - j)) (i : Fin (numExp lam0 d)) :
    Fin (numExp mu0 d) :=
  Fin.cast (numExp_eq_of_counting hrefl).symm (Fin.rev i)

/-- The aligned backward exponent is the negated forward one: `μ_{sidx i} = −λᵢ`. -/
theorem sidx_exp {lam0 mu0 : ℕ → ℝ}
    (hrefl : ∀ j : ℕ, j < d → mu0 j = -lam0 (d - 1 - j)) (i : Fin (numExp lam0 d)) :
    expEnum mu0 d (sidx hrefl i) = -expEnum lam0 d i := by
  rw [expEnum_eq_neg_rev_of_counting hrefl]
  congr 2
  ext
  have hnum : numExp mu0 d = numExp lam0 d := numExp_eq_of_counting hrefl
  have hi : (i : ℕ) < numExp lam0 d := i.isLt
  simp only [sidx, Fin.val_cast, Fin.val_rev]
  omega

/-- **Transport of equivariance through the inverse generator.** If `M` is invertible and
`map (M⁻¹) Q = P`, then `map (M) P = Q`. Used to convert the backward filtration's
`backwardGen`-equivariance into forward `A`-equivariance. -/
theorem map_of_map_inv {M : Matrix (Fin d) (Fin d) ℝ} (hM : M.det ≠ 0)
    {P Q : Submodule ℝ (EuclideanSpace ℝ (Fin d))}
    (h : Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) M⁻¹).toLinearMap Q = P) :
    Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) M).toLinearMap P = Q := by
  rw [← h, ← Submodule.map_comp]
  have hid : (Matrix.toEuclideanCLM (𝕜 := ℝ) M).toLinearMap.comp
      (Matrix.toEuclideanCLM (𝕜 := ℝ) M⁻¹).toLinearMap = LinearMap.id := by
    have hmul : Matrix.toEuclideanCLM (𝕜 := ℝ) M * Matrix.toEuclideanCLM (𝕜 := ℝ) M⁻¹ = 1 := by
      rw [← map_mul, Matrix.mul_nonsing_inv M (Ne.isUnit hM), map_one]
    have hcoe := congrArg
      (fun c : EuclideanSpace ℝ (Fin d) →L[ℝ] EuclideanSpace ℝ (Fin d) => c.toLinearMap) hmul
    simpa [ContinuousLinearMap.coe_mul] using hcoe
  rw [hid, Submodule.map_id]

/-! ### Per-point dimension and lattice facts -/

section PerPoint

variable {lam0 mu0 : ℕ → ℝ}
    (hrefl : ∀ j : ℕ, j < d → mu0 j = -lam0 (d - 1 - j))
    {Vx : Fin (numExp lam0 d + 1) → Submodule ℝ (EuclideanSpace ℝ (Fin d))}
    {Wx : Fin (numExp mu0 d + 1) → Submodule ℝ (EuclideanSpace ℝ (Fin d))}

/-- The forward successor-level finrank equals the strict forward count below `λᵢ`. -/
theorem finrank_Vsucc
    (hVdim : ∀ i : Fin (numExp lam0 d),
      Module.finrank ℝ (Vx i.castSucc)
        = ((Finset.range d).filter (fun j => lam0 j ≤ expEnum lam0 d i)).card)
    (hVlast : Vx (Fin.last (numExp lam0 d)) = ⊥) (i : Fin (numExp lam0 d)) :
    Module.finrank ℝ (Vx i.succ)
      = ((Finset.range d).filter (fun j => lam0 j < expEnum lam0 d i)).card := by
  rcases lt_or_ge ((i : ℕ) + 1) (numExp lam0 d) with hi | hi
  · have hcs : (⟨(i : ℕ) + 1, hi⟩ : Fin (numExp lam0 d)).castSucc = i.succ := by ext; simp
    rw [← hcs, hVdim ⟨(i : ℕ) + 1, hi⟩, ← forward_strict_count_eq_succ i hi]
  · have hlast : i.succ = Fin.last (numExp lam0 d) := by ext; simp; omega
    rw [hlast, hVlast, finrank_bot]
    symm
    rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
    intro j hj
    rw [Finset.mem_range] at hj
    rw [not_lt]
    obtain ⟨l, hl⟩ := exists_expEnum_eq lam0 hj
    rw [← hl]
    have hile : l ≤ i := by rw [Fin.le_def]; have hl2 := l.isLt; omega
    exact (expEnum_strictAnti lam0 d).antitone hile

/-- The aligned backward-level finrank is `d` minus the strict forward count below `λᵢ`. -/
theorem finrank_Wsidx
    (hWdim : ∀ s : Fin (numExp mu0 d),
      Module.finrank ℝ (Wx s.castSucc)
        = ((Finset.range d).filter (fun j => mu0 j ≤ expEnum mu0 d s)).card)
    (i : Fin (numExp lam0 d)) :
    Module.finrank ℝ (Wx (sidx hrefl i).castSucc)
      = d - ((Finset.range d).filter (fun j => lam0 j < expEnum lam0 d i)).card := by
  rw [hWdim (sidx hrefl i), sidx_exp hrefl i, backward_count_eq_of_counting hrefl]

/-- **Crux disjointness at the forward successor level.** -/
theorem crux_succ
    (hVlast : Vx (Fin.last (numExp lam0 d)) = ⊥)
    (hcrux : ∀ (i' : Fin (numExp lam0 d)) (s : Fin (numExp mu0 d)),
      expEnum lam0 d i' + expEnum mu0 d s < 0 → Vx i'.castSucc ⊓ Wx s.castSucc = ⊥)
    (i : Fin (numExp lam0 d)) :
    Vx i.succ ⊓ Wx (sidx hrefl i).castSucc = ⊥ := by
  rcases lt_or_ge ((i : ℕ) + 1) (numExp lam0 d) with hi | hi
  · have hcs : (⟨(i : ℕ) + 1, hi⟩ : Fin (numExp lam0 d)).castSucc = i.succ := by ext; simp
    rw [← hcs]
    apply hcrux ⟨(i : ℕ) + 1, hi⟩ (sidx hrefl i)
    rw [sidx_exp hrefl i]
    have : expEnum lam0 d ⟨(i : ℕ) + 1, hi⟩ < expEnum lam0 d i :=
      expEnum_strictAnti lam0 d (by rw [Fin.lt_def]; simp)
    linarith
  · have hlast : i.succ = Fin.last (numExp lam0 d) := by ext; simp; omega
    rw [hlast, hVlast, bot_inf_eq]

/-- **Crux disjointness at the backward successor level.** -/
theorem crux_succ_backward
    (hWlast : Wx (Fin.last (numExp mu0 d)) = ⊥)
    (hcrux : ∀ (i' : Fin (numExp lam0 d)) (s : Fin (numExp mu0 d)),
      expEnum lam0 d i' + expEnum mu0 d s < 0 → Vx i'.castSucc ⊓ Wx s.castSucc = ⊥)
    (i : Fin (numExp lam0 d)) :
    Vx i.castSucc ⊓ Wx (sidx hrefl i).succ = ⊥ := by
  rcases lt_or_ge ((sidx hrefl i : ℕ) + 1) (numExp mu0 d) with hs | hs
  · have hcs : (⟨(sidx hrefl i : ℕ) + 1, hs⟩ : Fin (numExp mu0 d)).castSucc
        = (sidx hrefl i).succ := by ext; simp
    rw [← hcs]
    apply hcrux i ⟨(sidx hrefl i : ℕ) + 1, hs⟩
    have hlt : expEnum mu0 d ⟨(sidx hrefl i : ℕ) + 1, hs⟩ < expEnum mu0 d (sidx hrefl i) :=
      expEnum_strictAnti mu0 d (by rw [Fin.lt_def]; simp)
    rw [sidx_exp hrefl i] at hlt
    linarith
  · have hlast : (sidx hrefl i).succ = Fin.last (numExp mu0 d) := by ext; simp; omega
    rw [hlast, hWlast, inf_bot_eq]

/-- The intersection-splitting subspace at forward level `i` (per-point). -/
noncomputable def esplitAt (i : Fin (numExp lam0 d)) :
    Submodule ℝ (EuclideanSpace ℝ (Fin d)) :=
  Vx i.castSucc ⊓ Wx (sidx hrefl i).castSucc

/-- **Totality at level `i`:** `Vx i.castSucc ⊔ Wx (sidx i).castSucc = ⊤`. -/
theorem sup_eq_top
    (hVdim : ∀ i : Fin (numExp lam0 d),
      Module.finrank ℝ (Vx i.castSucc)
        = ((Finset.range d).filter (fun j => lam0 j ≤ expEnum lam0 d i)).card)
    (hWdim : ∀ s : Fin (numExp mu0 d),
      Module.finrank ℝ (Wx s.castSucc)
        = ((Finset.range d).filter (fun j => mu0 j ≤ expEnum mu0 d s)).card)
    (hVanti : Antitone Vx) (hVlast : Vx (Fin.last (numExp lam0 d)) = ⊥)
    (hcrux : ∀ (i' : Fin (numExp lam0 d)) (s : Fin (numExp mu0 d)),
      expEnum lam0 d i' + expEnum mu0 d s < 0 → Vx i'.castSucc ⊓ Wx s.castSucc = ⊥)
    (i : Fin (numExp lam0 d)) :
    Vx i.castSucc ⊔ Wx (sidx hrefl i).castSucc = ⊤ := by
  have hsuccsup : Vx i.succ ⊔ Wx (sidx hrefl i).castSucc = ⊤ := by
    apply Submodule.eq_top_of_finrank_eq
    have hgr := Submodule.finrank_sup_add_finrank_inf_eq (Vx i.succ) (Wx (sidx hrefl i).castSucc)
    rw [crux_succ hrefl hVlast hcrux i, finrank_bot, add_zero,
      finrank_Vsucc hVdim hVlast i, finrank_Wsidx hrefl hWdim i] at hgr
    have hcnt : ((Finset.range d).filter (fun j => lam0 j < expEnum lam0 d i)).card ≤ d := by
      calc _ ≤ (Finset.range d).card := Finset.card_filter_le _ _
        _ = d := Finset.card_range d
    rw [hgr, finrank_euclideanSpace_fin]; omega
  refine top_unique ?_
  rw [← hsuccsup]
  exact sup_le_sup_right (hVanti (Fin.castSucc_le_succ i)) _

/-- `finrank (esplitAt i) = #{j | lam0 j ≤ λᵢ} − #{j | lam0 j < λᵢ}`. -/
theorem finrank_esplitAt
    (hVdim : ∀ i : Fin (numExp lam0 d),
      Module.finrank ℝ (Vx i.castSucc)
        = ((Finset.range d).filter (fun j => lam0 j ≤ expEnum lam0 d i)).card)
    (hWdim : ∀ s : Fin (numExp mu0 d),
      Module.finrank ℝ (Wx s.castSucc)
        = ((Finset.range d).filter (fun j => mu0 j ≤ expEnum mu0 d s)).card)
    (hVanti : Antitone Vx) (hVlast : Vx (Fin.last (numExp lam0 d)) = ⊥)
    (hcrux : ∀ (i' : Fin (numExp lam0 d)) (s : Fin (numExp mu0 d)),
      expEnum lam0 d i' + expEnum mu0 d s < 0 → Vx i'.castSucc ⊓ Wx s.castSucc = ⊥)
    (i : Fin (numExp lam0 d)) :
    Module.finrank ℝ (esplitAt (Vx := Vx) (Wx := Wx) hrefl i)
      = ((Finset.range d).filter (fun j => lam0 j ≤ expEnum lam0 d i)).card
        - ((Finset.range d).filter (fun j => lam0 j < expEnum lam0 d i)).card := by
  have hgr := Submodule.finrank_sup_add_finrank_inf_eq (Vx i.castSucc) (Wx (sidx hrefl i).castSucc)
  rw [sup_eq_top hrefl hVdim hWdim hVanti hVlast hcrux i, finrank_top, finrank_euclideanSpace_fin,
    hVdim i, finrank_Wsidx hrefl hWdim i] at hgr
  have hcnt : ((Finset.range d).filter (fun j => lam0 j < expEnum lam0 d i)).card ≤ d := by
    calc _ ≤ (Finset.range d).card := Finset.card_filter_le _ _
      _ = d := Finset.card_range d
  have hE : esplitAt (Vx := Vx) (Wx := Wx) hrefl i
      = Vx i.castSucc ⊓ Wx (sidx hrefl i).castSucc := rfl
  rw [hE]
  omega

/-- `esplitAt i ⊓ Vx i.succ = ⊥`. -/
theorem esplitAt_inf_Vsucc
    (hVlast : Vx (Fin.last (numExp lam0 d)) = ⊥)
    (hcrux : ∀ (i' : Fin (numExp lam0 d)) (s : Fin (numExp mu0 d)),
      expEnum lam0 d i' + expEnum mu0 d s < 0 → Vx i'.castSucc ⊓ Wx s.castSucc = ⊥)
    (i : Fin (numExp lam0 d)) :
    esplitAt (Vx := Vx) (Wx := Wx) hrefl i ⊓ Vx i.succ = ⊥ := by
  rw [eq_bot_iff, ← crux_succ hrefl hVlast hcrux i]
  simp only [esplitAt]
  exact le_inf (le_trans inf_le_right le_rfl) (le_trans inf_le_left inf_le_right)

/-- The telescoping identity `Vx i.castSucc = esplitAt i ⊔ Vx i.succ`. -/
theorem Vcast_eq_esplitAt_sup_Vsucc
    (hVdim : ∀ i : Fin (numExp lam0 d),
      Module.finrank ℝ (Vx i.castSucc)
        = ((Finset.range d).filter (fun j => lam0 j ≤ expEnum lam0 d i)).card)
    (hWdim : ∀ s : Fin (numExp mu0 d),
      Module.finrank ℝ (Wx s.castSucc)
        = ((Finset.range d).filter (fun j => mu0 j ≤ expEnum mu0 d s)).card)
    (hVanti : Antitone Vx) (hVlast : Vx (Fin.last (numExp lam0 d)) = ⊥)
    (hcrux : ∀ (i' : Fin (numExp lam0 d)) (s : Fin (numExp mu0 d)),
      expEnum lam0 d i' + expEnum mu0 d s < 0 → Vx i'.castSucc ⊓ Wx s.castSucc = ⊥)
    (i : Fin (numExp lam0 d)) :
    Vx i.castSucc = esplitAt (Vx := Vx) (Wx := Wx) hrefl i ⊔ Vx i.succ := by
  have hle : esplitAt (Vx := Vx) (Wx := Wx) hrefl i ⊔ Vx i.succ ≤ Vx i.castSucc := by
    refine sup_le ?_ (hVanti (Fin.castSucc_le_succ i))
    simp only [esplitAt]; exact inf_le_left
  symm
  apply Submodule.eq_of_le_of_finrank_eq hle
  have hgr := Submodule.finrank_sup_add_finrank_inf_eq
    (esplitAt (Vx := Vx) (Wx := Wx) hrefl i) (Vx i.succ)
  rw [esplitAt_inf_Vsucc hrefl hVlast hcrux i, finrank_bot, add_zero,
    finrank_esplitAt hrefl hVdim hWdim hVanti hVlast hcrux i,
    finrank_Vsucc hVdim hVlast i] at hgr
  have hcntlt : ((Finset.range d).filter (fun j => lam0 j < expEnum lam0 d i)).card
      ≤ ((Finset.range d).filter (fun j => lam0 j ≤ expEnum lam0 d i)).card :=
    Finset.card_le_card (Finset.monotone_filter_right _ fun j _ hj => le_of_lt hj)
  rw [hgr, hVdim i]; omega

/-- The split subspace is nonzero: `1 ≤ finrank (esplitAt i)`. -/
theorem one_le_finrank_esplitAt
    (hVdim : ∀ i : Fin (numExp lam0 d),
      Module.finrank ℝ (Vx i.castSucc)
        = ((Finset.range d).filter (fun j => lam0 j ≤ expEnum lam0 d i)).card)
    (hWdim : ∀ s : Fin (numExp mu0 d),
      Module.finrank ℝ (Wx s.castSucc)
        = ((Finset.range d).filter (fun j => mu0 j ≤ expEnum mu0 d s)).card)
    (hVanti : Antitone Vx) (hVlast : Vx (Fin.last (numExp lam0 d)) = ⊥)
    (hcrux : ∀ (i' : Fin (numExp lam0 d)) (s : Fin (numExp mu0 d)),
      expEnum lam0 d i' + expEnum mu0 d s < 0 → Vx i'.castSucc ⊓ Wx s.castSucc = ⊥)
    (i : Fin (numExp lam0 d)) :
    1 ≤ Module.finrank ℝ (esplitAt (Vx := Vx) (Wx := Wx) hrefl i) := by
  rw [finrank_esplitAt hrefl hVdim hWdim hVanti hVlast hcrux i]
  obtain ⟨j, hjd, hjeq⟩ := expEnum_eq_lam lam0 d i
  have hmemle : j ∈ (Finset.range d).filter (fun j => lam0 j ≤ expEnum lam0 d i) := by
    rw [Finset.mem_filter, Finset.mem_range]; exact ⟨hjd, le_of_eq hjeq.symm⟩
  have hnotlt : j ∉ (Finset.range d).filter (fun j => lam0 j < expEnum lam0 d i) := by
    rw [Finset.mem_filter]; rintro ⟨_, h⟩; rw [hjeq] at h; exact lt_irrefl _ h
  have hsub : (Finset.range d).filter (fun j => lam0 j < expEnum lam0 d i)
      ⊆ (Finset.range d).filter (fun j => lam0 j ≤ expEnum lam0 d i) :=
    Finset.monotone_filter_right _ fun j _ hj => le_of_lt hj
  have hlt := Finset.card_lt_card (Finset.ssubset_iff_of_subset hsub |>.mpr ⟨j, hmemle, hnotlt⟩)
  omega

end PerPoint

/-! ### The splitting in positive dimension -/

section Pos

variable [NeZero d] {μ : Measure X} [IsProbabilityMeasure μ] {T : X ≃ᵐ X}

/-- **The two-sided Oseledets splitting (positive dimension).** The headline statement,
established for `d > 0`; the public `oseledets_splitting` adds the trivial
`d = 0` branch. -/
theorem oseledets_splitting_pos
    (hT : Ergodic T μ)
    (A : X → Matrix (Fin d) (Fin d) ℝ)
    (hA : ∀ x, (A x).det ≠ 0)
    (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ)
    (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∃ (k : ℕ) (lam : Fin k → ℝ)
      (E : Fin k → X → Submodule ℝ (EuclideanSpace ℝ (Fin d))),
      StrictAnti lam ∧
      (∀ i, MeasurableSubspace fun x => E i x) ∧
      ∀ᵐ x ∂μ,
        DirectSum.IsInternal (fun i => E i x) ∧
        (∀ i, E i x ≠ ⊥) ∧
        (∀ i, Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap (E i x)
          = E i (T x)) ∧
        (∀ i, ∀ v ∈ E i x, v ≠ 0 →
          Tendsto
            (fun n : ℕ => (n : ℝ)⁻¹ *
              Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖)
            atTop (𝓝 (lam i)) ∧
          Tendsto
            (fun n : ℕ => (n : ℝ)⁻¹ *
              Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ)
                (cocycle A T n ((⇑T.symm)^[n] x))⁻¹ v‖)
            atTop (𝓝 (-lam i))) := by
  classical
  have hmp : MeasurePreserving T μ μ := hT.toMeasurePreserving
  -- Forward strong export.
  obtain ⟨lam0, hlam0mono, hlam0sv, V, hVmeas, hVae⟩ :=
    oseledets_filtration_dims hT A hA hAmeas hint hint'
  -- Backward strong export.
  have hbd : BackwardData μ A T := backwardData_of hA hAmeas hmp hint hint'
  obtain ⟨mu0, hmu0mono, hmu0sv, W, hWmeas, hWae⟩ :=
    oseledets_filtration_dims (T := ⇑T.symm) hT.symm (backwardGen A T)
      hbd.det_ne_zero hbd.measurable hbd.integrableLogNorm hbd.integrableLogNorm_inv
  -- Dimension a.e. facts.
  have hVdim : ∀ᵐ x ∂μ, ∀ i : Fin (numExp lam0 d),
      Module.finrank ℝ (V i.castSucc x)
        = ((Finset.range d).filter (fun j => lam0 j ≤ expEnum lam0 d i)).card := by
    filter_upwards [hVae] with x hx; exact hx.2.2.2.2.2
  have hWdim : ∀ᵐ x ∂μ, ∀ s : Fin (numExp mu0 d),
      Module.finrank ℝ (W s.castSucc x)
        = ((Finset.range d).filter (fun j => mu0 j ≤ expEnum mu0 d s)).card := by
    filter_upwards [hWae] with x hx; exact hx.2.2.2.2.2
  -- Backward structural facts for the crux (4-tuple form).
  have hWstruct : ∀ᵐ x ∂μ,
      W 0 x = ⊤ ∧ W (Fin.last (numExp mu0 d)) x = ⊥ ∧
      (∀ s : Fin (numExp mu0 d), W s.succ x < W s.castSucc x) ∧
      (∀ s : Fin (numExp mu0 d),
        ∀ v ∈ (W s.castSucc x : Set (EuclideanSpace ℝ (Fin d))), v ∉ W s.succ x →
          Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log
            ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle (backwardGen A T) (⇑T.symm) n x) v‖)
            atTop (𝓝 (expEnum mu0 d s))) := by
    filter_upwards [hWae] with x hx
    exact ⟨hx.1, hx.2.1, hx.2.2.1, hx.2.2.2.2.1⟩
  -- Forward structural facts for the crux (5-tuple form, dropping the dim conjunct).
  have hVstruct : ∀ᵐ x ∂μ,
      V 0 x = ⊤ ∧ V (Fin.last (numExp lam0 d)) x = ⊥ ∧
      (∀ i : Fin (numExp lam0 d), V i.succ x < V i.castSucc x) ∧
      (∀ i : Fin (numExp lam0 d + 1),
        Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap (V i x)
          = V i ((⇑T) x)) ∧
      (∀ i : Fin (numExp lam0 d),
        ∀ v ∈ (V i.castSucc x : Set (EuclideanSpace ℝ (Fin d))), v ∉ V i.succ x →
          Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
            Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A (⇑T) n x) v‖)
            atTop (𝓝 (expEnum lam0 d i))) := by
    filter_upwards [hVae] with x hx
    exact ⟨hx.1, hx.2.1, hx.2.2.1, hx.2.2.2.1, hx.2.2.2.2.1⟩
  -- The a.e. crux, counting bound, reflection.
  have hcrux := ae_crux hT hA hAmeas hint hint' lam0 mu0 V W hVmeas hVstruct hWstruct
  have hcount := ae_counting (μ := μ) lam0 mu0 V W hVdim hWdim hcrux
  have hsum := sum_mu0_eq_neg_sum_lam0 hT hA hAmeas hint hint' lam0 mu0 hlam0sv hmu0sv
  have hrefl : ∀ j : ℕ, j < d → mu0 j = -lam0 (d - 1 - j) :=
    reflect_of_counting_and_sum hlam0mono hmu0mono hcount hsum
  -- The backward equivariance, pushed to the forward image `T x`.
  have hWmapTx : ∀ᵐ x ∂μ, ∀ s : Fin (numExp mu0 d + 1),
      Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (backwardGen A T (T x))).toLinearMap
        (W s (T x)) = W s x := by
    have hWmap_ae : ∀ᵐ y ∂μ, ∀ s : Fin (numExp mu0 d + 1),
        Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (backwardGen A T y)).toLinearMap
          (W s y) = W s (T.symm y) := by
      filter_upwards [hWae] with y hy; exact hy.2.2.2.1
    filter_upwards [hmp.quasiMeasurePreserving.ae hWmap_ae] with x hx s
    have := hx s
    rwa [T.symm_apply_apply] at this
  -- The split bundle.
  refine ⟨numExp lam0 d, expEnum lam0 d,
    fun i x => V i.castSucc x ⊓ W (sidx hrefl i).castSucc x,
    expEnum_strictAnti lam0 d, ?_, ?_⟩
  · intro i
    exact MeasurableSubspace.inf (hVmeas i.castSucc) (hWmeas (sidx hrefl i).castSucc)
  -- The a.e. structural block.
  filter_upwards [hVae, hWae, hcrux, hWmapTx] with x hVx hWx hcx hWmapTxx
  obtain ⟨hV0, hVlast, hVstrict, hVmap, hVgrow, _hVd⟩ := hVx
  obtain ⟨_hW0, hWlast, hWstrict, _hWmap, hWgrow, _hWd⟩ := hWx
  -- Point-flag values and their basic order/structure.
  set Vx : Fin (numExp lam0 d + 1) → Submodule ℝ (EuclideanSpace ℝ (Fin d)) :=
    fun i => V i x with hVxdef
  set Wx : Fin (numExp mu0 d + 1) → Submodule ℝ (EuclideanSpace ℝ (Fin d)) :=
    fun s => W s x with hWxdef
  have hVanti : Antitone Vx := (Fin.strictAnti_iff_succ_lt.mpr hVstrict).antitone
  have hVlast' : Vx (Fin.last (numExp lam0 d)) = ⊥ := hVlast
  have hWlast' : Wx (Fin.last (numExp mu0 d)) = ⊥ := hWlast
  have hVdimx : ∀ i : Fin (numExp lam0 d),
      Module.finrank ℝ (Vx i.castSucc)
        = ((Finset.range d).filter (fun j => lam0 j ≤ expEnum lam0 d i)).card := _hVd
  have hWdimx : ∀ s : Fin (numExp mu0 d),
      Module.finrank ℝ (Wx s.castSucc)
        = ((Finset.range d).filter (fun j => mu0 j ≤ expEnum mu0 d s)).card := _hWd
  have hcruxx : ∀ (i' : Fin (numExp lam0 d)) (s : Fin (numExp mu0 d)),
      expEnum lam0 d i' + expEnum mu0 d s < 0 → Vx i'.castSucc ⊓ Wx s.castSucc = ⊥ := hcx
  -- The split subspace at the point is `esplitAt`.
  have hEeq : ∀ i : Fin (numExp lam0 d),
      V i.castSucc x ⊓ W (sidx hrefl i).castSucc x = esplitAt (Vx := Vx) (Wx := Wx) hrefl i := by
    intro i; rfl
  refine ⟨?_, ?_, ?_, ?_⟩
  · -- IsInternal via the telescoping-flag lattice lemma.
    rw [DirectSum.isInternal_submodule_iff_iSupIndep_and_iSup_eq_top]
    obtain ⟨hindep, hsupeq⟩ := flag_iSupIndep_and_iSup Vx (fun i => esplitAt hrefl i)
      hVlast'
      (fun i => Vcast_eq_esplitAt_sup_Vsucc hrefl hVdimx hWdimx hVanti hVlast' hcruxx i)
      (fun i => esplitAt_inf_Vsucc hrefl hVlast' hcruxx i)
    constructor
    · simpa only [hEeq] using hindep
    · rw [show (fun i => V i.castSucc x ⊓ W (sidx hrefl i).castSucc x)
          = fun i => esplitAt (Vx := Vx) (Wx := Wx) hrefl i from funext hEeq, hsupeq]
      exact hV0
  · -- Each split subspace is nonzero.
    intro i
    rw [hEeq i]
    exact Submodule.one_le_finrank_iff.mp
      (one_le_finrank_esplitAt hrefl hVdimx hWdimx hVanti hVlast' hcruxx i)
  · -- Equivariance: `map (A x) (E i x) = E i (T x)`.
    intro i
    have hinj : Function.Injective ⇑(Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap := by
      rw [ContinuousLinearMap.coe_coe]
      -- `toEuclideanCLM (A x)⁻¹` is a left inverse, hence the map is injective.
      have hmul : Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)⁻¹
          * Matrix.toEuclideanCLM (𝕜 := ℝ) (A x) = 1 := by
        rw [← map_mul, Matrix.nonsing_inv_mul _ (Ne.isUnit (hA x)), map_one]
      have hli : Function.LeftInverse
          ⇑(Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)⁻¹)
          ⇑(Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)) := by
        intro v
        rw [← ContinuousLinearMap.mul_apply, hmul, ContinuousLinearMap.one_apply]
      exact hli.injective
    rw [Submodule.map_inf (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap hinj]
    -- forward part
    have hVpart : Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap
        (V i.castSucc x) = V i.castSucc (T x) := hVmap i.castSucc
    -- backward part, transported through `(A x)⁻¹`
    have hWpart : Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap
        (W (sidx hrefl i).castSucc x) = W (sidx hrefl i).castSucc (T x) := by
      apply map_of_map_inv (hA x)
      have hbg : backwardGen A T (T x) = (A x)⁻¹ := by
        rw [backwardGen, T.symm_apply_apply]
      have := hWmapTxx (sidx hrefl i).castSucc
      rwa [hbg] at this
    rw [hVpart, hWpart]
  · -- Two-sided growth.
    intro i v hv hv0
    have hvV : v ∈ V i.castSucc x := (Submodule.mem_inf.mp hv).1
    have hvW : v ∈ W (sidx hrefl i).castSucc x := (Submodule.mem_inf.mp hv).2
    -- forward stratum: `v ∉ V i.succ x`
    have hvVnot : v ∉ V i.succ x := by
      intro hmem
      have : v ∈ esplitAt (Vx := Vx) (Wx := Wx) hrefl i ⊓ Vx i.succ :=
        Submodule.mem_inf.mpr ⟨hv, hmem⟩
      rw [esplitAt_inf_Vsucc hrefl hVlast' hcruxx i, Submodule.mem_bot] at this
      exact hv0 this
    -- backward stratum: `v ∉ W (sidx i).succ x`
    have hvWnot : v ∉ W (sidx hrefl i).succ x := by
      intro hmem
      have : v ∈ Vx i.castSucc ⊓ Wx (sidx hrefl i).succ :=
        Submodule.mem_inf.mpr ⟨hvV, hmem⟩
      rw [crux_succ_backward hrefl hWlast' hcruxx i, Submodule.mem_bot] at this
      exact hv0 this
    refine ⟨hVgrow i v hvV hvVnot, ?_⟩
    have hbw := hWgrow (sidx hrefl i) v hvW hvWnot
    rw [sidx_exp hrefl i] at hbw
    -- rewrite the backward cocycle through the identity `cocycle_backwardGen`
    simp only [cocycle_backwardGen] at hbw
    exact hbw

end Pos

/-! ### The dimension-zero case -/

private theorem euclidean_zero_subsingleton : Subsingleton (EuclideanSpace ℝ (Fin 0)) :=
  ⟨fun a b => by ext i; exact i.elim0⟩

/-- **The two-sided Oseledets splitting, dimension-zero case.** Trivial: `k = 0`, the empty
internal direct sum of the zero module. -/
theorem oseledets_splitting_dim_zero
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X ≃ᵐ X}
    (_hT : Ergodic T μ)
    (A : X → Matrix (Fin 0) (Fin 0) ℝ)
    (_hA : ∀ x, (A x).det ≠ 0)
    (_hAmeas : Measurable A)
    (_hint : IntegrableLogNorm A μ)
    (_hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∃ (k : ℕ) (lam : Fin k → ℝ)
      (E : Fin k → X → Submodule ℝ (EuclideanSpace ℝ (Fin 0))),
      StrictAnti lam ∧
      (∀ i, MeasurableSubspace fun x => E i x) ∧
      ∀ᵐ x ∂μ,
        DirectSum.IsInternal (fun i => E i x) ∧
        (∀ i, E i x ≠ ⊥) ∧
        (∀ i, Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap (E i x)
          = E i (T x)) ∧
        (∀ i, ∀ v ∈ E i x, v ≠ 0 →
          Tendsto
            (fun n : ℕ => (n : ℝ)⁻¹ *
              Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖)
            atTop (𝓝 (lam i)) ∧
          Tendsto
            (fun n : ℕ => (n : ℝ)⁻¹ *
              Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ)
                (cocycle A T n ((⇑T.symm)^[n] x))⁻¹ v‖)
            atTop (𝓝 (-lam i))) := by
  refine ⟨0, fun i => i.elim0, fun i => i.elim0, fun i => i.elim0, fun i => i.elim0, ?_⟩
  refine Eventually.of_forall fun x => ⟨?_, fun i => i.elim0, fun i => i.elim0, fun i => i.elim0⟩
  rw [DirectSum.isInternal_submodule_iff_iSupIndep_and_iSup_eq_top]
  haveI := euclidean_zero_subsingleton
  exact ⟨iSupIndep_subsingleton _, Subsingleton.elim _ _⟩

/-! ### The two-sided Oseledets splitting -/

/-- **The two-sided Oseledets multiplicative ergodic theorem (splitting form).**

For an *invertible* ergodic measure-preserving system `T : X ≃ᵐ X` and a measurable
everywhere-invertible cocycle generator `A` with `log⁺‖A‖, log⁺‖A⁻¹‖ ∈ L¹(μ)`, there are
`k` distinct Lyapunov exponents `λ₀ > ⋯ > λ_{k-1}` and a measurable, `A`-equivariant
**splitting** `ℝᵈ = E₀(x) ⊕ ⋯ ⊕ E_{k-1}(x)` of `EuclideanSpace ℝ (Fin d)` such that, for
`μ`-a.e. `x`, every nonzero `v ∈ Eᵢ(x)` grows forward at rate `λᵢ` and backward at rate
`−λᵢ`:
`(1/n) log‖A⁽ⁿ⁾(x) v‖ → λᵢ` and `(1/n) log‖(A⁽ⁿ⁾(T⁻ⁿx))⁻¹ v‖ → −λᵢ`. -/
theorem oseledets_splitting
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X ≃ᵐ X}
    (hT : Ergodic T μ)
    (A : X → Matrix (Fin d) (Fin d) ℝ)
    (hA : ∀ x, (A x).det ≠ 0)
    (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ)
    (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∃ (k : ℕ) (lam : Fin k → ℝ)
      (E : Fin k → X → Submodule ℝ (EuclideanSpace ℝ (Fin d))),
      StrictAnti lam ∧
      (∀ i, MeasurableSubspace fun x => E i x) ∧
      ∀ᵐ x ∂μ,
        DirectSum.IsInternal (fun i => E i x) ∧
        (∀ i, E i x ≠ ⊥) ∧
        (∀ i, Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap (E i x)
          = E i (T x)) ∧
        (∀ i, ∀ v ∈ E i x, v ≠ 0 →
          Tendsto
            (fun n : ℕ => (n : ℝ)⁻¹ *
              Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖)
            atTop (𝓝 (lam i)) ∧
          Tendsto
            (fun n : ℕ => (n : ℝ)⁻¹ *
              Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ)
                (cocycle A T n ((⇑T.symm)^[n] x))⁻¹ v‖)
            atTop (𝓝 (-lam i))) := by
  rcases Nat.eq_zero_or_pos d with hd | hd
  · subst hd
    exact oseledets_splitting_dim_zero hT A hA hAmeas hint hint'
  · haveI : NeZero d := ⟨hd.ne'⟩
    exact oseledets_splitting_pos hT A hA hAmeas hint hint'

end ErgodicTheory
