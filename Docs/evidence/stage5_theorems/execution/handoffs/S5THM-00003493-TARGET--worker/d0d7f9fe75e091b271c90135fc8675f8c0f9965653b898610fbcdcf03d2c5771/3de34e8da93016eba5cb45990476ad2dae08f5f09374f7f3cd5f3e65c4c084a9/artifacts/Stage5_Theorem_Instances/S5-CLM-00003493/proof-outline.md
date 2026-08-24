# Proof outline

1. Bind the goal to `type_of% Arxiv.«1609.08688».maximalLength_le_isBigO`; this references the frozen declaration only for its type.
2. Choose `Ω n = -(Real.iteratedLog n : ℝ)`. The statement does not require `Ω` to be nonnegative.
3. Reflexive Big-O followed by right negation proves `iteratedLog =O[atTop] Ω`, because real norm is invariant under negation.
4. Cast the earlier sorry-free theorem `Arxiv.«1609.08688».maximalLength_le n` to obtain `maximalLength n ≤ n²` in `ℝ`.
5. Since `iteratedLog n` is natural-valued, its real coercion is nonnegative, so `exp (-iteratedLog n) ≤ 1`; positivity of `exp` and `n²` then gives `n² ≤ n² / exp (-iteratedLog n)`.
6. Compose these facts into the existential root and expose a reverse theorem at the same exact frozen type.

The target provider theorem’s sorry-backed body is never invoked. Canonical Master must still compile the exact files under the pinned provider route and recompute the elaborated root, dependency census, and terminal axiom report.
