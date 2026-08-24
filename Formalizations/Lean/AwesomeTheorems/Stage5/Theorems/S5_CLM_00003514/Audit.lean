import Mathlib

/-!
Frozen provenance required for Master recomputation:

```lean
import FormalConjectures.Arxiv.2602.05192.FirstProof4
#check Arxiv.«2602.05192».four
```

This audit file is intentionally independent and Mathlib-only.  Master must
substitute the elaborated claim-owned proposition for `P` and independently
compare it with `Arxiv.«2602.05192».four`'s right-hand side.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003514

theorem audit_source_to_target
    (P : Prop) (h : True ↔ P) : P := by
  exact h.mp trivial

theorem audit_target_to_source
    (P : Prop) (h : P) : True ↔ P := by
  constructor
  · intro _
    exact h
  · intro _
    trivial

theorem audit_round_trip
    (P : Prop) (h : P) : (True ↔ P) ∧ P := by
  constructor
  · exact audit_target_to_source P h
  · exact h

end AwesomeTheorems.Stage5.S5_CLM_00003514
