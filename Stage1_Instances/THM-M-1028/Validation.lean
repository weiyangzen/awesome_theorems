import ObligationTree

/-!
# Independent validation probes for THM-M-1028

This module deliberately does not import `Proof`.  It reconstructs the local
modification algebra, event intersection, and conditional root composition.
The two substantive Wiener path packages remain explicit inputs.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Set Filter

namespace AwesomeTheorems.Stage1.THM_M_1028.Validation

universe u

theorem modification_refl {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) (X : RealProcess Omega) :
    IsModification X X P := fun _ => ae_of_all P fun _ => rfl

theorem modification_symm {Omega : Type u} [MeasurableSpace Omega]
    {P : Measure Omega} {X Y : RealProcess Omega}
    (h : IsModification X Y P) : IsModification Y X P :=
  fun t => (h t).mono fun _ hxy => hxy.symm

theorem modification_trans {Omega : Type u} [MeasurableSpace Omega]
    {P : Measure Omega} {X Y Z : RealProcess Omega}
    (hXY : IsModification X Y P) (hYZ : IsModification Y Z P) :
    IsModification X Z P :=
  fun t => (hXY t).and (hYZ t) |>.mono fun _ h => h.1.trans h.2

theorem intersect_path_events {Omega : Type u} [MeasurableSpace Omega]
    {P : Measure Omega} {Y : RealProcess Omega}
    (hc : ∀ᵐ omega ∂P, ContinuousOn (fun t => Y t omega) (Ici (0 : Real)))
    (hn : ∀ᵐ omega ∂P,
      NowhereDifferentiableOnNonnegative (fun t => Y t omega)) :
    ∀ᵐ omega ∂P,
      ContinuousOn (fun t => Y t omega) (Ici (0 : Real)) /\
        NowhereDifferentiableOnNonnegative (fun t => Y t omega) :=
  hc.and hn

theorem independent_statement_of_packages
    (continuous : ContinuousModificationPackage.{u})
    (nowhereDiff : NowhereDifferentiabilityPackage.{u}) :
    Statement.{u} := fun Omega _ P _ X hzero hincrements => by
  rcases continuous Omega P X hzero hincrements with ⟨Y, hXY, hc⟩
  exact ⟨Y, hXY, intersect_path_events hc
    (nowhereDiff Omega P X Y hzero hincrements hXY hc)⟩

#print axioms AwesomeTheorems.Stage1.THM_M_1028.Validation.modification_refl
#print axioms AwesomeTheorems.Stage1.THM_M_1028.Validation.modification_symm
#print axioms AwesomeTheorems.Stage1.THM_M_1028.Validation.modification_trans
#print axioms AwesomeTheorems.Stage1.THM_M_1028.Validation.intersect_path_events
#print axioms AwesomeTheorems.Stage1.THM_M_1028.Validation.independent_statement_of_packages

end AwesomeTheorems.Stage1.THM_M_1028.Validation
