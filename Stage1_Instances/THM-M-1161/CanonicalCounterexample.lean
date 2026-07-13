import FredholmIntegralEquationStatement
import Proof

/-!
# THM-M-1161 canonical counterexample adapter

This module checks that the countermodel constructed in `Proof.lean` refutes
the exact canonical declaration rather than only its local restatement.
-/

namespace AwesomeTheorems.Stage1.THM_M_1161

open scoped ComplexConjugate InnerProductSpace
open MeasureTheory

/-- Field-for-field transport from the proof artifact's exact local model
restatement to the canonical statement model. -/
def localToCanonicalModel
    {X E : Type*} [TopologicalSpace X] [CompactSpace X] [MeasurableSpace X]
    (mu : Measure X) [IsFiniteMeasure mu]
    [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
    (M : Proof.Model (E := E) mu) : FredholmKernelModel (E := E) mu where
  kernel := M.kernel
  realize := M.realize
  compact_domain := M.compact_domain
  continuous_kernel := M.continuous_kernel
  realize_injective := M.realize_injective
  operator := M.operator
  compact_operator := M.compact_operator
  integrable_kernel := M.integrable_kernel
  operator_eq_integral := M.operator_eq_integral

/-- The canonical and local solution predicates are definitionally equal. -/
theorem canonical_solves_iff_local
    {X E : Type*} [TopologicalSpace X] [CompactSpace X] [MeasurableSpace X]
    (mu : Measure X) [IsFiniteMeasure mu]
    [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
    (M : Proof.Model (E := E) mu) (lambda : ℂ) (phi f : E) :
    Solves mu (localToCanonicalModel mu M) lambda phi f ↔
      Proof.Solves mu M lambda phi f := by
  rfl

/-- The full canonical target and local root restatement are definitionally
equal for every transported model. -/
theorem canonical_target_iff_local_root
    {X E : Type*} [TopologicalSpace X] [CompactSpace X] [MeasurableSpace X]
    (mu : Measure X) [IsFiniteMeasure mu]
    [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
    (M : Proof.Model (E := E) mu) (lambda : ℂ) :
    FredholmSecondKindAlternative mu (localToCanonicalModel mu M) lambda ↔
      Proof.Root mu M lambda := by
  rfl

/-- Checked negation of the exact canonical statement at the concrete
`PUnit`/`Complex` model from `Proof.lean`. -/
theorem not_canonical_target :
    ¬ FredholmSecondKindAlternative (Measure.dirac PUnit.unit)
      (localToCanonicalModel (Measure.dirac PUnit.unit) Proof.badModel) 1 := by
  exact (canonical_target_iff_local_root
    (Measure.dirac PUnit.unit) Proof.badModel 1).not.mpr Proof.not_root_bad

#check not_canonical_target
#print axioms not_canonical_target

/-- The frozen `N-OPERATOR` normalization is itself refuted by the same
model: at `lambda = 1`, `phi = 0`, and `f = -1`, the pointwise equation holds
but `(I - T) phi = f` does not. -/
theorem not_operator_normalization :
    ¬(∀ (lambda phi f : ℂ),
      Solves (Measure.dirac PUnit.unit)
          (localToCanonicalModel (Measure.dirac PUnit.unit) Proof.badModel)
          lambda phi f ↔
        (ContinuousLinearMap.id ℂ ℂ - lambda • Proof.badModel.operator) phi = f) := by
  intro h
  have hsolves : Solves (Measure.dirac PUnit.unit)
      (localToCanonicalModel (Measure.dirac PUnit.unit) Proof.badModel) 1 0 (-1) :=
    (canonical_solves_iff_local
      (Measure.dirac PUnit.unit) Proof.badModel 1 0 (-1)).2
      ((Proof.solves_bad_one_iff 0 (-1)).2 rfl)
  have hfalse := (h 1 0 (-1)).1 hsolves
  norm_num [Proof.badModel] at hfalse

#print axioms not_operator_normalization

end AwesomeTheorems.Stage1.THM_M_1161
