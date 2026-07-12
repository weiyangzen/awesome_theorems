# THM-M-0508 rev-5.6 statement

This directory is the `planned` rev-5.6 intake for Vinogradov's three-primes theorem. The
repository claim is: "Every sufficiently large odd integer is a sum of three primes."

The statement phase freezes this repository claim over naturals with one uniform threshold,
`Odd n`, three `Nat.Prime` witnesses, no distinctness premise, and equality `n = p + q + r`.
`Statement.lean` also checks an equivalent `Filter.atTop` presentation. Exact historical wording
and any stronger asymptotic source theorem remain for pinpoint-source review.

The scope map and source-statement crosswalk separate repository metadata from reviewed source
evidence. `IntakeProbe.lean` remains API discovery only. `check_statement.py` re-elaborates the
canonical target and ensures removed-hypothesis, changed-domain, changed-binder-scope, and boundary
mutations serialize differently.

Lifecycle remains `planned`; the root vector remains `[H1, M4, R3]`. The exact Lean statement is
self-tested pending master acceptance, but there is no accepted proof state, source H0, audit
completion, or theorem completion. Statement commands and results are in `statement-validation.md`.

The obligation-tree phase freezes a 17-node ternary circle-method architecture with separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. The finite-count
existence bridge and conditional root composition elaborate in `ObligationTree.lean`; the Fourier,
major-arc, singular-series, and minor-arc leaves remain explicitly open at M4. This architecture
receipt does not change the lifecycle or root vector and remains pending master acceptance.
