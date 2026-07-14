import ObligationTree

/-!
# THM-M-0317 proof work

This module implements the compactness/separation half of the frozen
Tychonoff fixed-point architecture. The finite-dimensional approximation and
Brouwer half remains open.
-/

universe u

namespace AwesomeTheorems.THM_M_0317

/-- Small displacement in every zero neighbourhood says that zero lies in the
closure of the displacement image. -/
theorem zero_mem_closure_displacement_image {E : Type u} [AddCommGroup E]
    [TopologicalSpace E] [IsTopologicalAddGroup E] (K : Set E) (f : E → E)
    (happrox : HasArbitrarilySmallDisplacement K f) :
    (0 : E) ∈ closure ((fun x => f x - x) '' K) := by
  rw [mem_closure_iff_nhds]
  intro V hV
  obtain ⟨x, hxK, hxV⟩ := happrox V hV
  exact ⟨f x - x, hxV, x, hxK, rfl⟩

/-- The displacement image of a compact set under a continuous map is compact,
and hence closed in the Hausdorff ambient space. -/
theorem isClosed_displacement_image {E : Type u} [AddCommGroup E]
    [TopologicalSpace E] [IsTopologicalAddGroup E] [T2Space E]
    (K : Set E) (f : E → E) (hcompact : IsCompact K) (hf : Continuous f) :
    IsClosed ((fun x => f x - x) '' K) := by
  exact (hcompact.image (hf.sub continuous_id)).isClosed

/-- Compactness and Hausdorff separation turn arbitrarily small displacement
into an exact fixed point. This inhabits the exact frozen limit interface. -/
theorem compactnessLimitPackage : CompactnessLimitPackage.{u} := by
  intro E _ _ _ _ _ _ _ K f _ hcompact _ hf _ happrox
  have hzero : (0 : E) ∈ (fun x => f x - x) '' K :=
    (isClosed_displacement_image K f hcompact hf).closure_eq ▸
      zero_mem_closure_displacement_image K f happrox
  obtain ⟨x, hxK, hxzero⟩ := hzero
  exact ⟨x, hxK, sub_eq_zero.mp hxzero⟩

#print axioms zero_mem_closure_displacement_image
#print axioms isClosed_displacement_image
#print axioms compactnessLimitPackage

end AwesomeTheorems.THM_M_0317
