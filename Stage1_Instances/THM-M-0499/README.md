# THM-M-0499 rev-5.6 intake

This directory is the `planned` rev-5.6 intake for de la Vallee Poussin's
classical error term in the prime number theorem. The repository source writes
the claim as

`pi(x) - Li(x) = O(x * exp(-c * sqrt(log x)))`.

The intake freezes that theorem family, including the existential positive
constant and the limit `x -> infinity`, but does not silently choose a real- or
natural-variable encoding of `pi`, a normalization of `Li`, or endpoint
conventions. Those choices require a pinpoint source and checked Lean target in
the dependent statement phase.

The scope map records the mathematical boundary, and the source-statement
crosswalk separates repository metadata from source evidence. `IntakeProbe.lean`
checks only that the pinned environment exposes the prime-counting function and
the real/asymptotic APIs needed to state a candidate. It proves no error term.

Lifecycle is `planned`; the provisional root vector is `[H1, M4, R3]`. There is
no accepted proof state, exact Lean target, audit completion, or theorem
completion. Exact commands and results are recorded in `validation.md`.
