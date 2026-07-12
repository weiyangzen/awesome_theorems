import ObligationTree

/-!
# THM-M-0312 proof integration

This module closes the frozen machine-proof route with the proof bodies from the pinned mathlib
revision.  The two interface lemmas expose the same decomposition as the upstream
`banach_steinhaus` body; `uniformBoundedness` is the repo-local exact-target wrapper.
-/

namespace Stage1Instances.THM_M_0312

universe uE uF uK uK2 uI

variable {E : Type uE} {F : Type uF} {K : Type uK} {K2 : Type uK2}
  [SeminormedAddCommGroup E] [SeminormedAddCommGroup F]
  [NontriviallyNormedField K] [NontriviallyNormedField K2]
  [NormedSpace K E] [NormedSpace K2 F]
  {sigma12 : K →+* K2} [RingHomIsometric sigma12]
  {I : Type uI} [CompleteSpace E]

/-- The barrelled-space package turns pointwise bounds into uniform equicontinuity. -/
theorem pointwiseBounded_to_uniformEquicontinuous {g : I → E →SL[sigma12] F}
    (h : PointwiseBounded g) : UniformEquicontinuous ((↑) ∘ g) := by
  refine (norm_withSeminorms K2 F).banach_steinhaus (fun _ x ↦ ?_)
  simpa [bddAbove_def, Set.forall_mem_range] using h x

/-- The normed-space TFAE package converts uniform equicontinuity to one operator-norm bound. -/
theorem uniformEquicontinuous_to_uniformlyBounded {g : I → E →SL[sigma12] F}
    (h : UniformEquicontinuous ((↑) ∘ g)) : UniformlyBounded g := by
  exact (NormedSpace.equicontinuous_TFAE g).out 5 2 |>.mpr h

/-- Repo-local exact-target closure, composed through the frozen obligation interfaces. -/
theorem uniformBoundedness {g : I → E →SL[sigma12] F} : UniformBoundednessTarget g :=
  root_of_equicontinuity_packages pointwiseBounded_to_uniformEquicontinuous
    uniformEquicontinuous_to_uniformlyBounded

/-- Independent exact-type wrapper around the pinned public root declaration. -/
theorem uniformBoundedness_pinned {g : I → E →SL[sigma12] F} :
    UniformBoundednessTarget g := banach_steinhaus

#print axioms pointwiseBounded_to_uniformEquicontinuous
#print axioms uniformEquicontinuous_to_uniformlyBounded
#print axioms uniformBoundedness
#print axioms uniformBoundedness_pinned

end Stage1Instances.THM_M_0312
