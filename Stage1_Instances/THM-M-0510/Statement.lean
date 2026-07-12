import Mathlib.Combinatorics.Enumerative.Partition.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-!
# THM-M-0510: exact Hardy-Ramanujan asymptotic statement

This module freezes the ordinary-partition asymptotic statement only. It does
not contain a proof of the Hardy-Ramanujan theorem.
-/

noncomputable section

open Filter Asymptotics

namespace Stage1Instances.THM_M_0510

/-- The ordinary partition function, coerced to the reals. `Nat.Partition n`
consists of unordered positive parts whose sum is `n`. -/
def partitionCount (n : Nat) : Real :=
  Fintype.card (Nat.Partition n)

/-- The full Hardy-Ramanujan leading term, including its constant factor. -/
def hardyRamanujanMainTerm (n : Nat) : Real :=
  Real.exp (Real.pi * Real.sqrt (2 * (n : Real) / 3)) /
    (4 * (n : Real) * Real.sqrt 3)

/-- The exact selected target: the ordinary partition count is asymptotic to
the Hardy-Ramanujan leading term along natural numbers tending to infinity. -/
def HardyRamanujanAsymptoticTarget : Prop :=
  IsEquivalent atTop partitionCount hardyRamanujanMainTerm

/-- Direct expansion of the selected encoding. -/
def ExpandedTarget : Prop :=
  IsEquivalent atTop
    (fun n : Nat => (Fintype.card (Nat.Partition n) : Real))
    (fun n : Nat =>
      Real.exp (Real.pi * Real.sqrt (2 * (n : Real) / 3)) /
        (4 * (n : Real) * Real.sqrt 3))

/-- The named target is definitionally identical to its direct expansion. -/
theorem target_iff_expandedTarget :
    HardyRamanujanAsymptoticTarget ↔ ExpandedTarget :=
  Iff.rfl

-- Separately elaborated, deliberately non-identical statement mutations.

/-- Removes the ordinary partition count and retains only exponential growth. -/
def mutationRemovedPartitionCount : Prop :=
  IsEquivalent atTop
    (fun n : Nat => Real.log (partitionCount n))
    (fun n : Nat => Real.pi * Real.sqrt (2 * (n : Real) / 3))

/-- Changes the asymptotic index domain from naturals to integers. -/
def mutationChangedDomain : Prop :=
  IsEquivalent atTop
    (fun n : Int => partitionCount n.natAbs)
    (fun n : Int => hardyRamanujanMainTerm n.natAbs)

/-- Moves the varying index under a pointwise equality binder, replacing the
limit statement by an equality at every natural number. -/
def mutationChangedBinderScope : Prop :=
  ∀ n : Nat, partitionCount n = hardyRamanujanMainTerm n

/-- Excludes zero by changing the filter to the principal positive set. -/
def mutationBoundaryPositiveOnly : Prop :=
  IsEquivalent (Filter.principal {n : Nat | 0 < n})
    partitionCount hardyRamanujanMainTerm

/-- Lean's totalized division makes the selected comparison term zero at the
boundary `n = 0`; the asymptotic target itself retains all naturals. -/
theorem mainTerm_at_zero : hardyRamanujanMainTerm 0 = 0 := by
  simp [hardyRamanujanMainTerm]

end Stage1Instances.THM_M_0510

set_option pp.explicit true in
#print Stage1Instances.THM_M_0510.HardyRamanujanAsymptoticTarget
