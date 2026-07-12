import Statement

/-!
# THM-M-1003: obligation-tree interfaces

This module kernel-checks only the exact composition boundary frozen by the
obligation registry.  Its hypotheses are open proof obligations, not results.
-/

noncomputable section

open Filter MeasureTheory
open scoped ENNReal MeasureTheory NNReal Topology

universe u

namespace Stage1Instances.THM_M_1003

/-- The common-limit facts supplied by the martingale convergence anchors. -/
def LimitCandidatePackage {Omega : Type u} [MeasurableSpace Omega]
    (D : LpBoundedMartingale Omega) (limit : Omega -> Real) : Prop :=
  MemLp limit D.exponent D.measure /\
    (∀ᵐ omega ∂D.measure,
      Tendsto (fun n : Nat => D.process n omega) atTop (nhds (limit omega)))

/-- The same-exponent norm convergence that remains the central open bridge. -/
def SameExponentNormPackage {Omega : Type u} [MeasurableSpace Omega]
    (D : LpBoundedMartingale Omega) (limit : Omega -> Real) : Prop :=
  Tendsto
    (fun n : Nat =>
      eLpNorm (fun omega => D.process n omega - limit omega)
        D.exponent D.measure)
    atTop (nhds 0)

/-- Checked child-to-parent composition.  Both semantic child packages are
consumed, and the result is definitionally the complete frozen root. -/
theorem root_of_limit_packages
    (candidate : forall (Omega : Type u) [MeasurableSpace Omega]
      (D : LpBoundedMartingale Omega),
        Exists fun limit : Omega -> Real => LimitCandidatePackage D limit)
    (sameExponent : forall (Omega : Type u) [MeasurableSpace Omega]
      (D : LpBoundedMartingale Omega) (limit : Omega -> Real),
        LimitCandidatePackage D limit -> SameExponentNormPackage D limit) :
    LpMartingaleConvergenceTarget.{u} := by
  intro Omega _ D
  obtain ⟨limit, hMemLp, hAE⟩ := candidate Omega D
  exact ⟨limit, hMemLp, hAE, sameExponent Omega D limit ⟨hMemLp, hAE⟩⟩

#print axioms root_of_limit_packages

end Stage1Instances.THM_M_1003
