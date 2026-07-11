import Mathlib.Algebra.LinearRecurrence

/-!
# THM-M-0404: exact Skolem-Mahler-Lech statement

This module freezes and tests the statement boundary only. It contains no proof
of the Skolem-Mahler-Lech theorem.
-/

namespace Stage1Instances.THM_M_0404

universe u

/-- The one-sided natural arithmetic progression starting at `start` with the
given step. A zero step denotes a singleton. -/
def NatArithmeticProgression (start step n : Nat) : Prop :=
  ∃ k : Nat, n = start + step * k

/-- Membership in one of a finite list of natural arithmetic progressions. -/
def CoveredByProgressions (progressions : List (Nat × Nat)) (n : Nat) : Prop :=
  ∃ p : Nat × Nat, p ∈ progressions ∧ NatArithmeticProgression p.1 p.2 n

/-- A predicate on naturals is a finite exceptional set together with finitely
many one-sided arithmetic progressions. -/
def IsFiniteUnionOfArithmeticProgressions (S : Nat → Prop) : Prop :=
  ∃ exceptions : List Nat, ∃ progressions : List (Nat × Nat),
    ∀ n : Nat, S n ↔ n ∈ exceptions ∨ CoveredByProgressions progressions n

/-- The exact target selected at intake for Skolem-Mahler-Lech. -/
def SkolemMahlerLechTarget : Prop :=
  ∀ (K : Type u) [Field K] [CharZero K]
    (E : LinearRecurrence K) (sequence : Nat → K),
      E.IsSolution sequence →
        IsFiniteUnionOfArithmeticProgressions (fun n : Nat => sequence n = 0)

/-- Direct expansion of the historical candidate statement. -/
def PinnedCandidateSourceShape : Prop :=
  ∀ (K : Type u) [Field K] [CharZero K]
    (E : LinearRecurrence K) (sequence : Nat → K),
      E.IsSolution sequence →
        ∃ exceptions : List Nat, ∃ progressions : List (Nat × Nat),
          ∀ n : Nat, sequence n = 0 ↔
            n ∈ exceptions ∨
              ∃ p : Nat × Nat, p ∈ progressions ∧
                ∃ k : Nat, n = p.1 + p.2 * k

/-- Checked identity with the direct expansion of the historical candidate. -/
theorem skolemMahlerLechTarget_iff_pinnedCandidateSourceShape :
    SkolemMahlerLechTarget.{u} ↔ PinnedCandidateSourceShape.{u} :=
  by
    simp only [SkolemMahlerLechTarget, PinnedCandidateSourceShape,
      IsFiniteUnionOfArithmeticProgressions, CoveredByProgressions,
      NatArithmeticProgression]

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedCharZero : Prop :=
  ∀ (K : Type u) [Field K]
    (E : LinearRecurrence K) (sequence : Nat → K),
      E.IsSolution sequence →
        IsFiniteUnionOfArithmeticProgressions (fun n : Nat => sequence n = 0)

def mutationChangedCoefficientDomain : Prop :=
  ∀ (E : LinearRecurrence Rat) (sequence : Nat → Rat),
    E.IsSolution sequence →
      IsFiniteUnionOfArithmeticProgressions (fun n : Nat => sequence n = 0)

def mutationChangedBinderScope : Prop :=
  ∀ (K : Type u) [Field K] [CharZero K] (E : LinearRecurrence K),
    (∀ sequence : Nat → K, E.IsSolution sequence) →
      ∀ sequence : Nat → K,
        IsFiniteUnionOfArithmeticProgressions (fun n : Nat => sequence n = 0)

def mutationPositiveStepsOnly : Prop :=
  ∀ (K : Type u) [Field K] [CharZero K]
    (E : LinearRecurrence K) (sequence : Nat → K),
      E.IsSolution sequence →
        ∃ exceptions : List Nat, ∃ progressions : List (Nat × Nat),
          (∀ p ∈ progressions, 0 < p.2) ∧
          ∀ n : Nat, sequence n = 0 ↔
            n ∈ exceptions ∨ CoveredByProgressions progressions n

/-- The empty predicate exercises empty exception and progression lists. -/
theorem empty_boundary :
    IsFiniteUnionOfArithmeticProgressions (fun _n : Nat => False) := by
  exact ⟨[], [], by simp [CoveredByProgressions]⟩

/-- A zero-step progression is admitted and denotes its starting singleton. -/
theorem zero_step_boundary (start n : Nat) :
    NatArithmeticProgression start 0 n ↔ n = start := by
  simp [NatArithmeticProgression]

/-- The universal predicate is represented by the progression `(0, 1)`. -/
theorem universal_boundary :
    IsFiniteUnionOfArithmeticProgressions (fun _n : Nat => True) := by
  refine ⟨[], [(0, 1)], ?_⟩
  intro n
  simp [CoveredByProgressions, NatArithmeticProgression]

end Stage1Instances.THM_M_0404

set_option pp.explicit true in
#print Stage1Instances.THM_M_0404.SkolemMahlerLechTarget
