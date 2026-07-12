import Statement

/-!
# THM-M-1129 proof execution

This module contains local proof bodies for degenerate branches of the frozen
Poisson-kernel construction.  It deliberately does not declare the exact
root: the analytic representation and uniqueness obligations remain open.
-/

namespace Stage1.THM_M_1129

/-- At time zero the disk term vanishes because its outer factor is zero.
This is a kernel-level boundary fact used by the initial-data branches. -/
theorem poissonDiskTerm_zero_time (c : Real) (h : Plane -> Real) (x : Plane) :
    poissonDiskTerm c 0 h x = 0 := by
  simp [poissonDiskTerm]

/-- Zero Cauchy data contribute no velocity term at any time. -/
theorem poissonDiskTerm_zero_data (c t : Real) (x : Plane) :
    poissonDiskTerm c t (fun _ => 0) x = 0 := by
  simp [poissonDiskTerm]

/-- The differentiated displacement term also vanishes for zero data. -/
theorem deriv_poissonDiskTerm_zero_data (c t : Real) (x : Plane) :
    deriv (fun s => poissonDiskTerm c s (fun _ => 0) x) t = 0 := by
  simp [poissonDiskTerm]

/-- Both terms in the represented expression vanish for zero Cauchy data.
This closes the algebraic zero-data sub-branch, but does not assert uniqueness
of a wave solution with zero data. -/
theorem poissonExpression_zero_data (c t : Real) (x : Plane) :
    deriv (fun s => poissonDiskTerm c s (fun _ => 0) x) t +
        poissonDiskTerm c t (fun _ => 0) x = 0 := by
  rw [deriv_poissonDiskTerm_zero_data, poissonDiskTerm_zero_data, add_zero]

#print axioms poissonDiskTerm_zero_time
#print axioms poissonDiskTerm_zero_data
#print axioms deriv_poissonDiskTerm_zero_data
#print axioms poissonExpression_zero_data

end Stage1.THM_M_1129
