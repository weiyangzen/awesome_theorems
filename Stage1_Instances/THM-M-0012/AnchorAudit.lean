import Mathlib.Analysis.Complex.Polynomial.Basic

/-!
# THM-M-0012 anchor-audit probes

This file checks the exact pinned mathlib candidate against a literal copy of the frozen target.
The wrapper is candidate evidence for the anchor-audit node, not an accepted proof-phase or
theorem-completion declaration.
-/

namespace Stage1Instances.THM_M_0012_AnchorAudit

open Polynomial

def Nonconstant (f : Polynomial Complex) : Prop :=
  Not (exists c : Complex, f = C c)

def ExactTarget : Prop :=
  forall f : Polynomial Complex, Nonconstant f ->
    exists z : Complex, IsRoot f z

/-- Exact adapter from the frozen nonconstancy formulation to the pinned mathlib theorem. -/
theorem exactTarget_mathlib_candidate : ExactTarget := by
  intro f hf
  apply Complex.exists_root
  rw [← not_le]
  intro hdegree
  exact hf ⟨coeff f 0, eq_C_of_degree_le_zero hdegree⟩

#check Complex.exists_root
#check Complex.isAlgClosed
#check IsAlgClosed.exists_root
#print Complex.exists_root
#print Complex.isAlgClosed
#print axioms Complex.exists_root
#print axioms Complex.isAlgClosed
#print axioms IsAlgClosed.exists_root
#print axioms exactTarget_mathlib_candidate

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0012_AnchorAudit
