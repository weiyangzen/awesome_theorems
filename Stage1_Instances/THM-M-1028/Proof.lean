import ObligationTree

/-!
# THM-M-1028 proof-phase bodies

These proofs close the exact modification and final-event composition boundary
of the frozen statement.  The two mathematical path packages remain explicit
premises: pinned mathlib does not contain the Brownian continuous-modification
or almost-sure nowhere-differentiability theorems needed to discharge them.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Set Filter

namespace AwesomeTheorems.Stage1.THM_M_1028

universe u

/-- Coordinatewise almost-everywhere modification is reflexive. -/
theorem isModification_refl {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) (X : RealProcess Omega) :
    IsModification X X P := by
  intro t
  exact Filter.Eventually.of_forall fun _ => rfl

/-- Coordinatewise almost-everywhere modification is symmetric. -/
theorem isModification_symm {Omega : Type u} [MeasurableSpace Omega]
    {P : Measure Omega} {X Y : RealProcess Omega}
    (h : IsModification X Y P) : IsModification Y X P := by
  intro t
  exact (h t).symm

/-- Coordinatewise almost-everywhere modification is transitive. -/
theorem isModification_trans {Omega : Type u} [MeasurableSpace Omega]
    {P : Measure Omega} {X Y Z : RealProcess Omega}
    (hXY : IsModification X Y P) (hYZ : IsModification Y Z P) :
    IsModification X Z P := by
  intro t
  exact (hXY t).trans (hYZ t)

/-- Merge the two full-measure path events without changing the process. -/
theorem merge_path_events {Omega : Type u} [MeasurableSpace Omega]
    {P : Measure Omega} {Y : RealProcess Omega}
    (hcontinuous :
      ∀ᵐ aeOmega ∂P,
        ContinuousOn (fun t => Y t aeOmega) (Ici (0 : Real)))
    (hnondifferentiable :
      ∀ᵐ aeOmega ∂P,
        NowhereDifferentiableOnNonnegative (fun t => Y t aeOmega)) :
    ∀ᵐ aeOmega ∂P,
      ContinuousOn (fun t => Y t aeOmega) (Ici (0 : Real)) /\
        NowhereDifferentiableOnNonnegative (fun t => Y t aeOmega) := by
  filter_upwards [hcontinuous, hnondifferentiable] with omega hc hn
  exact And.intro hc hn

/--
Exact root composition from the two frozen substantive packages.  No terminal
Brownian path theorem is hidden in this wrapper: both packages are arguments.
-/
theorem statement_of_path_packages
    (continuous : ContinuousModificationPackage.{u})
    (nowhereDiff : NowhereDifferentiabilityPackage.{u}) :
    Statement.{u} := by
  intro Omega _ P _ X hzero hincrements
  obtain ⟨Y, hmod, hcontinuous⟩ := continuous Omega P X hzero hincrements
  refine ⟨Y, hmod, ?_⟩
  exact merge_path_events hcontinuous
    (nowhereDiff Omega P X Y hzero hincrements hmod hcontinuous)

#print axioms AwesomeTheorems.Stage1.THM_M_1028.isModification_refl
#print axioms AwesomeTheorems.Stage1.THM_M_1028.isModification_symm
#print axioms AwesomeTheorems.Stage1.THM_M_1028.isModification_trans
#print axioms AwesomeTheorems.Stage1.THM_M_1028.merge_path_events
#print axioms AwesomeTheorems.Stage1.THM_M_1028.statement_of_path_packages

end AwesomeTheorems.Stage1.THM_M_1028
