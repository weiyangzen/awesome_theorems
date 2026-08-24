import Mathlib
import FormalConjectures.Arxiv.«2605.12342».Conjecture1

/-!
The provider module supplies the frozen theorem type only.  Every proof term in
this package is claim-owned and independent of the provider theorem body.
-/

#check Arxiv.«2605.12342».conjecture_1.variants.rank_3_3

namespace AwesomeTheorems.Stage5.S5_CLM_00003520

open Equiv.Perm

private lemma closure_pair_ne_top
    {G : Type*} [Group G] (K : Subgroup G) {x y : G}
    (hx : x ∈ K) (hy : y ∈ K) (z : G) (hz : z ∉ K) :
    Subgroup.closure {x, y} ≠ ⊤ := by
  intro htop
  apply hz
  have hle : Subgroup.closure {x, y} ≤ K := by
    apply (Subgroup.closure_le K).2
    intro a ha
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at ha
    rcases ha with rfl | rfl
    · exact hx
    · exact hy
  apply hle
  rw [htop]
  trivial

private lemma odd_perm_exists :
    ∃ p : Equiv.Perm (Fin 3), Equiv.Perm.sign p ≠ 1 := by
  decide

private lemma moving_perm_exists :
    ∀ i : Fin 3, ∃ p : Equiv.Perm (Fin 3), p i ≠ i := by
  decide

private lemma nontrivial_even_perm_exists :
    ∃ p : Equiv.Perm (Fin 3), Equiv.Perm.sign p = 1 ∧ p ≠ 1 := by
  decide

set_option maxHeartbeats 4000000 in
private lemma pair_classification :
    ∀ p₁ p₂ q₁ q₂ : Equiv.Perm (Fin 3),
      Equiv.Perm.sign p₁ = Equiv.Perm.sign q₁ →
      Equiv.Perm.sign p₂ = Equiv.Perm.sign q₂ →
      (Equiv.Perm.sign p₁ = 1 ∧ Equiv.Perm.sign p₂ = 1) ∨
      (∃ i : Fin 3, p₁ i = i ∧ p₂ i = i) ∨
      (Equiv.Perm.sign q₁ = 1 ∧ Equiv.Perm.sign q₂ = 1) ∨
      (∃ i : Fin 3, q₁ i = i ∧ q₂ i = i) ∨
      (∃ c : Equiv.Perm (Fin 3),
        c * p₁ * c⁻¹ = q₁ ∧ c * p₂ * c⁻¹ = q₂) := by
  decide

private lemma first_even_obstruction
    {G : Subgroup (Equiv.Perm (Fin 3) × Equiv.Perm (Fin 3))}
    (hdiag : ∀ p : Equiv.Perm (Fin 3), (p, p) ∈ G)
    (x y : G)
    (hx : Equiv.Perm.sign x.1.1 = 1)
    (hy : Equiv.Perm.sign y.1.1 = 1) :
    Subgroup.closure {x, y} ≠ ⊤ := by
  let f : G →* ℤˣ :=
    Equiv.Perm.sign.comp ((MonoidHom.fst _ _).comp G.subtype)
  let K : Subgroup G := f.ker
  obtain ⟨p, hp⟩ := odd_perm_exists
  let z : G := ⟨(p, p), hdiag p⟩
  apply closure_pair_ne_top K hx hy z
  change Equiv.Perm.sign p ≠ 1
  exact hp

private lemma second_even_obstruction
    {G : Subgroup (Equiv.Perm (Fin 3) × Equiv.Perm (Fin 3))}
    (hdiag : ∀ p : Equiv.Perm (Fin 3), (p, p) ∈ G)
    (x y : G)
    (hx : Equiv.Perm.sign x.1.2 = 1)
    (hy : Equiv.Perm.sign y.1.2 = 1) :
    Subgroup.closure {x, y} ≠ ⊤ := by
  let f : G →* ℤˣ :=
    Equiv.Perm.sign.comp ((MonoidHom.snd _ _).comp G.subtype)
  let K : Subgroup G := f.ker
  obtain ⟨p, hp⟩ := odd_perm_exists
  let z : G := ⟨(p, p), hdiag p⟩
  apply closure_pair_ne_top K hx hy z
  change Equiv.Perm.sign p ≠ 1
  exact hp

private lemma first_fixed_obstruction
    {G : Subgroup (Equiv.Perm (Fin 3) × Equiv.Perm (Fin 3))}
    (hdiag : ∀ p : Equiv.Perm (Fin 3), (p, p) ∈ G)
    (i : Fin 3) (x y : G)
    (hx : x.1.1 i = i) (hy : y.1.1 i = i) :
    Subgroup.closure {x, y} ≠ ⊤ := by
  let K : Subgroup G :=
    { carrier := {a | a.1.1 i = i}
      one_mem' := by rfl
      mul_mem' := by
        intro a b ha hb
        change a.1.1 (b.1.1 i) = i
        rw [hb, ha]
      inv_mem' := by
        intro a ha
        change (a.1.1).symm i = i
        calc
          (a.1.1).symm i = (a.1.1).symm (a.1.1 i) := by rw [ha]
          _ = i := (a.1.1).symm_apply_apply i }
  obtain ⟨p, hp⟩ := moving_perm_exists i
  let z : G := ⟨(p, p), hdiag p⟩
  apply closure_pair_ne_top K hx hy z
  change p i ≠ i
  exact hp

private lemma second_fixed_obstruction
    {G : Subgroup (Equiv.Perm (Fin 3) × Equiv.Perm (Fin 3))}
    (hdiag : ∀ p : Equiv.Perm (Fin 3), (p, p) ∈ G)
    (i : Fin 3) (x y : G)
    (hx : x.1.2 i = i) (hy : y.1.2 i = i) :
    Subgroup.closure {x, y} ≠ ⊤ := by
  let K : Subgroup G :=
    { carrier := {a | a.1.2 i = i}
      one_mem' := by rfl
      mul_mem' := by
        intro a b ha hb
        change a.1.2 (b.1.2 i) = i
        rw [hb, ha]
      inv_mem' := by
        intro a ha
        change (a.1.2).symm i = i
        calc
          (a.1.2).symm i = (a.1.2).symm (a.1.2 i) := by rw [ha]
          _ = i := (a.1.2).symm_apply_apply i }
  obtain ⟨p, hp⟩ := moving_perm_exists i
  let z : G := ⟨(p, p), hdiag p⟩
  apply closure_pair_ne_top K hx hy z
  change p i ≠ i
  exact hp

private lemma conjugate_graph_obstruction
    {G : Subgroup (Equiv.Perm (Fin 3) × Equiv.Perm (Fin 3))}
    (hevenRight : ∀ p : Equiv.Perm (Fin 3),
      Equiv.Perm.sign p = 1 → ((1, p) : Equiv.Perm (Fin 3) × Equiv.Perm (Fin 3)) ∈ G)
    (c : Equiv.Perm (Fin 3)) (x y : G)
    (hx : c * x.1.1 * c⁻¹ = x.1.2)
    (hy : c * y.1.1 * c⁻¹ = y.1.2) :
    Subgroup.closure {x, y} ≠ ⊤ := by
  let K : Subgroup G :=
    { carrier := {a | c * a.1.1 * c⁻¹ = a.1.2}
      one_mem' := by
        change c * 1 * c⁻¹ = 1
        group
      mul_mem' := by
        intro a b ha hb
        change c * (a.1.1 * b.1.1) * c⁻¹ = a.1.2 * b.1.2
        calc
          c * (a.1.1 * b.1.1) * c⁻¹ =
              (c * a.1.1 * c⁻¹) * (c * b.1.1 * c⁻¹) := by group
          _ = a.1.2 * b.1.2 := by rw [ha, hb]
      inv_mem' := by
        intro a ha
        change c * a.1.1⁻¹ * c⁻¹ = a.1.2⁻¹
        calc
          c * a.1.1⁻¹ * c⁻¹ = (c * a.1.1 * c⁻¹)⁻¹ := by group
          _ = a.1.2⁻¹ := by rw [ha] }
  obtain ⟨p, hpEven, hpNontrivial⟩ := nontrivial_even_perm_exists
  let z : G := ⟨(1, p), hevenRight p hpEven⟩
  apply closure_pair_ne_top K hx hy z
  change c * 1 * c⁻¹ ≠ p
  intro h
  apply hpNontrivial
  simpa using h.symm

private lemma sign_eq_of_signDiff_mem
    {p q : Equiv.Perm (Fin 3)}
    (h : (p, q) ∈
      ((Equiv.Perm.sign.comp
          (MonoidHom.fst (Equiv.Perm (Fin 3)) (Equiv.Perm (Fin 3)))) *
        (Equiv.Perm.sign.comp
          (MonoidHom.snd (Equiv.Perm (Fin 3)) (Equiv.Perm (Fin 3))))⁻¹).ker) :
    Equiv.Perm.sign p = Equiv.Perm.sign q := by
  change Equiv.Perm.sign p * (Equiv.Perm.sign q)⁻¹ = 1 at h
  calc
    Equiv.Perm.sign p =
        (Equiv.Perm.sign p * (Equiv.Perm.sign q)⁻¹) * Equiv.Perm.sign q := by group
    _ = 1 * Equiv.Perm.sign q := by rw [h]
    _ = Equiv.Perm.sign q := one_mul _

private lemma diagonal_mem_signDiff (p : Equiv.Perm (Fin 3)) :
    (p, p) ∈
      ((Equiv.Perm.sign.comp
          (MonoidHom.fst (Equiv.Perm (Fin 3)) (Equiv.Perm (Fin 3)))) *
        (Equiv.Perm.sign.comp
          (MonoidHom.snd (Equiv.Perm (Fin 3)) (Equiv.Perm (Fin 3))))⁻¹).ker := by
  change Equiv.Perm.sign p * (Equiv.Perm.sign p)⁻¹ = 1
  exact mul_inv_cancel _

private lemma even_right_mem_signDiff (p : Equiv.Perm (Fin 3))
    (hp : Equiv.Perm.sign p = 1) :
    ((1, p) : Equiv.Perm (Fin 3) × Equiv.Perm (Fin 3)) ∈
      ((Equiv.Perm.sign.comp
          (MonoidHom.fst (Equiv.Perm (Fin 3)) (Equiv.Perm (Fin 3)))) *
        (Equiv.Perm.sign.comp
          (MonoidHom.snd (Equiv.Perm (Fin 3)) (Equiv.Perm (Fin 3))))⁻¹).ker := by
  change Equiv.Perm.sign (1 : Equiv.Perm (Fin 3)) * (Equiv.Perm.sign p)⁻¹ = 1
  simp [hp]

/--
The claim-owned, source-definition-expanded form of the frozen rank-three
exception.  It states that no two elements generate the equal-sign subgroup of
`Equiv.Perm (Fin 3) × Equiv.Perm (Fin 3)`.
-/
theorem rank_3_3_statement :
    ∀ h₁ h₂ :
      ((Equiv.Perm.sign.comp
          (MonoidHom.fst (Equiv.Perm (Fin 3)) (Equiv.Perm (Fin 3)))) *
        (Equiv.Perm.sign.comp
          (MonoidHom.snd (Equiv.Perm (Fin 3)) (Equiv.Perm (Fin 3))))⁻¹).ker,
      Subgroup.closure {h₁, h₂} ≠ ⊤ := by
  intro h₁ h₂
  have hs₁ : Equiv.Perm.sign h₁.1.1 = Equiv.Perm.sign h₁.1.2 :=
    sign_eq_of_signDiff_mem h₁.property
  have hs₂ : Equiv.Perm.sign h₂.1.1 = Equiv.Perm.sign h₂.1.2 :=
    sign_eq_of_signDiff_mem h₂.property
  rcases pair_classification h₁.1.1 h₂.1.1 h₁.1.2 h₂.1.2 hs₁ hs₂ with
      hEvenFirst | hFixFirst | hEvenSecond | hFixSecond | hGraph
  · exact first_even_obstruction diagonal_mem_signDiff h₁ h₂
      hEvenFirst.1 hEvenFirst.2
  · obtain ⟨i, hi₁, hi₂⟩ := hFixFirst
    exact first_fixed_obstruction diagonal_mem_signDiff i h₁ h₂ hi₁ hi₂
  · exact second_even_obstruction diagonal_mem_signDiff h₁ h₂
      hEvenSecond.1 hEvenSecond.2
  · obtain ⟨i, hi₁, hi₂⟩ := hFixSecond
    exact second_fixed_obstruction diagonal_mem_signDiff i h₁ h₂ hi₁ hi₂
  · obtain ⟨c, hc₁, hc₂⟩ := hGraph
    exact conjugate_graph_obstruction even_right_mem_signDiff c h₁ h₂ hc₁ hc₂

/-- Forward half of the bidirectional expanded-source crosswalk. -/
theorem source_to_target_transport :
    type_of% Arxiv.«2605.12342».conjecture_1.variants.rank_3_3 →
    type_of% rank_3_3_statement := id

/-- Reverse half of the bidirectional expanded-source crosswalk. -/
theorem target_to_source_transport :
    type_of% rank_3_3_statement →
    type_of% Arxiv.«2605.12342».conjecture_1.variants.rank_3_3 := id

/-- Trust-zero local closure at exactly the frozen provider theorem type. -/
theorem rank_3_3 : type_of% Arxiv.«2605.12342».conjecture_1.variants.rank_3_3 :=
  target_to_source_transport rank_3_3_statement

/-- Audit wrapper: the audited root and public root have definitionally equal types. -/
theorem rank_3_3_audit : type_of% Arxiv.«2605.12342».conjecture_1.variants.rank_3_3 :=
  rank_3_3

example : type_of% Arxiv.«2605.12342».conjecture_1.variants.rank_3_3 := AwesomeTheorems.Stage5.S5_CLM_00003520.rank_3_3
#print axioms AwesomeTheorems.Stage5.S5_CLM_00003520.rank_3_3

end AwesomeTheorems.Stage5.S5_CLM_00003520
