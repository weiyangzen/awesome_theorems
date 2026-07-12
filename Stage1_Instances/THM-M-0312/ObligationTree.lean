import Statement

/-!
# THM-M-0312 conditional obligation composition

The theorem below checks the two interfaces through which the pinned mathlib proof passes.  The
interfaces remain explicit premises here: this phase freezes their composition and does not claim
new proof credit for either package.
-/

namespace Stage1Instances.THM_M_0312

universe uE uF uK uK2 uI

variable {E : Type uE} {F : Type uF} {K : Type uK} {K2 : Type uK2}
  [SeminormedAddCommGroup E] [SeminormedAddCommGroup F]
  [NontriviallyNormedField K] [NontriviallyNormedField K2]
  [NormedSpace K E] [NormedSpace K2 F]
  {sigma12 : K →+* K2} [RingHomIsometric sigma12]
  {I : Type uI} [CompleteSpace E]

def PointwiseBounded (g : I → E →SL[sigma12] F) : Prop :=
  forall x : E, exists C : Real, forall i : I, norm (g i x) <= C

def UniformlyBounded (g : I → E →SL[sigma12] F) : Prop :=
  exists C : Real, forall i : I, norm (g i) <= C

/-- Exact checked parent composition for the equicontinuity route used by `banach_steinhaus`. -/
theorem root_of_equicontinuity_packages {g : I → E →SL[sigma12] F}
    (toEquicontinuous : PointwiseBounded g → UniformEquicontinuous ((↑) ∘ g))
    (fromEquicontinuous : UniformEquicontinuous ((↑) ∘ g) → UniformlyBounded g) :
    UniformBoundednessTarget g := by
  intro h
  exact fromEquicontinuous (toEquicontinuous h)

#print axioms root_of_equicontinuity_packages

end Stage1Instances.THM_M_0312
