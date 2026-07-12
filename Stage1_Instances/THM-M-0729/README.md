# THM-M-0729 rev-5.6 intake

This directory is the fail-closed `planned` dossier for the repository label "PCP theorem".
One repository inventory gives only the gloss "probabilistically checkable proofs"; a second gives
the standard shorthand `NP = PCP[O(log n), O(1)]`. The latter identifies the intended theorem
family, but it is not yet an exact proposition: neither inventory defines `NP`, the PCP verifier,
the proof oracle, the two resource bounds, completeness, soundness, or input-size conventions.

The intake freezes the intended scope and the missing choices rather than silently selecting a
textbook formulation. Standard variants differ in alphabet, adaptive versus nonadaptive queries,
perfect versus bounded completeness, constant soundness threshold, randomness accounting, and
whether resource bounds hold asymptotically or for every input. Those variants are mathematically
related but cannot be substituted without a checked source statement and transports.

`Statement.lean` now freezes one explicit standard formulation: binary verifier-based NP equals a
binary, nonadaptive oracle-checker class with eventual logarithmic randomness, a uniform constant
query bound, perfect completeness, and soundness one half. The target and mutations elaborate with
one pinned mathlib import. This moves only the proposed machine statement boundary to M3; the root
remains `[H3, M3, R4]`, because no PCP proof, primary-source pinpoint review, or readable
reconstruction is accepted. Exact statement commands and results are in `statement-validation.md`.

## Open task DAG

All dependent phases remain open in `task-dag.json`. Primary-source inspection must still check the
chosen verifier model and constants against an immutable edition before H0. This dossier supplies
no `H0`, `M0`, or `R0` credit, no audit completion, and no theorem completion.
