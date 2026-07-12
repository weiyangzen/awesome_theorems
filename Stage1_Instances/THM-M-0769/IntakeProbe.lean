import Mathlib.Logic.Basic

#check Classical.choice
#check Classical.axiomOfChoice

-- Candidate encoding of the repository's indexed-family gloss. This is an API
-- probe only; the statement phase must freeze and mutation-test the target.
#check fun (ι : Sort*) (A : ι → Sort*) =>
  (∀ i, Nonempty (A i)) → Nonempty (∀ i, A i)
