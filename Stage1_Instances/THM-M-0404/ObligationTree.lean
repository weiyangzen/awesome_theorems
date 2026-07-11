import Statement

/-!
# THM-M-0404 conditional obligation composition

This module checks the final composition boundary selected by the frozen
architecture.  Both substantive premises remain explicit; no
Skolem-Mahler-Lech proof is asserted here.
-/

namespace Stage1Instances.THM_M_0404

universe u

/-- Eventual periodicity of a predicate on natural numbers. -/
def IsEventuallyPeriodic (S : Nat -> Prop) : Prop :=
  exists N period : Nat, 0 < period /\
    forall n : Nat, N <= n -> (S (n + period) <-> S n)

/-- The recurrence-specific output of the spectral, torsion, and
nondegenerate-zero packages. -/
def EventuallyPeriodicZeroSets : Prop :=
  forall (K : Type u) [Field K] [CharZero K]
    (E : LinearRecurrence K) (sequence : Nat -> K),
      E.IsSolution sequence ->
        IsEventuallyPeriodic (fun n : Nat => sequence n = 0)

/-- The predicate-level combinatorial conversion kept separate from the
number-theoretic recurrence argument. -/
def EventualPeriodicToFiniteUnion : Prop :=
  forall S : Nat -> Prop,
    IsEventuallyPeriodic S -> IsFiniteUnionOfArithmeticProgressions S

/-- Checked conditional composition into the exact canonical root. -/
theorem root_of_eventualPeriodic_packages
    (periodicZeros : EventuallyPeriodicZeroSets.{u})
    (finiteUnion : EventualPeriodicToFiniteUnion) :
    SkolemMahlerLechTarget.{u} := by
  intro K _field _charZero E sequence hsolution
  exact finiteUnion (fun n : Nat => sequence n = 0)
    (periodicZeros K E sequence hsolution)

#print axioms root_of_eventualPeriodic_packages

end Stage1Instances.THM_M_0404
