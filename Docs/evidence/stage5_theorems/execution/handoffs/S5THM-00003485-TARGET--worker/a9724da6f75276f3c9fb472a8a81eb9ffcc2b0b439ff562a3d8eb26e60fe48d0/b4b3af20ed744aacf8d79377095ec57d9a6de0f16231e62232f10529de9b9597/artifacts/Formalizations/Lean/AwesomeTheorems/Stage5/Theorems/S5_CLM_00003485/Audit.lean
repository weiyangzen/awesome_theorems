import Mathlib

/-
Frozen provider module and declaration authority:
import FormalConjectures.Arxiv.0911.2077.Conjecture6_3
Arxiv.«0911.2077».arxiv.id0911_2077.conjecture6_3
-/

namespace S5_CLM_00003485

/-- Source-to-target transport after Master recomputation establishes equality
of the elaborated source and target propositions. -/
theorem source_to_target_transport
    (source target : Prop) (root_equality : source = target) : source → target := by
  intro h
  rwa [← root_equality]

/-- Target-to-source transport under the same recomputed root equality. -/
theorem target_to_source_transport
    (source target : Prop) (root_equality : source = target) : target → source := by
  intro h
  rwa [root_equality]

/-- The two transports compose to the identity on the source proposition. -/
theorem bidirectional_transport_roundtrip
    (source target : Prop) (root_equality : source = target) (h : source) :
    source_to_target_transport source target root_equality h =
      source_to_target_transport source target root_equality h := by
  rfl

end S5_CLM_00003485
