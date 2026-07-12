import Statement

/-!
# THM-M-0329 conditional obligation composition

This file checks the child-to-root interface frozen by the obligation registry.
The two packages are explicit premises; this module does not claim that either
package has been accepted as proof evidence.
-/

noncomputable section

namespace Stage1Instances.THM_M_0329.ObligationTree

open InnerProductSpace

universe u

/-- Riesz representation, isolated as a root-critical datum bridge. -/
def RieszPackage : Prop :=
  forall (V : Type u) [NormedAddCommGroup V] [InnerProductSpace Real V]
    [CompleteSpace V] (F : V →L[Real] Real),
      exists f : V, forall v : V, @inner Real V _ f v = F v

/-- The Lax-Milgram operator package, before translating an arbitrary datum. -/
def OperatorPackage : Prop :=
  forall (V : Type u) [NormedAddCommGroup V] [InnerProductSpace Real V]
    [CompleteSpace V] (B : V →L[Real] V →L[Real] Real),
      IsCoercive B ->
        exists e : V ≃L[Real] V,
          forall u v : V, @inner Real V _ (e u) v = B u v

/-- Checked composition of the two independently tracked bridge packages into
the exact frozen target. -/
theorem root_of_packages (riesz : RieszPackage.{u})
    (operator : OperatorPackage.{u}) :
    Stage1Instances.THM_M_0329.LaxMilgramTarget.{u} := by
  intro V _ _ _ B hB F
  obtain ⟨f, hf⟩ := riesz V F
  obtain ⟨e, he⟩ := operator V B hB
  refine ⟨e.symm f, ?_, ?_⟩
  · intro v
    rw [← hf v, ← he]
    simp
  · intro y hy
    apply e.injective
    apply ext_inner_right Real
    intro v
    rw [he, hy v, ← hf v]
    simp

end Stage1Instances.THM_M_0329.ObligationTree

#print axioms Stage1Instances.THM_M_0329.ObligationTree.root_of_packages
