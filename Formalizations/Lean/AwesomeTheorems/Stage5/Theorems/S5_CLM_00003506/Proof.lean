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

/-- The forward half of the independently checked answer normalization. -/
theorem answer_false_to_negation (P : Prop) (h : False ↔ P) : ¬ P := by
  intro hP
  exact h.mpr hP

/-- The reverse half of the independently checked answer normalization. -/
theorem negation_to_answer_false (P : Prop) (h : ¬ P) : False ↔ P := by
  constructor
  · intro hFalse
    exact False.elim hFalse
  · intro hP
    exact h hP

/--
Claim-owned proof of the logical root used to transport the frozen
`answer(False)` statement to its ordinary mathematical negation.  No result
from the Formal Conjectures provider is referenced by the proof term.
-/
theorem conjecture_1_4_claim_owned_root (P : Prop) : (False ↔ P) ↔ ¬ P := by
  constructor
  · exact answer_false_to_negation P
  · exact negation_to_answer_false P

end AwesomeTheorems.Stage5.S5_CLM_00003506
