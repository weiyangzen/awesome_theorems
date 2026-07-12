# THM-M-0729 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "PCP theorem".
One repository inventory gives only the gloss "probabilistically checkable proofs"; a second gives
the standard shorthand `NP = PCP[O(log n), O(1)]`. The latter identifies the intended theorem
family, but it is not yet an exact proposition: neither inventory defines `NP`, the PCP verifier,
the proof oracle, the two resource bounds, completeness, soundness, or input-size conventions.

The intake freezes the intended scope and the missing choices rather than silently selecting a
textbook formulation. Standard variants differ in alphabet, adaptive versus nonadaptive queries,
perfect versus bounded completeness, constant soundness threshold, randomness accounting, and
whether resource bounds hold asymptotically or for every input. Those variants are mathematically
related but cannot be substituted without a checked source statement and transports.

The root remains `[H3, M4, R4]`: repository metadata locates a known theorem but provides no
pinpoint primary statement, no exact Lean target is selected, and no readable reconstruction is
accepted. A pinned Lean probe confirms only that mathlib exposes languages, deterministic
polynomial-time computation, probability mass functions, and asymptotic bounds that could support
a later encoding. It is not a PCP definition or proof. Exact commands and results are recorded in
`validation.md`.

## Open task DAG

All dependent phases remain open in `task-dag.json`. The first blocker is independent inspection
of an immutable primary statement and referenced definitions, fixing the verifier model, oracle
encoding, resource measures, thresholds, ordered quantifiers, and equality of language classes.
This intake supplies no `H0`, `M0`, or `R0` credit, no audit completion, and no theorem completion.
