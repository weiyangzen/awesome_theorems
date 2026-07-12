import Mathlib.Analysis.Fourier.LpSpace

/-!
# THM-M-0342: Plancherel statement

This module freezes the norm-isometry formulation for complex-valued `L2` functions on finite-
dimensional real Euclidean spaces. It contains no proof of the target.
-/

open MeasureTheory
open scoped FourierTransform ENNReal

namespace Stage1Instances.THM_M_0342

abbrev Domain (n : Nat) := EuclideanSpace Real (Fin n)

/-- The exact Plancherel target, stated for representatives of complex `L2` classes. -/
def PlancherelTarget : Prop :=
  forall (n : Nat) (f : Domain n -> Complex),
    forall hf : MemLp f 2 (volume : Measure (Domain n)),
      ‖𝓕 (hf.toLp f)‖ = ‖hf.toLp f‖

def mutationRemovedHypothesis : Prop :=
  forall (n : Nat) (f : Domain n -> Complex),
    ‖f 0‖ = ‖f 0‖

def mutationChangedDomain : Prop :=
  forall (f : Real -> Complex),
    forall hf : MemLp f 2 (volume : Measure Real),
      ‖𝓕 (hf.toLp f)‖ = ‖hf.toLp f‖

def mutationChangedBinderScope : Prop :=
  forall n : Nat,
    exists f : Domain n -> Complex,
      forall hf : MemLp f 2 (volume : Measure (Domain n)),
        ‖𝓕 (hf.toLp f)‖ = ‖hf.toLp f‖

def mutationExcludesBoundary : Prop :=
  forall (n : Nat) (_hn : 0 < n) (f : Domain n -> Complex),
    forall hf : MemLp f 2 (volume : Measure (Domain n)),
      ‖𝓕 (hf.toLp f)‖ = ‖hf.toLp f‖

end Stage1Instances.THM_M_0342

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0342.PlancherelTarget
