# Full study — maximal length of 2-increasing triples

## Frozen statement and source

The target asks for a function `Ω : ℕ → ℝ` such that the real-valued iterated logarithm is `O(Ω)` at `atTop` and `maximalLength n ≤ n² / exp (Ω n)` for every natural `n`. The exact authority is `Arxiv.«1609.08688».maximalLength_le_isBigO`, lines 229–233 of the pinned Formal Conjectures module. Its provider body contains `sorry`, so this package uses it only through `type_of%`.

## Independent proof

Take `Ω n = -iteratedLog n`. Big-O uses norms, so changing only the sign of the comparison function preserves the reflexive estimate. The pointwise inequality follows from the earlier provider theorem `maximalLength_le`, whose source body is explicit and sorry-free: after casting from naturals to reals it gives `maximalLength n ≤ n²`. Here `Real.iteratedLog n` is natural-valued and then coerced to `ℝ`; that cast is nonnegative, hence `exp (-iteratedLog n) ≤ 1`, and dividing the nonnegative square by this positive number can only increase it.

This witness exploits the literal quantifiers of the frozen declaration: no lower bound or eventual positivity requirement is imposed on `Ω`. Nothing is assumed about the target theorem’s provider proof.

## Composition, exceptional cases, and trust

The proof DAG records statement binding, witness choice, the Big-O step, the universal pointwise bound, root composition, and reverse transport. The cases `n = 0` and `n = 1` require no special branch because `maximalLength_le` is universal and natural-to-real casts are always nonnegative. No local definition, alias, notation, macro, coercion, or import replacement reinterprets a source symbol.

The worker performs only the mandated no-Lean semantic/evidence preflight. Canonical Master alone authenticates the provider-native toolchain, elaborates the exact local body at trust zero, recomputes the root expression and transitive constants, checks the terminal axiom report, runs cold replay and semantic-substitution mutations, and decides acceptance.
