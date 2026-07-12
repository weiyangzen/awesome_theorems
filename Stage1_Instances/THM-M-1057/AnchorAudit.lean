import Mathlib.Analysis.Subadditive
import Mathlib.Dynamics.Ergodic.Function
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
Pinned-mathlib anchor checks for the statement in `Statement.lean`.

These wrappers establish only two supporting branches: deterministic Fekete
convergence for normalized expectations and ergodic constancy of an already
constructed invariant limit.  They do not establish pointwise convergence.
-/

noncomputable section

open Filter Function MeasureTheory Set
open scoped MeasureTheory Topology

namespace Stage1Instances.THM_M_1057.AnchorAudit

universe u

theorem deterministic_fekete_candidate {a : Nat -> Real}
    (hsub : Subadditive a) (hbdd : BddBelow (range fun n => a n / (n : Real))) :
    Tendsto (fun n => a n / (n : Real)) atTop (nhds (Subadditive.lim hsub)) :=
  hsub.tendsto_lim hbdd

theorem iterate_measure_preserving_candidate
    {Omega : Type u} [MeasurableSpace Omega] {mu : Measure Omega}
    {T : Omega -> Omega} (hT : Ergodic T mu) (n : Nat) :
    MeasurePreserving (T^[n]) mu mu :=
  hT.1.iterate n

theorem ergodic_constancy_candidate
    {Omega : Type u} [MeasurableSpace Omega] {mu : Measure Omega}
    {T : Omega -> Omega} (hT : Ergodic T mu) {g : Omega -> Real}
    (hgm : AEStronglyMeasurable g mu) (hinv : g ∘ T =ᵐ[mu] g) :
    exists c : Real, g =ᵐ[mu] const Omega c :=
  hT.ae_eq_const_of_ae_eq_comp_ae hgm hinv

#check Subadditive.tendsto_lim
#check MeasureTheory.MeasurePreserving.iterate
#check Ergodic.ae_eq_const_of_ae_eq_comp_ae
#print axioms deterministic_fekete_candidate
#print axioms iterate_measure_preserving_candidate
#print axioms ergodic_constancy_candidate

end Stage1Instances.THM_M_1057.AnchorAudit
