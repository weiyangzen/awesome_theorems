import ObligationTree
import Mathlib.Data.Nat.Periodic

/-!
# THM-M-0404 proof-phase bodies

This module closes the predicate-level combinatorial package.  The
number-theoretic eventual-periodicity package remains an explicit premise: no
proof of Skolem-Mahler-Lech itself is claimed here.
-/

namespace Stage1Instances.THM_M_0404

/-- An eventually periodic predicate is a finite exceptional set together with
one progression for each true residue in its periodic tail. -/
theorem eventualPeriodic_to_finiteUnion (S : Nat -> Prop) :
    IsEventuallyPeriodic S -> IsFiniteUnionOfArithmeticProgressions S := by
  rintro ⟨N, period, period_pos, periodic⟩
  classical
  let tail : Nat -> Prop := fun k => S (N + k)
  have tail_periodic : Function.Periodic tail period := by
    intro k
    apply propext
    simpa [tail, Nat.add_assoc] using
      periodic (N + k) (Nat.le_add_right N k)
  refine ⟨(List.range N).filter S,
    (List.range period).filter tail |>.map (fun r => (N + r, period)), ?_⟩
  intro n
  by_cases before : n < N
  · constructor
    · intro hn
      exact Or.inl (by simp [before, hn])
    · rintro (hexception | hprogression)
      · exact of_decide_eq_true (List.mem_filter.mp hexception).2
      · rcases hprogression with ⟨p, hp, k, rfl⟩
        rcases List.mem_map.mp hp with ⟨r, _hr, rfl⟩
        omega
  · have N_le_n : N <= n := Nat.le_of_not_gt before
    let k := n - N
    have N_add_k : N + k = n := Nat.add_sub_of_le N_le_n
    have residue_lt : k % period < period := Nat.mod_lt k period_pos
    have tail_residue : tail (k % period) <-> S n := by
      have hresidue := tail_periodic.map_mod_nat k
      change S (N + k % period) = S (N + k) at hresidue
      change S (N + k % period) <-> S n
      rw [hresidue, N_add_k]
    constructor
    · intro hn
      right
      refine ⟨(N + k % period, period), ?_, ?_⟩
      · apply List.mem_map.mpr
        refine ⟨k % period, ?_, rfl⟩
        simp [residue_lt, tail, tail_residue.mpr hn]
      · refine ⟨k / period, ?_⟩
        change n = N + k % period + period * (k / period)
        rw [<- N_add_k, Nat.add_assoc, Nat.mod_add_div]
    · rintro (hexception | hprogression)
      · have : n < N := List.mem_range.mp (List.mem_filter.mp hexception).1
        omega
      · rcases hprogression with ⟨p, hp, q, rfl⟩
        rcases List.mem_map.mp hp with ⟨r, hr, rfl⟩
        have htail : tail r := of_decide_eq_true (List.mem_filter.mp hr).2
        have r_lt : r < period := List.mem_range.mp (List.mem_filter.mp hr).1
        have hperiods := tail_periodic.nsmul q
        simpa [tail, Nat.nsmul_eq_mul, Nat.mul_comm, Nat.add_assoc] using
          (hperiods r).mpr htail

/-- Closed proof body for the frozen combinatorial package proposition. -/
theorem eventualPeriodicToFiniteUnion_proof : EventualPeriodicToFiniteUnion :=
  eventualPeriodic_to_finiteUnion

/-- Updated root composition uses the local combinatorial proof body and keeps
only the number-theoretic Skolem-Mahler-Lech package as a premise. -/
theorem root_of_eventuallyPeriodicZeroSets
    (periodicZeros : EventuallyPeriodicZeroSets.{u}) :
    SkolemMahlerLechTarget.{u} :=
  root_of_eventualPeriodic_packages periodicZeros
    eventualPeriodicToFiniteUnion_proof

#print axioms eventualPeriodic_to_finiteUnion
#print axioms root_of_eventuallyPeriodicZeroSets

end Stage1Instances.THM_M_0404
