import Mathlib.Probability.Kernel.Composition.Comp

/-!
# THM-M-1091 obligation composition harness

This module checks the exact child-to-parent composition selected before the proof phase. The
central kernel-power theorem is an explicit hypothesis here, so elaboration does not itself assign
proof credit to the audited mathlib anchor.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Set
open scoped ENNReal ProbabilityTheory

namespace Stage1Instances.THM_M_1091_Obligations

universe u

def RootTarget : Prop :=
  ∀ (State : Type u) [MeasurableSpace State]
    (κ : Kernel State State) [IsMarkovKernel κ] (m n : Nat),
      κ ^ (m + n) = (κ ^ n) ∘ₖ (κ ^ m)

def PowAddChild : Prop :=
  ∀ (State : Type u) [MeasurableSpace State]
    (κ : Kernel State State) [IsMarkovKernel κ] (a b : Nat),
      κ ^ (a + b) = (κ ^ a) ∘ₖ (κ ^ b)

/-- Exact composition certificate: use the central child at swapped indices and normalize addition. -/
theorem compose_root (pow_add_child : PowAddChild.{u}) : RootTarget.{u} := by
  intro State _ κ _ m n
  simpa only [add_comm] using pow_add_child State κ n m

/-- The zero-first-step boundary is retained in the frozen architecture. -/
theorem zero_first_boundary
    (State : Type u) [MeasurableSpace State]
    (κ : Kernel State State) [IsMarkovKernel κ] (n : Nat) :
    κ ^ (0 + n) = (κ ^ n) ∘ₖ (κ ^ 0) := by
  simpa only [zero_add, pow_zero] using (Kernel.comp_id (κ ^ n)).symm

/-- The zero-second-step boundary is retained in the frozen architecture. -/
theorem zero_second_boundary
    (State : Type u) [MeasurableSpace State]
    (κ : Kernel State State) [IsMarkovKernel κ] (m : Nat) :
    κ ^ (m + 0) = (κ ^ 0) ∘ₖ (κ ^ m) := by
  simpa only [add_zero, pow_zero] using (Kernel.id_comp (κ ^ m)).symm

#check compose_root
#print axioms compose_root
#print axioms zero_first_boundary
#print axioms zero_second_boundary

end Stage1Instances.THM_M_1091_Obligations
