# Proof outline

1. Freeze the meaning of `monotonicSubsequenceSums`: an output is the sum of `x` over a finite set of indices where `x` is monotone or antitone.
2. Freeze the meaning of `admissibleConstants`: `c` belongs to it exactly when, for every positive error, all sufficiently large lengths and every injective real sequence admit such a subsequence sum above the normalized `(c - ε)` bound.
3. Bind the target to the pinned source proposition `IsGreatest Erdos1026.admissibleConstants 1`. As an `IsGreatest` statement, this records both `1 ∈ admissibleConstants` and the upper-bound assertion that every admissible constant is at most `1`.
4. Check bidirectional identity transport. The source-to-target and target-to-source functions both return their hypothesis unchanged, so they cannot alter hypotheses, the output, constants, coercions, or binders.
5. Compose the two transports into the audited root. Lean checks this composition at trust zero. The canonical Master remains responsible for recomputing the pinned provider declaration and accepting the final integrated package.

Exceptional case: the provider declaration body is sorry-backed and is not treated as independent proof authority. That boundary is explicit in every evidence layer.
