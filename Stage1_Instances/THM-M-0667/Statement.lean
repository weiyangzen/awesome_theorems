import Mathlib.Computability.Ackermann

/-!
# THM-M-0667: exact Ackermann non-definability statement

This module freezes the statement boundary only. The imported pinned mathlib
module contains proof infrastructure, but this file does not claim or wrap its
root proof as proof-phase evidence.
-/

namespace Stage1Instances.THM_M_0667

open Nat

/-- The canonical target: the standard two-variable Ackermann-Peter function
is not a binary primitive recursive function. -/
def AckermannNondefinabilityTarget : Prop :=
  ¬Primrec₂ ack

/-- Direct expansion of the selected mathlib encoding. -/
def ExpandedTarget : Prop :=
  ¬Primrec (fun p : Nat × Nat => ack p.1 p.2)

/-- Checked transport from `Primrec₂` to primitive recursiveness of the
uncurried function. -/
theorem ackermannNondefinabilityTarget_iff_expandedTarget :
    AckermannNondefinabilityTarget ↔ ExpandedTarget := by
  exact not_congr Primrec₂.uncurry.symm

/-- Checked transport to mathlib's unary pairing representation. -/
theorem ackermannNondefinabilityTarget_iff_unpairedNat :
    AckermannNondefinabilityTarget ↔ ¬Nat.Primrec (Nat.unpaired ack) := by
  exact not_congr Primrec₂.unpaired'.symm

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationDiagonalOnly : Prop :=
  ¬Primrec (fun n : Nat => ack n n)

def mutationGeneralRecursiveInstead : Prop :=
  ¬Computable₂ ack

def mutationSwappedArguments : Prop :=
  ¬Primrec₂ (fun m n : Nat => ack n m)

def mutationRemovedNegation : Prop :=
  Primrec₂ ack

/-- The selected `ack` includes the zero-level boundary equation. -/
theorem zero_level_boundary (n : Nat) : ack 0 n = n + 1 := by
  simp

/-- The selected `ack` includes the successor/zero boundary equation. -/
theorem successor_zero_boundary (m : Nat) : ack (m + 1) 0 = ack m 1 := by
  simp

/-- The selected `ack` has the frozen nested successor recursion. -/
theorem successor_successor_boundary (m n : Nat) :
    ack (m + 1) (n + 1) = ack m (ack (m + 1) n) := by
  simp

end Stage1Instances.THM_M_0667

set_option pp.explicit true in
#print Stage1Instances.THM_M_0667.AckermannNondefinabilityTarget
