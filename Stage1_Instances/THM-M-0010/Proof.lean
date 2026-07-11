import Statement

/-!
# THM-M-0010: proof of the exact Artin-Rees target

The imported `Statement` module is built in an isolated temporary directory by
`check_proof.sh`.  The proof is a checked wrapper over the pinned mathlib
Artin-Rees declaration; it does not restate or weaken the frozen target.
-/

namespace Stage1Instances.THM_M_0010.Proof

open Stage1Instances.THM_M_0010

universe u v

/-- The exact frozen Artin-Rees equality, discharged by the pinned mathlib
proof body `Ideal.exists_pow_inf_eq_pow_smul`. -/
theorem artinRees : ArtinReesTarget.{u, v} := by
  intro R _ _ I M _ _ _ N
  exact Ideal.exists_pow_inf_eq_pow_smul I N

#print axioms artinRees

end Stage1Instances.THM_M_0010.Proof
