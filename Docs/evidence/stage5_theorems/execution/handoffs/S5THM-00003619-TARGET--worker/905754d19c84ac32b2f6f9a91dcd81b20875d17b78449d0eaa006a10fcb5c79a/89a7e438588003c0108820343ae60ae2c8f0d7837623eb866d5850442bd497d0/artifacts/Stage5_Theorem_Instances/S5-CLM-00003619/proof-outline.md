# Proof outline

## Statement and inputs

`a : ℕ → ℤ` is strictly increasing. There is a real constant `C > 0` such
that every successor satisfies `a (n + 1) ≥ C * (a n)^2` after coercion to
the reals. The output is the irrationality of `Erdos1051.ErdosSeries a`.

## Semantic binding

The source and target use the same binders, coercions, exponent, inequality,
and `ErdosSeries` declaration. The two transports are identity maps on the
elaborated conclusion; the exact provider module is imported, and no local
declaration shadows a source surface symbol.

## Closure step

The rapid-growth inputs are supplied to the pinned rapid-growth declaration.
Its result has exactly the target conclusion, so no rewriting, weakened
hypothesis, changed index convention, or substituted series is involved.

## Output and trust boundary

The audit file independently elaborates the root and the reverse identity
transport. The worker records trust-zero cold replay and empty human, machine,
and readability cut sets; only the canonical Master may accept the candidate.
