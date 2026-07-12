# THM-M-0508 rev-5.6 intake

This directory is the `planned` rev-5.6 intake for Vinogradov's three-primes theorem. The
repository claim is: "Every sufficiently large odd integer is a sum of three primes."

The intake freezes that theorem family as an eventual existence statement, while leaving the
threshold, natural-versus-integer presentation, prime conventions, and exact historical wording
to a pinpoint-source review in the statement phase. Repetition of primes is provisionally allowed,
as in the standard additive representation, but must be confirmed from the selected source.

The scope map and source-statement crosswalk separate the repository metadata from reviewed source
evidence. `IntakeProbe.lean` checks only that the pinned Lean environment exposes the elementary
APIs needed to encode the claim. It is not the canonical statement and proves no analytic-number-
theory result.

Lifecycle is `planned`; the provisional root vector is `[H1, M4, R3]`. There is no accepted proof
state, exact Lean target, audit completion, or theorem completion. Exact commands and results are
recorded in `validation.md`.
