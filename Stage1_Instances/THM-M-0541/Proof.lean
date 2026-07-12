import Mathlib.AlgebraicTopology.SimplicialComplex.Basic
import Mathlib.Data.Finsupp.Basic
import Mathlib.Data.Finset.Sort
import Mathlib.Algebra.BigOperators.Finsupp.Basic

namespace Stage1Instances.THM_M_0541

open Finset

universe u

variable {V : Type u} [LinearOrder V]

def Simplex (K : AbstractSimplicialComplex V) (n : Nat) :=
  {s : Finset V // s ∈ K ∧ s.card = n + 1}

def face {K : AbstractSimplicialComplex V} {n : Nat}
    (sigma : Simplex K (n + 1)) (i : Fin (n + 2)) : Simplex K n := by
  let v := sigma.1.orderEmbOfFin sigma.2.2 i
  refine ⟨sigma.1.erase v, ?_, ?_⟩
  · exact (K.isRelLowerSet_faces sigma.2.1).2 (erase_subset _ _) (card_pos.mp (by
      dsimp [v]
      rw [card_erase_of_mem (sigma.1.orderEmbOfFin_mem sigma.2.2 i), sigma.2.2]
      omega))
  · rw [card_erase_of_mem (sigma.1.orderEmbOfFin_mem sigma.2.2 i), sigma.2.2]
    omega

abbrev Chains (K : AbstractSimplicialComplex V) (n : Nat) := Simplex K n →₀ ℤ

def HasAlternatingBoundary (K : AbstractSimplicialComplex V)
    (d : (n : Nat) → Chains K (n + 1) →+ Chains K n) : Prop :=
  ∀ (n : Nat) (sigma : Simplex K (n + 1)),
    d n (Finsupp.single sigma 1) =
      ∑ i : Fin (n + 2), Finsupp.single (face sigma i) ((-1 : ℤ) ^ (i : Nat))

def CanonicalTarget (K : AbstractSimplicialComplex V) : Prop :=
  ∃ d : (n : Nat) → Chains K (n + 1) →+ Chains K n,
    HasAlternatingBoundary K d ∧
      ∀ (n : Nat) (c : Chains K (n + 2)), d n (d (n + 1) c) = 0

def StatementShape : Prop :=
  ∀ (V : Type u) [LinearOrder V] (K : AbstractSimplicialComplex V), CanonicalTarget K

lemma orderEmbOfFin_erase_apply {s : Finset V} {m : Nat} (hs : s.card = m + 1)
    (j : Fin (m + 1)) (i : Fin m) :
    (s.erase (s.orderEmbOfFin hs j)).orderEmbOfFin (by
      rw [card_erase_of_mem (s.orderEmbOfFin_mem hs j), hs]
      omega) i =
      s.orderEmbOfFin hs (j.succAbove i) := by
  let hcard : (s.erase (s.orderEmbOfFin hs j)).card = m := by
    rw [card_erase_of_mem (s.orderEmbOfFin_mem hs j), hs]
    omega
  let f : Fin m → V := fun i => s.orderEmbOfFin hs (j.succAbove i)
  have hf_mem : ∀ i, f i ∈ s.erase (s.orderEmbOfFin hs j) := by
    intro i
    simp only [mem_erase, f, orderEmbOfFin_mem, and_true]
    exact fun h => Fin.succAbove_ne j i ((s.orderEmbOfFin hs).injective h)
  have hf_mono : StrictMono f :=
    (s.orderEmbOfFin hs).strictMono.comp (Fin.strictMono_succAbove j)
  exact congrFun (orderEmbOfFin_unique hcard hf_mem hf_mono) i |>.symm

lemma face_face {K : AbstractSimplicialComplex V} {n : Nat}
    (sigma : Simplex K (n + 2)) (i : Fin (n + 2)) (j : Fin (n + 3))
    (hji : (j : Nat) ≤ (i : Nat)) :
    face (face sigma j) i = face (face sigma i.succ) (Fin.castLT j (by omega)) := by
  apply Subtype.ext
  dsimp [face]
  rw [orderEmbOfFin_erase_apply]
  have hsucc : j.succAbove i = i.succ := by
    exact Fin.succAbove_of_le_castSucc j i (by simpa using hji)
  rw [hsucc, erase_right_comm]
  rw [orderEmbOfFin_erase_apply]
  congr 2
  symm
  exact Fin.succAbove_succ_of_le i (Fin.castLT j (by omega)) (by simpa using hji)

/-- The alternating boundary, extended additively from basis simplices. -/
noncomputable def boundary (K : AbstractSimplicialComplex V) (n : Nat) :
    Chains K (n + 1) →+ Chains K n :=
  Finsupp.liftAddHom (fun sigma =>
    { toFun := fun z => ∑ i : Fin (n + 2), Finsupp.single (face sigma i) (z * ((-1 : ℤ) ^ (i : Nat)))
      map_zero' := by simp
      map_add' := by
        intro a b
        simp only [add_mul, Finsupp.single_add, Finset.sum_add_distrib] })

@[simp] lemma boundary_single (K : AbstractSimplicialComplex V) (n : Nat)
    (sigma : Simplex K (n + 1)) (z : ℤ) :
    boundary K n (Finsupp.single sigma z) =
      ∑ i : Fin (n + 2), Finsupp.single (face sigma i) (z * ((-1 : ℤ) ^ (i : Nat))) := by
  simp [boundary]

lemma boundary_squared_single (K : AbstractSimplicialComplex V) (n : Nat)
    (sigma : Simplex K (n + 2)) :
    boundary K n (boundary K (n + 1) (Finsupp.single sigma 1)) = 0 := by
  simp only [boundary_single, one_mul, map_sum]
  rw [Finset.sum_comm]
  rw [← Finset.sum_product']
  let P := Fin (n + 2) × Fin (n + 3)
  let S : Finset P := {ij : P | (ij.2 : Nat) ≤ (ij.1 : Nat)}
  rw [Finset.univ_product_univ, ← Finset.sum_add_sum_compl S]
  -- Pair `(i,j)` with `(j,i+1)`; the two coefficients are opposite.
  let phi : ∀ ij : P, ij ∈ S → P := fun ij hij =>
    (Fin.castLT ij.2 (lt_of_le_of_lt (Finset.mem_filter.mp hij).2 (Fin.is_lt ij.1)), ij.1.succ)
  rw [show ∑ x ∈ Sᶜ, Finsupp.single (face (face sigma x.2) x.1)
        (((-1 : ℤ) ^ (x.2 : Nat)) * ((-1 : ℤ) ^ (x.1 : Nat))) =
      ∑ x ∈ S, -Finsupp.single (face (face sigma x.2) x.1)
        (((-1 : ℤ) ^ (x.2 : Nat)) * ((-1 : ℤ) ^ (x.1 : Nat))) by
    symm
    apply Finset.sum_bij phi
    · intro ij hij
      simp_rw [S, phi, Finset.compl_filter, Finset.mem_filter_univ, Fin.val_succ,
        Fin.val_castLT] at hij ⊢
      omega
    · rintro ⟨i, j⟩ hij ⟨i', j'⟩ hij' h
      rw [Prod.mk_inj]
      exact ⟨by simpa [phi] using congrArg Prod.snd h,
        by simpa [phi, Fin.castSucc_castLT] using congrArg Fin.castSucc (congrArg Prod.fst h)⟩
    · rintro ⟨i', j'⟩ hij'
      simp_rw [S, Finset.compl_filter, Finset.mem_filter_univ, not_le] at hij'
      refine ⟨(j'.pred (by rintro rfl; simp at hij'), Fin.castSucc i'), ?_, ?_⟩
      · simpa [S] using Nat.le_sub_one_of_lt hij'
      · simp only [phi, Fin.castLT_castSucc, Fin.succ_pred]
    · rintro ⟨i, j⟩ hij
      have hji : (j : Nat) ≤ (i : Nat) := by simpa [S] using hij
      rw [face_face sigma i j hji]
      rw [← Finsupp.single_neg]
      congr 1
      simp only [phi, Fin.val_succ, Fin.val_castLT, pow_succ]
      ring
  ]
  simp

lemma boundary_squared (K : AbstractSimplicialComplex V) (n : Nat) (c : Chains K (n + 2)) :
    boundary K n (boundary K (n + 1) c) = 0 := by
  classical
  induction c using Finsupp.induction with
  | zero => simp
  | @single_add sigma z c hsigma hc ih =>
      rw [map_add, map_add, ih, add_zero]
      rw [show Finsupp.single sigma z = z • Finsupp.single sigma 1 by simp]
      simp only [map_zsmul]
      rw [boundary_squared_single]
      simp

theorem statementShape : StatementShape := by
  intro V _ K
  refine ⟨boundary K, ?_, boundary_squared K⟩
  intro n sigma
  simpa using boundary_single K n sigma 1

end Stage1Instances.THM_M_0541

#check (Stage1Instances.THM_M_0541.statementShape : Stage1Instances.THM_M_0541.StatementShape)
#print axioms Stage1Instances.THM_M_0541.statementShape
