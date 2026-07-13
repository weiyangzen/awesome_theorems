import Statement
import Mathlib.Analysis.Analytic.Uniqueness

/-!
# THM-M-1200: counterexample to the frozen target

In the pinned calculus API, `ContDiff Real top` means real analytic, not merely
smooth. An analytic function on the real plane with compact support is
identically zero. Consequently the frozen weak-defect predicate is vacuous,
even when the algebraic jump law is false.

This module refutes only the frozen Lean encoding. It does not refute the
Rankine-Hugoniot theorem with the intended smooth compactly supported tests.
-/

noncomputable section

namespace Stage1Instances.THM_M_1200.Counterexample

open Set Filter

/-- Every admissible test function in the frozen statement is zero: its
`top` differentiability order is analytic and its support is compact. -/
theorem analytic_compactSupport_eq_zero
    (phi : Real × Real → Real) (smooth : ContDiff Real ⊤ phi)
    (compact : HasCompactSupport phi) : phi = 0 := by
  have support_ne_univ : tsupport phi ≠ (univ : Set (Real × Real)) :=
    compact.ne_univ
  obtain ⟨z, hz⟩ := (ne_univ_iff_exists_notMem (tsupport phi)).mp support_ne_univ
  exact smooth.analyticOnNhd.eq_of_eventuallyEq
    analyticOnNhd_const
    (notMem_tsupport_iff_eventuallyEq.mp hz)

/-- With the frozen analytic test class, every interface defect vanishes,
regardless of the jump coefficient. -/
theorem all_interfaceDefects_vanish (f : Real → Real) (uL uR s : Real) :
    InterfaceDefectVanishes f uL uR s := by
  intro phi smooth compact
  rw [analytic_compactSupport_eq_zero phi smooth compact]
  simp [interfaceDefect]

/-- A concrete specialization refutes the exact frozen universal target. -/
theorem not_rankineHugoniotTarget : Not RankineHugoniotTarget := by
  intro target
  have jumpLaw := (target (fun _ => 0) 0 1 1).mp
    (all_interfaceDefects_vanish (fun _ => 0) 0 1 1)
  norm_num at jumpLaw

#check analytic_compactSupport_eq_zero
#check all_interfaceDefects_vanish
#check not_rankineHugoniotTarget
#print axioms analytic_compactSupport_eq_zero
#print axioms all_interfaceDefects_vanish
#print axioms not_rankineHugoniotTarget

end Stage1Instances.THM_M_1200.Counterexample
