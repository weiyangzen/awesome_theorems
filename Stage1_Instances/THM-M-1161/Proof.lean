import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.Normed.Operator.FredholmAlternative
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# THM-M-1161 proof-phase countermodel

The frozen model requires `realize` to be injective, but does not require it
to preserve zero, addition, or scalar multiplication.  This file gives an
admission-free countermodel to the exact canonical target.  It is blocker
evidence, not a proof of the advertised Fredholm alternative.
-/

namespace AwesomeTheorems.Stage1.THM_M_1161.Proof

open scoped ComplexConjugate InnerProductSpace
open MeasureTheory

variable {X E : Type*} [TopologicalSpace X] [CompactSpace X] [MeasurableSpace X]
  (mu : Measure X) [IsFiniteMeasure mu]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]

/-- Exact restatement of the frozen model, local to the proof artifact so it
can be checked directly with the canonical minimal imports. -/
structure Model where
  kernel : X → X → ℂ
  realize : E → X → ℂ
  compact_domain : IsCompact (Set.univ : Set X)
  continuous_kernel : Continuous (Function.uncurry kernel)
  realize_injective : Function.Injective realize
  operator : E →L[ℂ] E
  compact_operator : IsCompactOperator operator
  integrable_kernel (u : E) (x : X) :
    Integrable (fun y => kernel x y * realize u y) mu
  operator_eq_integral (u : E) (x : X) :
    realize (operator u) x = ∫ y, kernel x y * realize u y ∂mu

def Solves (M : Model (E := E) mu) (lambda : ℂ) (phi f : E) : Prop :=
  ∀ x : X, M.realize phi x - lambda *
    ∫ y, M.kernel x y * M.realize phi y ∂mu = M.realize f x

/-- Exact restatement of the frozen canonical proposition. -/
def Root (M : Model (E := E) mu) (lambda : ℂ) : Prop :=
  let A : E →L[ℂ] E := ContinuousLinearMap.id ℂ E - lambda • M.operator
  let Astar : E →L[ℂ] E := ContinuousLinearMap.adjoint A
  ((∀ u : E, Solves mu M lambda u 0 → u = 0) ∧
      ∀ f : E, ∃! phi : E, Solves mu M lambda phi f) ∨
    ((∃ u : E, u ≠ 0 ∧ Solves mu M lambda u 0) ∧
      ∀ f : E, (∃ phi : E, Solves mu M lambda phi f) ↔
        ∀ psi : E, Astar psi = 0 → ⟪f, psi⟫_ℂ = 0)

noncomputable def badModel :
    Model (X := PUnit) (E := ℂ) (Measure.dirac PUnit.unit) where
  kernel := fun _ _ => 1
  realize := fun z _ => z + 1
  compact_domain := isCompact_univ
  continuous_kernel := continuous_const
  realize_injective := by
    intro a b h
    have hu := congrFun h PUnit.unit
    exact add_right_cancel hu
  operator := ContinuousLinearMap.id ℂ ℂ
  compact_operator := isCompactOperator_id
  integrable_kernel := by
    intro u x
    simp
  operator_eq_integral := by
    intro u x
    change u + 1 = _
    simp

/-- In the countermodel at `lambda = 1`, the equation is independent of its
purported solution: it is solvable exactly for the datum `-1`. -/
theorem solves_bad_one_iff (phi f : ℂ) :
    Solves (Measure.dirac PUnit.unit) badModel 1 phi f ↔ f = -1 := by
  constructor
  · intro h
    have hx := h PUnit.unit
    simp only [badModel, integral_dirac] at hx
    linear_combination -hx
  · intro h
    subst f
    intro x
    simp [badModel]

/-- The exact frozen target is false for `badModel`: its first branch would
make both `0` and `1` the unique solution for datum `-1`, while its second
branch requires a homogeneous solution even though none exists. -/
theorem not_root_bad :
    ¬ Root (Measure.dirac PUnit.unit) badModel 1 := by
  intro h
  rcases h with hfirst | hsecond
  · obtain ⟨phi, _hphi, hunique⟩ := hfirst.2 (-1)
    have hzero : Solves (Measure.dirac PUnit.unit) badModel 1 0 (-1) :=
      (solves_bad_one_iff 0 (-1)).2 rfl
    have hone : Solves (Measure.dirac PUnit.unit) badModel 1 1 (-1) :=
      (solves_bad_one_iff 1 (-1)).2 rfl
    have hp0 : phi = 0 := (hunique 0 hzero).symm
    have hp1 : phi = 1 := (hunique 1 hone).symm
    exact zero_ne_one (hp0.symm.trans hp1)
  · obtain ⟨u, _hu_ne, hu⟩ := hsecond.1
    have hfalse : (0 : ℂ) = -1 := (solves_bad_one_iff u 0).1 hu
    norm_num at hfalse

#check not_root_bad
#print axioms not_root_bad

end AwesomeTheorems.Stage1.THM_M_1161.Proof
