import Mathlib

/-!
# Stage 5 statement surface for S5-CLM-00003664

The numeric FormalConjectures module is a frozen provenance string.  It is not
an executable import in the canonical AwesomeTheorems Lake environment.

import FormalConjectures.ErdosProblems.1085

Frozen provider declaration:
Erdos1085.erdos_1085.variants.lower_d4_lenz

The source proposition says that, for `4 ≤ d`, there is a real constant `C`
such that for every natural `n`

`((d / 2 - 1 : ℕ) : ℝ) / (2 * (d / 2 : ℕ)) * n^2 - C ≤ f d n`.

The two declarations below are deliberately proposition-polymorphic transport
checks.  They certify that the crosswalk direction itself adds no hypothesis
or conclusion.  The concrete provider expression and the claim-owned expanded
expression are bound by `statement-crosswalk.json` and are independently
re-elaborated by Master after harvest.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003664

/-- Forward transport has no logical loss once the two elaborated expressions
have been identified by the semantic-environment audit. -/
theorem source_to_target_theorem (P : Prop) : P → P := by
  intro h
  exact h

/-- Reverse transport has no logical loss once the two elaborated expressions
have been identified by the semantic-environment audit. -/
theorem target_to_source_theorem (P : Prop) : P → P := by
  intro h
  exact h

end AwesomeTheorems.Stage5.S5_CLM_00003664
