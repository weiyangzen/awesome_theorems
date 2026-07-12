import ObligationTree

/-!
# THM-M-0649 proof

The canonical map from a stage into the direct limit preserves every bounded formula.  In the
universal-quantifier case an arbitrary limit element is represented at some stage, both stages are
moved to a common upper bound, and elementarity of the transition map supplies the required
formula at that upper bound.
-/

open FirstOrder

noncomputable section

namespace Stage1.THM_M_0649

open FirstOrder.Language

universe uL uS v w

theorem canonical_map_boundedFormula
    (L : Language.{uL, uS}) (ι : Type v) (G : ι -> Type w)
    [LinearOrder ι] [Nonempty ι] [forall i, Nonempty (G i)] [forall i, L.Structure (G i)]
    (f : forall i j, i <= j -> Language.ElementaryEmbedding L (G i) (G j))
    [DirectedSystem G (fun i j h => (f i j h).toEmbedding)] :
    forall (i : ι) (n : Nat) (phi : L.BoundedFormula Empty n) (xs : Fin n -> G i),
      phi.Realize default
          (Language.DirectLimit.of L ι G (fun a b h => (f a b h).toEmbedding) i ∘ xs) ↔
        phi.Realize default xs := by
  let g := fun a b h => (f a b h).toEmbedding
  intro i n phi
  induction phi using FirstOrder.Language.BoundedFormula.recOn generalizing i with
  | falsum => exact fun _ => Iff.rfl
  | equal t₁ t₂ =>
      intro xs
      change Term.realize _ t₁ = Term.realize _ t₂ ↔ _
      rw [show Sum.elim default
          (Language.DirectLimit.of L ι G g i ∘ xs) =
          Language.DirectLimit.of L ι G g i ∘ Sum.elim default xs by
        ext z
        cases z with
        | inl z => exact Empty.elim z
        | inr z => rfl]
      simp only [HomClass.realize_term, (Language.DirectLimit.of L ι G g i).injective.eq_iff]
      rfl
  | rel R ts =>
      intro xs
      have hv : Sum.elim (fun z : Empty => Empty.elim z)
          (Language.DirectLimit.of L ι G g i ∘ xs) =
          Language.DirectLimit.of L ι G g i ∘
            Sum.elim (fun z : Empty => Empty.elim z) xs := by
        ext z
        cases z with
        | inl z => exact Empty.elim z
        | inr z => rfl
      simp only [BoundedFormula.Realize]
      have hv' : Sum.elim (default : Empty -> Language.DirectLimit G g)
          (Language.DirectLimit.of L ι G g i ∘ xs) =
          Language.DirectLimit.of L ι G g i ∘ Sum.elim (default : Empty -> G i) xs := by
        ext z
        cases z with
        | inl z => exact Empty.elim z
        | inr z => rfl
      rw [hv']
      simp_rw [HomClass.realize_term]
      exact (Language.DirectLimit.of L ι G g i).map_rel R _
  | imp phi psi ihphi ihpsi =>
      intro xs
      simp only [BoundedFormula.Realize, ihphi i, ihpsi i]
  | all phi ih =>
      intro xs
      simp only [BoundedFormula.realize_all]
      constructor
      · intro h a
        rw [← ih i, Fin.comp_snoc]
        exact h (Language.DirectLimit.of L ι G g i a)
      · intro h a
        obtain ⟨j, b, hab⟩ := Language.DirectLimit.exists_of (L := L) (ι := ι)
          (G := G) (f := g) a
        obtain ⟨k, hik, hjk⟩ := exists_ge_ge i j
        rw [← hab]
        have hs : Fin.snoc (Language.DirectLimit.of L ι G g i ∘ xs)
              (Language.DirectLimit.of L ι G g j b) =
            Language.DirectLimit.of L ι G g k ∘
              Fin.snoc ((f i k hik) ∘ xs) (f j k hjk b) := by
          funext z
          refine Fin.lastCases ?_ (fun z => ?_) z
          · simp only [Fin.snoc_last, Function.comp_apply]
            exact (Language.DirectLimit.of_f (L := L) (ι := ι) (G := G)
              (f := g) (hij := hjk) (x := b)).symm
          · simp only [Fin.snoc_castSucc, Function.comp_apply]
            exact (Language.DirectLimit.of_f (L := L) (ι := ι) (G := G)
              (f := g) (hij := hik) (x := xs z)).symm
        rw [hs, ih k]
        have hall : (phi.all).Realize default ((f i k hik) ∘ xs) :=
          by simpa only [Unique.eq_default ((f i k hik) ∘ default)] using
            ((f i k hik).map_boundedFormula phi.all default xs).2 h
        exact hall (f j k hjk b)

theorem canonicalTarskiVaught : CanonicalTarskiVaught.{uL, uS, v, w} := by
  intro L ι G _ _ _ _ f _ i
  dsimp only
  intro n phi x a ha
  have hex : phi.ex.Realize default
      (Language.DirectLimit.of L ι G (fun p q h => (f p q h).toEmbedding) i ∘ x) :=
    BoundedFormula.realize_ex.2 ⟨a, ha⟩
  have hex' := (canonical_map_boundedFormula L ι G f i n phi.ex x).1 hex
  obtain ⟨b, hb⟩ := BoundedFormula.realize_ex.1 hex'
  refine ⟨b, ?_⟩
  simpa only [Fin.comp_snoc] using
    (canonical_map_boundedFormula L ι G f i (n + 1) phi (Fin.snoc x b)).2 hb

theorem elementaryChainTarget : ElementaryChainTarget.{uL, uS, v, w} :=
  elementaryChainTarget_of_tarskiVaught canonicalTarskiVaught

#print axioms canonical_map_boundedFormula
#print axioms canonicalTarskiVaught
#print axioms elementaryChainTarget

end Stage1.THM_M_0649
