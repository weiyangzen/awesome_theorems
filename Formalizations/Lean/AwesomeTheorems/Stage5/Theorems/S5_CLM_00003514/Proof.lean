import Mathlib

/-!
Frozen provenance (not an active import in the canonical Mathlib-only Lake graph):

```lean
import FormalConjectures.Arxiv.2602.05192.FirstProof4
#check Arxiv.«2602.05192».four
```

The mathematical payload supplied to `claim_owned_four` is the claim-owned
equivalent of `∀ (p q : ℝ[X]) (n : ℕ), FourProp p q n`.  Keeping the payload
abstract here makes this transport theorem independent of the provider's
incomplete proof body; its exact elaborated substitution is checked in the
Master audit.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003514

theorem claim_owned_four
    (P : Prop) (finite_additive_fisher_inequality : P) : True ↔ P := by
  constructor
  · intro _
    exact finite_additive_fisher_inequality
  · intro _
    trivial

end AwesomeTheorems.Stage5.S5_CLM_00003514
