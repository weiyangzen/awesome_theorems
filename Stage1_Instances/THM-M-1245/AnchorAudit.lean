import Mathlib.Analysis.FunctionalSpaces.SobolevInequality

/-!
# THM-M-1245 anchor audit

This file checks the terminal candidate in the repository's immutable mathlib
pin.  The `example` is only an applicability probe: the later proof node owns
the named wrapper for the frozen root.
-/

noncomputable section

open MeasureTheory

#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_le

example (n : Nat) (p q : NNReal) (hn : 0 < n) (hp : 1 <= p)
    (hpq : (q : Real)⁻¹ = (p : Real)⁻¹ - (n : Real)⁻¹)
    (u : EuclideanSpace Real (Fin n) -> Real) (hu : ContDiff Real 1 u)
    (hcu : HasCompactSupport u) :
    eLpNorm u q volume <=
      MeasureTheory.eLpNormLESNormFDerivOfEqInnerConst
          (volume : Measure (EuclideanSpace Real (Fin n))) p *
        eLpNorm (fderiv Real u) p volume := by
  have hfin : 0 < Module.finrank Real (EuclideanSpace Real (Fin n)) := by
    simpa using hn
  have hconj :
      (q : Real)⁻¹ = (p : Real)⁻¹ -
        (Module.finrank Real (EuclideanSpace Real (Fin n)) : Real)⁻¹ := by
    simpa using hpq
  simpa using
    MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner volume hu hcu hp hfin hconj

#print axioms MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner
#print axioms MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq
