import Mathlib.Analysis.InnerProductSpace.Dual

/-!
# THM-M-0278 discovery-only intake probe

These checks authenticate the direct Fréchet-Riesz interfaces in pinned mathlib and elaborate one
candidate existence-and-uniqueness consequence. They do not select a source-faithful canonical
target, establish statement identity, or transfer proof credit to THM-M-0278.
-/

open Module

#check StrongDual
#check InnerProductSpace.toDualMap
#check InnerProductSpace.toDual
#check InnerProductSpace.toDual_apply_apply
#check InnerProductSpace.toDual_symm_apply

example (K E : Type*) [RCLike K] [NormedAddCommGroup E]
    [InnerProductSpace K E] [CompleteSpace E] (ell : StrongDual K E) :
    ExistsUnique (fun y : E => forall u : E, ell u = inner K y u) := by
  refine ⟨(InnerProductSpace.toDual K E).symm ell, ?_, ?_⟩
  · intro u
    exact InnerProductSpace.toDual_symm_apply.symm
  · intro y hy
    apply (InnerProductSpace.toDual K E).injective
    apply ContinuousLinearMap.ext
    intro u
    rw [InnerProductSpace.toDual_apply_apply, InnerProductSpace.toDual_apply_apply]
    rw [← hy u]
    exact (InnerProductSpace.toDual_symm_apply (𝕜 := K) (E := E) (x := u) (y := ell)).symm

#print axioms InnerProductSpace.toDual
#print axioms InnerProductSpace.toDual_symm_apply
