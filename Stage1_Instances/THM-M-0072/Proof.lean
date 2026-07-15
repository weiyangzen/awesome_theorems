import ObligationTree
import Mathlib.GroupTheory.Transfer
import Mathlib.GroupTheory.Nilpotent
import Mathlib.GroupTheory.IndexNormal
import Mathlib.GroupTheory.GroupAction.Period

/-!
# THM-M-0072 proof

This module implements Thompson's transfer argument for Lemma 5.38(a)(i). A maximal subgroup
`M` of the Sylow 2-subgroup `S` is normal and has index two. Transfer from `G` to `S / M` must be
trivial, since otherwise its kernel has index two in `G`. If an involution `u` has no conjugate in
`M`, the orbit formula for transfer instead evaluates it to the nonidentity coset of `u`, because
the Sylow index is odd. This contradiction closes the outside-maximal branch; the checked
obligation-tree composition supplies the inside branch and the exact printed root.
-/

noncomputable section

open Function MulAction Subgroup

namespace Stage1Instances.THM_M_0072.Proof

open Stage1Instances.THM_M_0072
open Stage1Instances.THM_M_0072.ObligationTree

universe u

/-- A maximal subgroup of a finite p-group is normal. -/
theorem maximal_normal_of_pgroup
    {P : Type u} [Group P] [Finite P]
    {p : Nat} [Fact (Nat.Prime p)]
    (hp : IsPGroup p P) (M : Subgroup P) (hM : IsCoatom M) : M.Normal := by
  haveI : Group.IsNilpotent P := hp.isNilpotent
  exact Subgroup.NormalizerCondition.normal_of_coatom M
    normalizerCondition_of_isNilpotent hM

/-- The quotient by a normal maximal subgroup is simple. -/
theorem quotient_isSimpleGroup_of_isCoatom
    {P : Type u} [Group P] (M : Subgroup P) [M.Normal] (hM : IsCoatom M) :
    IsSimpleGroup (P ⧸ M) := by
  haveI : Nontrivial (P ⧸ M) := QuotientGroup.nontrivial_iff.mpr hM.ne_top
  refine ⟨?_⟩
  intro H _hH
  let q : P →* P ⧸ M := QuotientGroup.mk' M
  have hle : M ≤ H.comap q := QuotientGroup.le_comap_mk' M H
  rcases eq_or_lt_of_le hle with hEq | hLt
  · left
    apply Subgroup.comap_injective (QuotientGroup.mk'_surjective M)
    simpa [q, MonoidHom.comap_bot, QuotientGroup.ker_mk'] using hEq.symm
  · right
    have htop : H.comap q = ⊤ := hM.2 _ hLt
    apply Subgroup.comap_injective (QuotientGroup.mk'_surjective M)
    simpa [q] using htop

/-- A maximal subgroup of a finite p-group has index p. -/
theorem maximal_index_prime_of_pgroup
    {P : Type u} [Group P] [Finite P]
    {p : Nat} [Fact (Nat.Prime p)]
    (hp : IsPGroup p P) (M : Subgroup P) (hM : IsCoatom M) : M.index = p := by
  letI : M.Normal := maximal_normal_of_pgroup hp M hM
  letI : IsSimpleGroup (P ⧸ M) := quotient_isSimpleGroup_of_isCoatom M hM
  have hpq : IsPGroup p (P ⧸ M) := hp.to_quotient M
  haveI : Group.IsNilpotent (P ⧸ M) := hpq.isNilpotent
  letI : CommGroup (P ⧸ M) := inferInstance
  have hprime : (Nat.card (P ⧸ M)).Prime := IsSimpleGroup.prime_card
  have hindexprime : M.index.Prime := M.index_eq_card ▸ hprime
  obtain ⟨n, hn⟩ := hp.index M
  have hn_one : n = 1 := Nat.Prime.eq_one_of_pow (hn ▸ hindexprime)
  simpa [hn, hn_one]

/-- A maximal subgroup of a finite 2-group has index two. -/
theorem maximal_index_two_of_2group
    {P : Type u} [Group P] [Finite P]
    (hp : IsPGroup 2 P) (M : Subgroup P) (hM : IsCoatom M) : M.index = 2 := by
  letI : Fact (Nat.Prime 2) := ⟨Nat.prime_two⟩
  exact maximal_index_prime_of_pgroup hp M hM

/-- Every orbit of an involution has length one or two. -/
lemma period_eq_one_or_two
    {G : Type u} [Group G] [Finite G]
    (H : Subgroup G) (g : G) (hg : orderOf g = 2) (q : G ⧸ H) :
    Function.minimalPeriod (g • ·) q = 1 ∨ Function.minimalPeriod (g • ·) q = 2 := by
  have hdiv : Function.minimalPeriod (g • ·) q ∣ 2 := by
    rw [← hg]
    exact MulAction.period_dvd_orderOf g q
  exact (Nat.dvd_prime Nat.prime_two).mp hdiv

/-- In a quotient of order two, the two elements outside the kernel define the same coset. -/
lemma quotient_eq_of_both_not_mem
    {G : Type u} [Group G]
    (H : Subgroup G) (M : Subgroup H) [M.Normal]
    (hindex : M.index = 2) {a b : H} (ha : a ∉ M) (hb : b ∉ M) :
    (a : H ⧸ M) = (b : H ⧸ M) := by
  rw [QuotientGroup.eq_iff_div_mem, div_eq_mul_inv,
    M.mul_mem_iff_of_index_two hindex, M.inv_mem_iff]
  exact iff_of_false ha hb

/-- Thompson's outside-maximal transfer branch. -/
theorem outsideTransferConclusion : TransferOutsideTarget.{u} := by
  intro G _ _ _hEven hNoIndex S M hM u huM hu
  letI : Fact (Nat.Prime 2) := ⟨Nat.prime_two⟩
  letI : M.Normal := maximal_normal_of_pgroup S.isPGroup' M hM
  have hMindex : M.index = 2 := maximal_index_two_of_2group S.isPGroup' M hM

  let Q := S ⧸ M
  let quotientMap : S →* Q := QuotientGroup.mk' M
  have hQcard : Nat.card Q = 2 := by
    simpa [Q] using M.index_eq_card.symm.trans hMindex
  letI : IsCyclic Q := isCyclic_of_prime_card hQcard
  letI : CommGroup Q := IsCyclic.commGroup

  let x : Q := quotientMap u
  have huG : orderOf (u : G) = 2 := by simpa using hu
  have hu2 : u ^ 2 = 1 := (orderOf_eq_prime_iff.mp hu).1
  have huG2 : (u : G) ^ 2 = 1 := by
    simpa using congrArg ((↑) : S → G) hu2
  have hx2 : x ^ 2 = 1 := by
    dsimp [x]
    rw [← quotientMap.map_pow, hu2, quotientMap.map_one]
  have hx1 : x ≠ 1 := by
    intro hx
    apply huM
    exact (QuotientGroup.eq_one_iff u).mp (by simpa [x, quotientMap, Q] using hx)

  let transferMap : G →* Q := MonoidHom.transfer quotientMap
  have htransferTrivial : transferMap = 1 := by
    apply MonoidHom.range_eq_bot_iff.mp
    letI : Fact (Nat.card Q).Prime := ⟨hQcard.symm ▸ Nat.prime_two⟩
    rcases transferMap.range.eq_bot_or_eq_top_of_prime_card with hrange | hrange
    · exact hrange
    · exfalso
      have hker : transferMap.ker.index = 2 := by
        rw [Subgroup.index_ker, hrange, Subgroup.card_top, hQcard]
      have hnot : transferMap.ker.index ≠ 2 := by
        simpa [bne_iff_ne] using hNoIndex transferMap.ker
      exact hnot hker

  by_contra hconclusion
  push_neg at hconclusion
  let Orbits := Quotient
    (MulAction.orbitRel (zpowers (u : G)) (G ⧸ (S : Subgroup G)))
  letI : Fintype Orbits := Fintype.ofFinite Orbits

  have hfactor (q : Orbits) :
      quotientMap
          ⟨q.out.out⁻¹ * (u : G) ^ Function.minimalPeriod ((u : G) • ·) q.out * q.out.out,
            QuotientGroup.out_conj_pow_minimalPeriod_mem
              (S : Subgroup G) (u : G) q.out⟩ =
        x ^ Function.minimalPeriod ((u : G) • ·) q.out := by
    rcases period_eq_one_or_two (S : Subgroup G) (u : G) huG q.out with hn | hn
    · let conjugate : S :=
        ⟨q.out.out⁻¹ * (u : G) * q.out.out, by
          simpa [hn] using
            (QuotientGroup.out_conj_pow_minimalPeriod_mem
              (S : Subgroup G) (u : G) q.out)⟩
      have hconjugateM : conjugate ∉ M := by
        intro hc
        apply hconclusion ⟨conjugate, hc⟩
        apply isConj_iff.mpr
        refine ⟨q.out.out⁻¹, ?_⟩
        simp [conjugate]
      have hquotient : quotientMap conjugate = quotientMap u := by
        simpa [quotientMap, Q] using
          quotient_eq_of_both_not_mem (S : Subgroup G) M hMindex hconjugateM huM
      simpa [hn, conjugate, x] using hquotient
    · calc
        quotientMap
            ⟨q.out.out⁻¹ * (u : G) ^ Function.minimalPeriod ((u : G) • ·) q.out * q.out.out,
              QuotientGroup.out_conj_pow_minimalPeriod_mem
                (S : Subgroup G) (u : G) q.out⟩ = quotientMap 1 := by
                  congr 1
                  apply Subtype.ext
                  simp [hn, huG2]
        _ = 1 := quotientMap.map_one
        _ = x ^ Function.minimalPeriod ((u : G) • ·) q.out := by
          simp [hn, hx2]

  have htransferValue : transferMap (u : G) = x ^ (S : Subgroup G).index := by
    rw [MonoidHom.transfer_eq_prod_quotient_orbitRel_zpowers_quot
      (H := (S : Subgroup G)) quotientMap (u : G)]
    calc
      (∏ q : Orbits,
          quotientMap
            ⟨q.out.out⁻¹ * (u : G) ^ Function.minimalPeriod ((u : G) • ·) q.out * q.out.out,
              QuotientGroup.out_conj_pow_minimalPeriod_mem
                (S : Subgroup G) (u : G) q.out⟩) =
          ∏ q : Orbits, x ^ Function.minimalPeriod ((u : G) • ·) q.out := by
            apply Finset.prod_congr rfl
            intro q _
            exact hfactor q
      _ = x ^ ∑ q : Orbits, Function.minimalPeriod ((u : G) • ·) q.out := by
        rw [Finset.prod_pow_eq_pow_sum]
      _ = x ^ (S : Subgroup G).index := by
        rw [Subgroup.index_eq_sum_minimalPeriod (S : Subgroup G) (u : G)]

  have hindexOdd : Odd (S : Subgroup G).index := by
    rw [← Nat.not_even_iff_odd, even_iff_two_dvd]
    exact S.not_dvd_index
  obtain ⟨k, hk⟩ := hindexOdd
  have hpow : x ^ (S : Subgroup G).index = x := by
    rw [hk, pow_add, pow_mul, hx2, one_pow, one_mul, pow_one]
  have htransferOne : transferMap (u : G) = 1 := by
    rw [htransferTrivial]
    rfl
  exact hx1 (hpow.symm.trans (htransferValue.symm.trans htransferOne))

/-- The exact printed Thompson-transfer target, assembled from both maximal-subgroup branches. -/
theorem thompsonTransferLemma_proof : ThompsonTransferLemmaTarget.{u} :=
  root_of_outsideTransfer outsideTransferConclusion

#check (outsideTransferConclusion : TransferOutsideTarget.{u})
#check (thompsonTransferLemma_proof : ThompsonTransferLemmaTarget.{u})

#print axioms maximal_normal_of_pgroup
#print axioms maximal_index_two_of_2group
#print axioms outsideTransferConclusion
#print axioms thompsonTransferLemma_proof

set_option pp.universes true in
set_option pp.explicit true in
#print ThompsonTransferLemmaTarget

end Stage1Instances.THM_M_0072.Proof
