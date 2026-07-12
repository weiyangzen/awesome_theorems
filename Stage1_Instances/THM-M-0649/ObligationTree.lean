import Statement

/-!
# THM-M-0649 conditional obligation composition

This module gives a checked type to the Tarski-Vaught cut selected by the frozen obligation
architecture.  It deliberately assumes that cut; proving it is downstream work.
-/

open FirstOrder

noncomputable section

namespace Stage1.THM_M_0649

open FirstOrder.Language

universe uL uS v w

/-- The exact Tarski-Vaught witness condition for every canonical map into the direct limit. -/
def CanonicalTarskiVaught : Prop :=
  forall (L : Language.{uL, uS}) (ι : Type v) (G : ι -> Type w)
    [LinearOrder ι] [Nonempty ι] [forall i, Nonempty (G i)] [forall i, L.Structure (G i)]
    (f : forall i j, i <= j -> Language.ElementaryEmbedding L (G i) (G j))
    [DirectedSystem G (fun i j h => (f i j h).toEmbedding)] (i : ι),
    let ofi := Language.DirectLimit.of L ι G
      (fun a b h => (f a b h).toEmbedding) i
    forall (n : Nat) (phi : L.BoundedFormula Empty (n + 1)) (x : Fin n -> G i)
      (a : L.DirectLimit G (fun p q h => (f p q h).toEmbedding)),
      phi.Realize default (Fin.snoc (ofi ∘ x) a) ->
        exists b : G i, phi.Realize default (Fin.snoc (ofi ∘ x) (ofi b))

/-- Checked final composition: the frozen Tarski-Vaught cut supplies the exact root. -/
theorem elementaryChainTarget_of_tarskiVaught
    (htv : CanonicalTarskiVaught.{uL, uS, v, w}) :
    ElementaryChainTarget.{uL, uS, v, w} := by
  intro L ι G _ _ _ _ f _ i
  let ofi := Language.DirectLimit.of L ι G
    (fun a b h => (f a b h).toEmbedding) i
  refine ⟨ofi.toElementaryEmbedding ?_, rfl⟩
  exact htv L ι G f i

#print axioms elementaryChainTarget_of_tarskiVaught

end Stage1.THM_M_0649
