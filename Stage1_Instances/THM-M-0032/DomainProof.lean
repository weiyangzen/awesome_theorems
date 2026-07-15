import ObligationTree
import Mathlib.RingTheory.Ideal.MinimalPrime.Noetherian
import Mathlib.Util.AssertNoSorry

/-!
# THM-M-0032 regular-local domain package

This module implements the frozen `M0032-N-DOMAIN` obligation.  It proves domainhood from the exact
regular-local context by induction on the minimal number of generators of the maximal ideal.  The
body is only provisional evidence until master acceptance, and it does not prove the separate
prime-element package or the UFD root.
-/

namespace Stage1Instances.THM_M_0032.DomainProof

open IsLocalRing

universe u

local notation "m" => IsLocalRing.maximalIdeal

private theorem Ideal.toCotangent_out {R : Type*} [CommRing R]
    (I : Ideal R) (q : I.Cotangent) :
    I.toCotangent (Quotient.out q) = q := by
  rw [Ideal.toCotangent_apply I, ← Submodule.Quotient.mk''_eq_mk, Quotient.out_eq']

private theorem spanRank_quot_singleton_le
    {R : Type u} {x : R} [CommRing R] [IsLocalRing R]
    [Nontrivial (R ⧸ Ideal.span {x})] [IsLocalRing (R ⧸ Ideal.span {x})] :
    (m R).spanRank ≤ (m (R ⧸ Ideal.span {x})).spanRank + 1 := by
  obtain ⟨s, hs1, hs2⟩ := Submodule.exists_span_set_card_eq_spanRank (m (R ⧸ Ideal.span {x}))
  let s' : Set R := Quotient.out '' s
  have ims' : Ideal.Quotient.mk (Ideal.span {x}) '' s' = s := by
    ext y
    simp [s']
  have mapsp := Ideal.map_span (Ideal.Quotient.mk (Ideal.span {x})) s'
  rw [ims'] at mapsp
  have hs2' : Ideal.span s = m (R ⧸ Ideal.span {x}) := hs2
  rw [hs2'] at mapsp
  have comapmap := Ideal.comap_map_of_surjective'
    (Ideal.Quotient.mk (Ideal.span {x})) Ideal.Quotient.mk_surjective (Ideal.span s')
  letI : IsLocalHom (Ideal.Quotient.mk (Ideal.span {x})) :=
    IsLocalHom.of_surjective _ Ideal.Quotient.mk_surjective
  have hcomap : Ideal.comap (Ideal.Quotient.mk (Ideal.span {x}))
      (m (R ⧸ Ideal.span {x})) = m R := IsLocalRing.maximalIdeal_comap _
  rw [mapsp, hcomap, Ideal.mk_ker, ← Ideal.span_union] at comapmap
  have a : Cardinal.mk (s' ∪ {x} : Set R) ≤ Cardinal.mk s' + 1 := by
    simpa using Cardinal.mk_union_le s' {x}
  have ss' : Cardinal.mk s' ≤ Cardinal.mk s := Cardinal.mk_image_le
  have srle := Submodule.spanRank_span_le_card (R := R) (s' ∪ {x})
  change (Ideal.span (s' ∪ {x})).spanRank ≤ _ at srle
  rw [← comapmap] at srle
  rw [← hs1]
  exact srle.trans (a.trans (by simpa [add_comm] using add_le_add_right ss' 1))

private theorem exists_minimal_generators_containing
    {R : Type u} {x : R} [CommRing R] [IsLocalRing R] [IsNoetherianRing R]
    (hx1 : x ∈ m R) (hx2 : x ∉ (m R) ^ 2) :
    ∃ s : Set R, Ideal.span s = m R ∧ Cardinal.mk s = (m R).spanRank ∧ x ∈ s := by
  let x' : m R := ⟨x, hx1⟩
  have hx' : (m R).toCotangent x' ≠ 0 := by
    rw [ne_eq, Ideal.toCotangent_eq_zero]
    exact hx2
  let s' : Set ((m R).Cotangent) := {(m R).toCotangent x'}
  have li : LinearIndepOn (ResidueField R) id s' :=
    LinearIndepOn.singleton hx'
  let B := Module.Basis.extend li
  let S := Set.range (DFunLike.coe B)
  have Srw : S = li.extend (Set.subset_univ s') := Module.Basis.range_extend li
  have hxS : (m R).toCotangent x' ∈ S := by
    rw [Srw]
    exact Module.Basis.subset_extend li rfl
  have Sspan : Submodule.span (ResidueField R) S = ⊤ := Module.Basis.span_eq B
  have Scard : Cardinal.mk S = (m R).spanRank := by
    have h := Module.Basis.mk_eq_rank'' B
    have hrank : Module.rank (ResidueField R) (m R).Cotangent =
        Module.finrank (ResidueField R) (m R).Cotangent :=
      (Module.finrank_eq_rank (ResidueField R) (m R).Cotangent).symm
    rw [hrank, ← IsLocalRing.spanFinrank_maximalIdeal_eq_finrank_cotangentSpace R,
      ← Srw] at h
    have hfg : (m R).spanRank = (m R).spanFinrank :=
      Submodule.FG.spanRank_eq_spanFinrank (m R).fg_of_isNoetherianRing
    rw [← hfg] at h
    exact h
  let S' := S \ {(m R).toCotangent x'}
  have hS_union : S = S' ∪ {(m R).toCotangent x'} := by
    simp [S', hxS]
  have S'card : Cardinal.mk S = Cardinal.mk S' + 1 := by
    rw [hS_union, ← Cardinal.mk_singleton ((m R).toCotangent x')]
    exact Cardinal.mk_union_of_disjoint Set.disjoint_sdiff_left
  let s'' : Set (m R) := Quotient.out '' S'
  let s : Set (m R) := s'' ∪ {x'}
  have hcard_s'' : Cardinal.mk s'' = Cardinal.mk S' :=
    Cardinal.mk_image_eq Quotient.out_injective
  have hx_not_s'' : x' ∉ s'' := by
    intro hxmem
    have hout : (m R).toCotangent '' s'' = S' := by
      dsimp [s'']
      exact Function.LeftInverse.image_image (Ideal.toCotangent_out (m R)) S'
    have : (m R).toCotangent x' ∈ S' := by
      rw [← hout]
      exact Set.mem_image_of_mem _ hxmem
    exact this.2 rfl
  have scard : Cardinal.mk s = Cardinal.mk s'' + 1 := by
    dsimp [s]
    rw [← Cardinal.mk_singleton x']
    exact Cardinal.mk_union_of_disjoint (Set.disjoint_singleton_right.mpr hx_not_s'')
  have sim : (m R).toCotangent '' s = S := by
    dsimp [s]
    rw [Set.image_union, Set.image_singleton]
    have hout : (m R).toCotangent '' s'' = S' := by
      dsimp [s'']
      exact Function.LeftInverse.image_image (Ideal.toCotangent_out (m R)) S'
    rw [hout, ← hS_union]
  have sspan : Submodule.span R s = ⊤ := by
    apply IsLocalRing.CotangentSpace.span_image_eq_top_iff.mp
    rw [sim]
    exact Sspan
  refine ⟨(m R).subtype '' s, ?_, ?_, ?_⟩
  · change Submodule.span R ((m R).subtype '' s) = m R
    rw [← Submodule.map_span, sspan, Submodule.map_top, Submodule.range_subtype]
  · rw [Cardinal.mk_image_eq (m R).subtype_injective,
      scard, hcard_s'', ← S'card, Scard]
  · exact ⟨x', by simp [s], rfl⟩

private theorem spanRank_quot_singleton_ge
    {R : Type u} {x : R} [CommRing R] [IsLocalRing R] [IsNoetherianRing R]
    [Nontrivial (R ⧸ Ideal.span {x})]
    [IsLocalRing (R ⧸ Ideal.span {x})]
    (hx1 : x ∈ m R) (hx2 : x ∉ (m R) ^ 2) :
    (m (R ⧸ Ideal.span {x})).spanRank + 1 ≤ (m R).spanRank := by
  obtain ⟨s, hs1, hs2, hxs⟩ := exists_minimal_generators_containing hx1 hx2
  let s' : Set R := s \ {x}
  have scup : s = s' ∪ {x} := by simp [s', hxs]
  have ss' : Cardinal.mk s = Cardinal.mk s' + 1 := by
    rw [scup, ← Cardinal.mk_singleton x]
    exact Cardinal.mk_union_of_disjoint Set.disjoint_sdiff_left
  have mapeq : Ideal.map (Ideal.Quotient.mk (Ideal.span {x})) (Ideal.span s) =
      Ideal.map (Ideal.Quotient.mk (Ideal.span {x})) (Ideal.span s') := by
    apply (Ideal.map_eq_iff_sup_ker_eq_of_surjective (Ideal.Quotient.mk (Ideal.span {x}))
      Ideal.Quotient.mk_surjective).mpr
    rw [Ideal.mk_ker, ← Ideal.span_union, ← Ideal.span_union, scup]
    simp
  have mapsp := Ideal.map_span (Ideal.Quotient.mk (Ideal.span {x})) s'
  rw [hs1, IsLocalRing.map_maximalIdeal_of_surjective _ Ideal.Quotient.mk_surjective, mapsp]
    at mapeq
  let s'' : Set (R ⧸ Ideal.span {x}) := Ideal.Quotient.mk (Ideal.span {x}) '' s'
  have cds'' : Cardinal.mk s'' ≤ Cardinal.mk s' := Cardinal.mk_image_le
  have a := Submodule.spanRank_span_le_card (R := R ⧸ Ideal.span {x}) s''
  rw [show Submodule.span (R ⧸ Ideal.span {x}) s'' = Ideal.span s'' from rfl, ← mapeq] at a
  have hadd := add_le_add_right (a.trans cds'') 1
  rw [add_comm 1 (m (R ⧸ Ideal.span {x})).spanRank,
    add_comm 1 (Cardinal.mk s')] at hadd
  exact hadd.trans_eq (by rw [← ss', hs2])

private theorem spanFinrank_quot_singleton_add_one
    {R : Type u} {x : R} [CommRing R] [IsLocalRing R] [IsNoetherianRing R]
    [Nontrivial (R ⧸ Ideal.span {x})]
    [IsLocalRing (R ⧸ Ideal.span {x})]
    (hx1 : x ∈ m R) (hx2 : x ∉ (m R) ^ 2) :
    (m (R ⧸ Ideal.span {x})).spanFinrank + 1 = (m R).spanFinrank := by
  have eqrank : (m R).spanRank = (m (R ⧸ Ideal.span {x})).spanRank + 1 :=
    le_antisymm spanRank_quot_singleton_le (spanRank_quot_singleton_ge hx1 hx2)
  rw [Submodule.FG.spanRank_eq_spanFinrank (m R).fg_of_isNoetherianRing,
    Submodule.FG.spanRank_eq_spanFinrank (m (R ⧸ Ideal.span {x})).fg_of_isNoetherianRing] at eqrank
  exact_mod_cast eqrank.symm

private theorem span_singleton_prime_not_minimal_implies_domain
    {R : Type u} [CommRing R] [IsLocalRing R] [IsNoetherianRing R]
    (x : R) [(Ideal.span {x}).IsPrime]
    (notMin : Ideal.span {x} ∉ minimalPrimes R) :
    IsDomain R := by
  obtain ⟨q, hq1, hq2⟩ := Ideal.exists_minimalPrimes_le (bot_le : ⊥ ≤ Ideal.span {x})
  have x_not_in_q : x ∉ q := by
    intro hx
    have hxq : Ideal.span {x} ≤ q := (Ideal.span_singleton_le_iff_mem q).mpr hx
    have : q = Ideal.span {x} := le_antisymm hq2 hxq
    exact notMin (this ▸ hq1)
  have q_in_x_pow : ∀ n : Nat, q ≤ Ideal.span {x} ^ n := by
    intro n
    induction n with
    | zero => simp
    | succ n ih =>
      intro y hy
      rw [Ideal.span_singleton_pow] at ih ⊢
      obtain ⟨r, hr⟩ := Ideal.mem_span_singleton'.mp (ih hy)
      have qPrime : q.IsPrime := Ideal.minimalPrimes_isPrime hq1
      have xpow_not_q : x ^ n ∉ q := by
        intro hxp
        exact x_not_in_q (Ideal.IsPrime.mem_of_pow_mem qPrime n hxp)
      rw [← hr] at hy
      have hrq : r ∈ q := (qPrime.mem_or_mem hy).resolve_right xpow_not_q
      obtain ⟨a, ha⟩ := Ideal.mem_span_singleton'.mp (hq2 hrq)
      apply Ideal.mem_span_singleton'.mpr
      refine ⟨a, ?_⟩
      rw [← ha] at hr
      rw [← hr]
      ring
  have hIntersection := Ideal.iInf_pow_eq_bot_of_isLocalRing (Ideal.span {x})
    (Ideal.IsPrime.ne_top (inferInstance : (Ideal.span {x}).IsPrime))
  have qZero : q ≤ ⊥ := by
    intro y hy
    rw [← hIntersection]
    exact Ideal.mem_iInf.mpr (fun n => q_in_x_pow n hy)
  have qeqZero : q = ⊥ := le_antisymm qZero bot_le
  have qPrime : q.IsPrime := Ideal.minimalPrimes_isPrime hq1
  rw [qeqZero] at qPrime
  exact IsDomain.of_bot_isPrime R

private theorem ringKrullDim_zero_isField
    (R : Type u) [CommRing R] [IsRegularLocalRing R]
    (kd0 : ringKrullDim R = 0) : IsField R := by
  have hm : (m R).spanFinrank = 0 := by
    have h := IsRegularLocalRing.spanFinrank_maximalIdeal (R := R)
    rw [kd0] at h
    exact_mod_cast h
  have mBot : m R = ⊥ :=
    (Submodule.spanFinrank_eq_zero_iff_eq_bot (m R).fg_of_isNoetherianRing).mp hm
  exact IsLocalRing.isField_iff_maximalIdeal_eq.mpr mBot

private theorem quotient_regular
    {R : Type u} [CommRing R] [IsRegularLocalRing R]
    (x : R) [Nontrivial (R ⧸ Ideal.span {x})]
    (hx1 : x ∈ m R) (hx2 : x ∉ (m R) ^ 2) :
    IsRegularLocalRing (R ⧸ Ideal.span {x}) := by
  letI : IsLocalRing (R ⧸ Ideal.span {x}) :=
    IsLocalRing.of_surjective' (Ideal.Quotient.mk (Ideal.span {x})) Ideal.Quotient.mk_surjective
  apply IsRegularLocalRing.of_spanFinrank_maximalIdeal_le
  have hdim := ringKrullDim_le_ringKrullDim_quotient_add_encard ({x} : Set R) (by
    simpa [IsLocalRing.ringJacobson_eq_maximalIdeal] using hx1)
  have hspan := spanFinrank_quot_singleton_add_one hx1 hx2
  rw [Set.encard_singleton, ← IsRegularLocalRing.spanFinrank_maximalIdeal (R := R), ← hspan]
    at hdim
  have hdim' : (↑(m (R ⧸ Ideal.span {x})).spanFinrank : WithBot ℕ∞) + 1 ≤
      ringKrullDim (R ⧸ Ideal.span {x}) + 1 := by simpa using hdim
  exact ENat.WithBot.add_le_add_one_right_iff.mp hdim'

private theorem regularLocalRing_isDomain_induction :
    ∀ (n : Nat) (R : Type u) [CommRing R] [IsRegularLocalRing R],
      (m R).spanFinrank = n → IsDomain R := by
  intro n
  induction n with
  | zero =>
    intro R _ _ hm
    have kd0 : ringKrullDim R = 0 := by
      rw [← IsRegularLocalRing.spanFinrank_maximalIdeal (R := R)]
      exact_mod_cast hm
    letI : Field R := (ringKrullDim_zero_isField R kd0).toField
    infer_instance
  | succ n ih =>
    intro R _ hR hn
    by_contra hR_not_Dom
    have isMinPrime : ∀ x : R, x ∈ m R → x ∉ (m R) ^ 2 →
        Ideal.span {x} ∈ minimalPrimes R := by
      intro x hx hx2
      have xPrime : (Ideal.span {x}).IsPrime := by
        apply (Ideal.Quotient.isDomain_iff_prime (Ideal.span {x})).mp
        haveI : Nontrivial (R ⧸ Ideal.span {x}) :=
          Ideal.Quotient.nontrivial_iff.mpr (Ideal.span_singleton_ne_top (by
            simpa [IsLocalRing.mem_maximalIdeal, mem_nonunits_iff] using hx))
        letI : IsLocalRing (R ⧸ Ideal.span {x}) :=
          IsLocalRing.of_surjective' (Ideal.Quotient.mk (Ideal.span {x}))
            Ideal.Quotient.mk_surjective
        have minGenquot : (m (R ⧸ Ideal.span {x})).spanFinrank = n := by
          have hdrop := spanFinrank_quot_singleton_add_one hx hx2
          omega
        letI : IsRegularLocalRing (R ⧸ Ideal.span {x}) := quotient_regular x hx hx2
        exact ih (R ⧸ Ideal.span {x}) minGenquot
      letI : (Ideal.span {x}).IsPrime := xPrime
      by_contra hx3
      exact hR_not_Dom (span_singleton_prime_not_minimal_implies_domain x hx3)
    clear ih
    let S' := minimalPrimes R ∪ {(m R) ^ 2}
    have sFin : S'.Finite := Set.Finite.union
      (minimalPrimes.finite_of_isNoetherianRing R) (Set.finite_singleton ((m R) ^ 2))
    let S := Set.Finite.toFinset sFin
    have hp : ∀ i ∈ S, i ≠ (m R) ^ 2 → i ≠ (m R) ^ 2 → i.IsPrime := by
      intro I hI hm1 _
      have : I ∈ S' := (Set.Finite.mem_toFinset sFin).mp hI
      rcases this with h1 | h2
      · exact Ideal.minimalPrimes_isPrime h1
      · exact (hm1 h2).elim
    have maxinmin : ∃ i ∈ S, m R ≤ i := by
      apply (@Ideal.subset_union_prime (Ideal R) R _ S (fun x => x) ((m R) ^ 2)
        ((m R) ^ 2) hp (m R)).mp
      intro x hx
      by_cases xinm2 : x ∈ (m R) ^ 2
      · refine Set.mem_iUnion₂.mpr ⟨(m R) ^ 2, ?_, xinm2⟩
        exact (Set.Finite.mem_toFinset sFin).mpr (Set.mem_union_right (minimalPrimes R) rfl)
      · refine Set.mem_iUnion₂.mpr ⟨Ideal.span {x}, ?_, Ideal.mem_span_singleton_self x⟩
        exact (Set.Finite.mem_toFinset sFin).mpr
          (Set.mem_union_left {(m R) ^ 2} (isMinPrime x hx xinm2))
    obtain ⟨P, hP1, hP2⟩ := maxinmin
    have dimNotZero : ringKrullDim R ≠ 0 := by
      rw [← IsRegularLocalRing.spanFinrank_maximalIdeal (R := R)]
      intro hzero
      have : (m R).spanFinrank = 0 := by exact_mod_cast hzero
      omega
    apply dimNotZero
    clear hn hR_not_Dom isMinPrime dimNotZero hp
    rcases (Set.Finite.mem_toFinset sFin).mp hP1 with h1 | h2
    · clear hP1 S sFin S'
      rw [← ringKrullDimZero_iff_ringKrullDim_eq_zero]
      refine Ring.KrullDimLE.mk₀ ?_
      intro I hI
      have hIm : I ≤ m R := IsLocalRing.le_maximalIdeal (Ideal.IsPrime.ne_top hI)
      have hIP : I ≤ P := hIm.trans hP2
      have h1' : Minimal Ideal.IsPrime P := by
        rw [minimalPrimes_eq_minimals] at h1
        exact h1
      have IP := h1'.le_of_le hI hIP
      have hmPrime : (m R).IsPrime := (maximalIdeal.isMaximal R).isPrime
      have mP := h1'.le_of_le hmPrime hP2
      have PI : P = I := le_antisymm IP hIP
      have Pm : P = m R := le_antisymm mP hP2
      have Im : I = m R := PI.symm.trans Pm
      rw [Im]
      exact IsLocalRing.maximalIdeal.isMaximal R
    · have hm : m R ≤ (m R) ^ 2 := h2 ▸ hP2
      have mFG := (isNoetherianRing_iff_ideal_fg R).mp inferInstance (m R)
      have mlem2 : m R ≤ (m R) • (m R) := by
        rw [show (m R) • (m R) = (m R) * (m R) from rfl, ← pow_two]
        exact hm
      have mlejac : m R ≤ Ideal.jacobson ⊥ := by
        rw [IsLocalRing.jacobson_eq_maximalIdeal ⊥ bot_ne_top]
      have mbot := Submodule.eq_bot_of_le_smul_of_le_jacobson_bot
        (m R) (m R) mFG mlem2 mlejac
      exact ringKrullDim_eq_zero_of_isField
        (IsLocalRing.isField_iff_maximalIdeal_eq.mpr mbot)

/-- Every regular local ring is a domain, implementing the frozen `M0032-N-DOMAIN` interface. -/
theorem regularLocalRing_isDomain
    {R : Type u} [CommRing R] [IsRegularLocalRing R] : IsDomain R :=
  regularLocalRing_isDomain_induction (m R).spanFinrank R rfl

/-- The exact package consumed by the frozen conditional root composition. -/
theorem regularLocalDomainPackage :
    Stage1Instances.THM_M_0032.ObligationTree.RegularLocalDomainPackage.{u} := by
  intro R _ _
  exact regularLocalRing_isDomain

#print axioms regularLocalRing_isDomain
#print axioms regularLocalDomainPackage

assert_no_sorry regularLocalRing_isDomain
assert_no_sorry regularLocalDomainPackage

end Stage1Instances.THM_M_0032.DomainProof
