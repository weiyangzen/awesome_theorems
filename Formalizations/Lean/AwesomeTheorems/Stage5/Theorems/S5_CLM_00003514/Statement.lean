import Mathlib

/-!
Frozen provenance (the numeric provider module is deliberately retained as text):

```lean
import FormalConjectures.Arxiv.2602.05192.FirstProof4
#check Arxiv.«2602.05192».four
```

The provider declaration has type
`answer(True) ↔ ∀ (p q : ℝ[X]) (n : ℕ), FourProp p q n`.
The claim-owned surface below isolates the proposition at the right of that
question-answer wrapper.  It introduces no semantic definition or notation.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003514

theorem source_to_target_statement
    (P : Prop) (h : True ↔ P) : P := by
  exact h.mp trivial

theorem target_to_source_statement
    (P : Prop) (h : P) : True ↔ P := by
  constructor
  · intro _
    exact h
  · intro _
    trivial

end AwesomeTheorems.Stage5.S5_CLM_00003514
