import Mathlib.Order.Zorn
import «ObligationTree»

namespace Stage1Instances.THM_M_0696

universe u

theorem derives_mono {Atom : Type u} {Gamma Delta : Set (Formula Atom)} {phi : Formula Atom}
    (hsub : Gamma ⊆ Delta) (h : Derives Gamma phi) : Derives Delta phi := by
  induction h with
  | assumption hmem => exact .assumption (hsub hmem)
  | axiomK phi psi => exact .axiomK phi psi
  | axiomS phi psi chi => exact .axiomS phi psi chi
  | axiomDNE phi => exact .axiomDNE phi
  | modusPonens himp hphi ihimp ihphi => exact .modusPonens ihimp ihphi

theorem derives_id {Atom : Type u} (Gamma : Set (Formula Atom)) (phi : Formula Atom) :
    Derives Gamma (.imp phi phi) := by
  exact .modusPonens (.modusPonens (.axiomS phi (.imp phi phi) phi) (.axiomK phi (.imp phi phi)))
    (.axiomK phi phi)

theorem deduction_theorem : DeductionTheoremTarget.{u} := by
  intro Atom Gamma phi psi
  constructor
  · intro h
    induction h with
    | assumption hmem =>
        rcases hmem with (rfl | hmem)
        · exact derives_id Gamma _
        · exact .modusPonens (.axiomK _ _) (.assumption hmem)
    | axiomK a b => exact .modusPonens (.axiomK _ _) (.axiomK a b)
    | axiomS a b c => exact .modusPonens (.axiomK _ _) (.axiomS a b c)
    | axiomDNE a => exact .modusPonens (.axiomK _ _) (.axiomDNE a)
    | modusPonens hab ha ihab iha => exact .modusPonens (.modusPonens (.axiomS phi _ _) ihab) iha
  · intro h
    exact .modusPonens (derives_mono (Set.subset_insert phi Gamma) h) (.assumption (Set.mem_insert _ _))

theorem derives_explosion {Atom : Type u} (Gamma : Set (Formula Atom)) (phi : Formula Atom)
    (hFalse : Derives Gamma .falsum) : Derives Gamma phi := by
  have hNN : Derives Gamma (.imp (.imp phi .falsum) .falsum) :=
    .modusPonens (.axiomK .falsum (.imp phi .falsum)) hFalse
  exact .modusPonens (.axiomDNE phi) hNN

theorem seed_consistency : SeedConsistencyTarget.{u} := by
  intro Atom Gamma phi hn hbad
  have hNN : Derives Gamma (.imp (Neg phi) .falsum) := (deduction_theorem Atom Gamma (Neg phi) .falsum).mp hbad
  exact hn (.modusPonens (.axiomDNE phi) hNN)

theorem derives_cut {Atom : Type u} {Gamma : Set (Formula Atom)} {cut phi : Formula Atom}
    (hcut : Derives Gamma cut) (h : Derives (Set.insert cut Gamma) phi) : Derives Gamma phi := by
  exact .modusPonens ((deduction_theorem Atom Gamma cut phi).mp h) hcut

theorem chain_captures_derivation {Atom : Type u} {C : Set (Set (Formula Atom))}
    (hne : C.Nonempty) (hchain : IsChain (· ⊆ ·) C) {phi : Formula Atom}
    (h : Derives (Set.sUnion C) phi) : ∃ Gamma ∈ C, Derives Gamma phi := by
  induction h with
  | assumption hmem =>
      rcases Set.mem_sUnion.mp hmem with ⟨Gamma, hGC, hp⟩
      exact ⟨Gamma, hGC, .assumption hp⟩
  | axiomK a b =>
      rcases hne with ⟨Gamma, hGC⟩
      exact ⟨Gamma, hGC, .axiomK a b⟩
  | axiomS a b c =>
      rcases hne with ⟨Gamma, hGC⟩
      exact ⟨Gamma, hGC, .axiomS a b c⟩
  | axiomDNE a =>
      rcases hne with ⟨Gamma, hGC⟩
      exact ⟨Gamma, hGC, .axiomDNE a⟩
  | modusPonens hab ha ihab iha =>
      rcases ihab with ⟨G, hGC, hG⟩
      rcases iha with ⟨D, hDC, hD⟩
      by_cases hEq : G = D
      · subst D
        exact ⟨G, hGC, .modusPonens hG hD⟩
      rcases hchain hGC hDC hEq with hGD | hDG
      · exact ⟨D, hDC, .modusPonens (derives_mono hGD hG) hD⟩
      · exact ⟨G, hGC, .modusPonens hG (derives_mono hDG hD)⟩

theorem lindenbaum : LindenbaumTarget.{u} := by
  intro Atom Gamma hcons
  let S : Set (Set (Formula Atom)) := {Delta | Gamma ⊆ Delta ∧ Consistent Delta}
  have hGammaS : Gamma ∈ S := ⟨Set.Subset.rfl, hcons⟩
  obtain ⟨Delta, hGammaDelta, hMax⟩ := zorn_subset_nonempty S (fun C hCS hchain hne => by
    refine ⟨Set.sUnion C, ?_, fun D hDC => Set.subset_sUnion_of_mem hDC⟩
    constructor
    · intro p hp
      rcases hne with ⟨D, hDC⟩
      exact Set.mem_sUnion_of_mem ((hCS hDC).1 hp) hDC
    · intro hbad
      rcases chain_captures_derivation hne hchain hbad with ⟨D, hDC, hD⟩
      exact (hCS hDC).2 hD) Gamma hGammaS
  rcases hMax.1 with ⟨_, hDeltaCons⟩
  refine ⟨Delta, hGammaDelta, hDeltaCons, ?_, ?_⟩
  · intro phi hDer
    by_contra hnot
    have hinsCons : Consistent (Set.insert phi Delta) := by
      intro hbad
      exact hDeltaCons (derives_cut hDer hbad)
    have hinsS : Set.insert phi Delta ∈ S := ⟨Set.Subset.trans hGammaDelta (Set.subset_insert phi Delta), hinsCons⟩
    have := hMax.2 hinsS (Set.subset_insert phi Delta)
    exact hnot (this (Set.mem_insert phi Delta))
  · intro phi
    by_cases hp : phi ∈ Delta
    · exact Or.inl hp
    · right
      by_contra hnp
      have hc1 : ¬ Consistent (Set.insert phi Delta) := by
        intro hc
        have hs : Set.insert phi Delta ∈ S := ⟨Set.Subset.trans hGammaDelta (Set.subset_insert phi Delta), hc⟩
        exact hp ((hMax.2 hs (Set.subset_insert phi Delta)) (Set.mem_insert phi Delta))
      have hc2 : ¬ Consistent (Set.insert (Neg phi) Delta) := by
        intro hc
        have hs : Set.insert (Neg phi) Delta ∈ S := ⟨Set.Subset.trans hGammaDelta (Set.subset_insert (Neg phi) Delta), hc⟩
        exact hnp ((hMax.2 hs (Set.subset_insert (Neg phi) Delta)) (Set.mem_insert (Neg phi) Delta))
      have hn : Derives Delta (Neg phi) :=
        (deduction_theorem Atom Delta phi .falsum).mp (Classical.not_not.mp hc1)
      have hnn : Derives Delta (.imp (Neg phi) .falsum) :=
        (deduction_theorem Atom Delta (Neg phi) .falsum).mp (Classical.not_not.mp hc2)
      exact hDeltaCons (.modusPonens hnn hn)

theorem maximal_imp_iff {Atom : Type u} {Delta : Set (Formula Atom)}
    (hmax : MaximalConsistent Delta) (phi psi : Formula Atom) :
    Formula.imp phi psi ∈ Delta ↔ phi ∉ Delta ∨ psi ∈ Delta := by
  constructor
  · intro himp
    by_cases hp : phi ∈ Delta
    · exact Or.inr (hmax.2.1 (.modusPonens (.assumption himp) (.assumption hp)))
    · exact Or.inl hp
  · rintro (hnp | hpsi)
    · have hnmem : Neg phi ∈ Delta := (hmax.2.2 phi).resolve_left hnp
      have hlocal : Derives (Set.insert phi Delta) psi := by
        have hn : Derives (Set.insert phi Delta) (Neg phi) := .assumption (Set.mem_insert_of_mem phi hnmem)
        have hp : Derives (Set.insert phi Delta) phi := .assumption (Set.mem_insert phi Delta)
        exact derives_explosion _ _ (.modusPonens hn hp)
      exact hmax.2.1 ((deduction_theorem Atom Delta phi psi).mp hlocal)
    · exact hmax.2.1 (.modusPonens (.axiomK psi phi) (.assumption hpsi))

theorem truth_lemma : TruthLemmaTarget.{u} := by
  intro Atom Delta hmax phi
  induction phi with
  | atom a =>
      simp only [Formula.eval, canonicalValuation]
      by_cases h : Derives Delta (.atom a)
      · simp [h, hmax.2.1 h]
      · simp [h]
        exact fun hm => h (.assumption hm)
  | falsum =>
      simp only [Formula.eval, Bool.false_eq_true, false_iff]
      exact fun hmem => hmax.1 (.assumption hmem)
  | imp phi psi ihphi ihpsi =>
      rw [maximal_imp_iff hmax, ← ihphi, ← ihpsi]
      simp [Formula.eval]

theorem countermodel : CountermodelTarget.{u} := by
  intro Atom Gamma phi hn
  have hseed := seed_consistency Atom Gamma phi hn
  obtain ⟨Delta, hsub, hmax⟩ := lindenbaum Atom (Set.insert (Neg phi) Gamma) hseed
  refine ⟨canonicalValuation Delta, ?_, ?_⟩
  · intro psi hpsi
    exact (truth_lemma Atom Delta hmax psi).2 (hsub (Set.mem_insert_of_mem (Neg phi) hpsi))
  · have hnmem : Neg phi ∈ Delta := hsub (Set.mem_insert (Neg phi) Gamma)
    have hntrue := (truth_lemma Atom Delta hmax (Neg phi)).2 hnmem
    simp [Neg, Formula.eval] at hntrue ⊢
    exact hntrue

theorem propositional_completeness : PropositionalCompletenessTarget.{u} :=
  completeness_of_countermodel countermodel

#print axioms deduction_theorem
#print axioms lindenbaum
#print axioms truth_lemma
#print axioms countermodel
#print axioms propositional_completeness

end Stage1Instances.THM_M_0696
