import Mathlib.Analysis.Convex.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
# THM-M-0319: anchor type and transport audit

This file records the exact type exposed by the immutable external Lean 4
candidate and checks the adapter from that subtype-map formulation to the
canonical ambient-map target. It does not import or assume the external proof.
-/

namespace Stage1Instances.THM_M_0319.AnchorAudit

/-- Exact terminal type of `harfe/fixed-point-theorems-lean4` declaration
`brouwer_fixed_point` at commit `11a9f041246d28374edae384241757f9a0cbd5e4`.
The name is local so this source audit cannot accidentally claim the body. -/
def HarfeBrouwerType : Prop :=
  forall {V : Type*} [NormedAddCommGroup V] [NormedSpace Real V]
    [FiniteDimensional Real V] (s : Set V),
    Convex Real s -> IsCompact s -> s.Nonempty ->
      forall f : C(s, s), exists x, f x = x

/-- The canonical ambient-map target, repeated here so this audit is a
self-contained elaboration probe rather than an import of a future proof. -/
def CanonicalTarget : Prop :=
  forall (n : Nat) (K : Set (EuclideanSpace Real (Fin n)))
    (f : EuclideanSpace Real (Fin n) -> EuclideanSpace Real (Fin n)),
    K.Nonempty -> IsCompact K -> Convex Real K -> ContinuousOn f K ->
      Set.MapsTo f K K -> exists x, x ∈ K ∧ f x = x

/-- If the external candidate is later pinned and imported, its subtype-map
theorem closes the exact canonical target through this checked adapter. -/
theorem harfe_type_implies_canonical (h : HarfeBrouwerType.{0}) : CanonicalTarget := by
  intro n K f hne hcompact hconvex hcontinuous hmaps
  let g : C(K, K) :=
    { toFun := fun x => ⟨f x, hmaps x.property⟩
      continuous_toFun :=
        (continuousOn_iff_continuous_restrict.mp hcontinuous).subtype_mk _ }
  obtain ⟨x, hx⟩ := h K hconvex hcompact hne g
  exact ⟨x, x.property, congrArg Subtype.val hx⟩

end Stage1Instances.THM_M_0319.AnchorAudit

set_option pp.explicit true in
#print Stage1Instances.THM_M_0319.AnchorAudit.HarfeBrouwerType

#print axioms Stage1Instances.THM_M_0319.AnchorAudit.harfe_type_implies_canonical
