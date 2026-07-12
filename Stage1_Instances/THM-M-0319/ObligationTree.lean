import Mathlib.Analysis.Convex.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
# THM-M-0319: checked obligation-tree interfaces

This file checks only the already-audited subtype-to-ambient composition and
the zero-dimensional boundary. The external Brouwer proof is an explicit
premise; this module does not claim or recreate that proof body.
-/

namespace Stage1Instances.THM_M_0319.ObligationTree

def ExternalBrouwerBody : Prop :=
  forall {V : Type*} [NormedAddCommGroup V] [NormedSpace Real V]
    [FiniteDimensional Real V] (s : Set V),
    Convex Real s -> IsCompact s -> s.Nonempty ->
      forall f : C(s, s), exists x, f x = x

def CanonicalTarget : Prop :=
  forall (n : Nat) (K : Set (EuclideanSpace Real (Fin n)))
    (f : EuclideanSpace Real (Fin n) -> EuclideanSpace Real (Fin n)),
    K.Nonempty -> IsCompact K -> Convex Real K -> ContinuousOn f K ->
      Set.MapsTo f K K -> exists x, x ∈ K ∧ f x = x

/-- Checked composition edge `M0319-T-SUBTYPE -> M0319-ROOT`. -/
theorem root_of_external_body (h : ExternalBrouwerBody.{0}) : CanonicalTarget := by
  intro n K f hne hcompact hconvex hcontinuous hmaps
  let g : C(K, K) :=
    { toFun := fun x => ⟨f x, hmaps x.property⟩
      continuous_toFun :=
        (continuousOn_iff_continuous_restrict.mp hcontinuous).subtype_mk _ }
  obtain ⟨x, hx⟩ := h K hconvex hcompact hne g
  exact ⟨x, x.property, congrArg Subtype.val hx⟩

/-- The included dimension-zero semantic boundary is independently closed. -/
theorem zero_dimensional_boundary (K : Set (EuclideanSpace Real (Fin 0)))
    (f : EuclideanSpace Real (Fin 0) -> EuclideanSpace Real (Fin 0))
    (hne : K.Nonempty) : exists x, x ∈ K ∧ f x = x := by
  obtain ⟨x, hx⟩ := hne
  refine ⟨x, hx, ?_⟩
  ext i
  exact Fin.elim0 i

end Stage1Instances.THM_M_0319.ObligationTree

#print axioms Stage1Instances.THM_M_0319.ObligationTree.root_of_external_body
#print axioms Stage1Instances.THM_M_0319.ObligationTree.zero_dimensional_boundary
