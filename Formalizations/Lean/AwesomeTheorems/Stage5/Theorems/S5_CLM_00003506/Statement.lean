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

/--
The provider's `answer(False) ↔ P` surface is propositionally identical to
the claim-owned negative formulation `¬ P`.  Here `P` is the complete
right-hand side of the frozen `conjecture_1_4` record; making it an explicit
parameter keeps this normalization independent of provider definitions and
of the provider theorem body.
-/
theorem answer_false_statement (P : Prop) : (False ↔ P) ↔ ¬ P := by
  constructor
  · intro h hP
    exact h.mpr hP
  · intro h
    constructor
    · intro hFalse
      exact False.elim hFalse
    · intro hP
      exact h hP

end AwesomeTheorems.Stage5.S5_CLM_00003506
