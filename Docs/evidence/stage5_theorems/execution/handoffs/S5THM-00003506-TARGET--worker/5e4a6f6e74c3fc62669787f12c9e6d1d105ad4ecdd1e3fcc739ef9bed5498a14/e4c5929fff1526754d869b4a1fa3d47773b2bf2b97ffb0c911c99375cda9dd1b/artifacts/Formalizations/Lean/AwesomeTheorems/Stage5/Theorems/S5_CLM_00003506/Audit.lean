/-
Frozen Formal Conjectures provenance (comment only; the numeric component is
not a module that the canonical Mathlib Lake environment may import):
import FormalConjectures.Arxiv.2303.01089.FurstenbergTimesPTimesQ
Arxiv.id2303_01089.conjecture_1_4
Provider revision: 2270d31e8dd611521f979de6d86da364930b7669
Provider file SHA-256: 78abd479faa4a2d45d67847da856460835be8beaf1406a10e71021b5133322b1
-/

import Mathlib

namespace AwesomeTheorems.Stage5.S5_CLM_00003506

/-- Audited source-surface to claim-owned negative transport. -/
theorem source_to_target_theorem (P : Prop) : (False ↔ P) → ¬ P := by
  intro h hP
  exact h.mpr hP

/-- Audited claim-owned negative to source-surface transport. -/
theorem target_to_source_theorem (P : Prop) : ¬ P → (False ↔ P) := by
  intro h
  constructor
  · intro hFalse
    exact False.elim hFalse
  · intro hP
    exact h hP

/-- Exact bidirectional audit root, independently reconstructed. -/
theorem audit_exact_root (P : Prop) : (False ↔ P) ↔ ¬ P := by
  constructor
  · exact source_to_target_theorem P
  · exact target_to_source_theorem P

end AwesomeTheorems.Stage5.S5_CLM_00003506
