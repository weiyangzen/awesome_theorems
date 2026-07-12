# THM-M-0343 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Poisson summation formula.
The repository source gives only the gloss "the relationship between Fourier series and the
Fourier transform" and does not specify a formula, Fourier-transform normalization, function
class, convergence hypotheses, lattice, or evaluation point.

Pinned mathlib contains a directly relevant formal family headed by
`Real.tsum_eq_tsum_fourier`. This is strong evidence that a faithful Lean target is feasible, but
intake does not silently identify that particular general theorem, either of its decay corollaries,
or its Schwartz-space specialization with the underspecified repository gloss. The statement phase
must select a sourced version and check its normalization and hypotheses.

The root remains `[H3, M4, R4]`: the human-source proposition is not pinpointed, the canonical Lean
expression is not frozen, and no reconstruction is accepted. `IntakeProbe.lean` only checks that the
pinned candidate declarations elaborate. Exact validation commands and boundaries are recorded in
`validation.md`.
