# Proof outline

Fix an arbitrary formula `φ` and suppose that it belongs to the candidate normal modal logic `L`.

1. The claim-owned translation-closure lemma sends the membership proof `φ ∈ L` to membership of the Boxdot translation, `■φ ∈ L`.
2. Faithful interpretation, specialized at `φ`, is the equivalence `■φ ∈ L ↔ φ ∈ KT`. Its forward implication therefore sends the translated membership from step 1 to `φ ∈ KT`.
3. Since `φ` and its membership proof were arbitrary, every theorem of `L` is a theorem of `KT`; hence `L ⊆ KT`.

The formal core abstracts the source names as `contains`, `boxdot`, and `kt` so that it can be compiled from `Mathlib` without importing the sorry-backed provider. The canonical Master must independently instantiate that core against the frozen modal presentation and verify the translation-closure transport. This is the only nonlocal semantic boundary; it is not hidden as a proof oracle.
