import Mathlib.ModelTheory.DirectLimit
import Mathlib.ModelTheory.ElementaryMaps

open FirstOrder

namespace Stage1.THM_M_0649

open FirstOrder.Language

universe uL uS v w

/-- The elementary-chain theorem in its typed direct-system form.

The `DirectedSystem` instance is the coherence law for the elementary transition maps after
forgetting elementarity.  The conclusion says that the canonical direct-limit embedding of every
stage admits exactly that underlying map as an elementary embedding. -/
def ElementaryChainTarget : Prop :=
  forall (L : Language.{uL, uS}) (ι : Type v) (G : ι → Type w)
    [LinearOrder ι] [Nonempty ι] [∀ i, Nonempty (G i)] [∀ i, L.Structure (G i)]
    (f : ∀ i j, i ≤ j → Language.ElementaryEmbedding L (G i) (G j))
    [DirectedSystem G (fun i j h => (f i j h).toEmbedding)],
    ∀ i,
      ∃ e : Language.ElementaryEmbedding L (G i)
          (L.DirectLimit G (fun a b h => (f a b h).toEmbedding)),
        e.toEmbedding = Language.DirectLimit.of L ι G
          (fun a b h => (f a b h).toEmbedding) i

/-- Fully expanded spelling used to lock the target's binder order and conclusion. -/
def ExpandedTarget : Prop :=
  forall (L : Language.{uL, uS}) (ι : Type v) (G : ι → Type w)
    [LinearOrder ι] [Nonempty ι] [∀ i, Nonempty (G i)] [∀ i, L.Structure (G i)]
    (f : ∀ i j, i ≤ j → Language.ElementaryEmbedding L (G i) (G j))
    [DirectedSystem G (fun i j h => (f i j h).toEmbedding)],
    ∀ i,
      ∃ e : Language.ElementaryEmbedding L (G i)
          (L.DirectLimit G (fun a b h => (f a b h).toEmbedding)),
        e.toEmbedding = Language.DirectLimit.of L ι G
          (fun a b h => (f a b h).toEmbedding) i

theorem target_iff_expandedTarget :
    ElementaryChainTarget.{uL, uS, v, w} ↔ ExpandedTarget.{uL, uS, v, w} := Iff.rfl

-- Structural mutations: these elaborate, but are not the frozen source claim.
def mutationMereEmbeddings : Prop :=
  forall (L : Language.{uL, uS}) (ι : Type v) (G : ι → Type w)
    [LinearOrder ι] [Nonempty ι] [∀ i, Nonempty (G i)] [∀ i, L.Structure (G i)]
    (f : ∀ i j, i ≤ j → G i ↪[L] G j)
    [DirectedSystem G (fun i j h => f i j h)],
    ∀ i, ∃ e : Language.ElementaryEmbedding L (G i)
        (L.DirectLimit G (fun a b h => f a b h)),
      e.toEmbedding = Language.DirectLimit.of L ι G (fun a b h => f a b h) i

def mutationOnlyFirstStage : Prop :=
  forall (L : Language.{uL, uS}) (ι : Type v) (G : ι → Type w)
    [LinearOrder ι] [Nonempty ι] [∀ i, Nonempty (G i)] [∀ i, L.Structure (G i)]
    (f : ∀ i j, i ≤ j → Language.ElementaryEmbedding L (G i) (G j))
    [DirectedSystem G (fun i j h => (f i j h).toEmbedding)] (i : ι),
    ∃ e : Language.ElementaryEmbedding L (G i)
        (L.DirectLimit G (fun a b h => (f a b h).toEmbedding)),
      e.toEmbedding = Language.DirectLimit.of L ι G
        (fun a b h => (f a b h).toEmbedding) i

def mutationAssumedConclusion : Prop :=
  forall (L : Language.{uL, uS}) (ι : Type v) (G : ι → Type w)
    [LinearOrder ι] [Nonempty ι] [∀ i, Nonempty (G i)] [∀ i, L.Structure (G i)]
    (f : ∀ i j, i ≤ j → Language.ElementaryEmbedding L (G i) (G j))
    [DirectedSystem G (fun i j h => (f i j h).toEmbedding)],
    (∀ i, ∃ e : Language.ElementaryEmbedding L (G i)
        (L.DirectLimit G (fun a b h => (f a b h).toEmbedding)),
      e.toEmbedding = Language.DirectLimit.of L ι G
        (fun a b h => (f a b h).toEmbedding) i) → True

end Stage1.THM_M_0649

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1.THM_M_0649.ElementaryChainTarget
