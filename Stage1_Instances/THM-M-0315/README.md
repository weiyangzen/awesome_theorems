# THM-M-0315 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Fredholm alternative. The
repository source gives only the gloss "solvability of compact-operator equations", an attribution
to Erik Fredholm, the year 1903, and an untrusted `已验证` label. It does not state the operator
equation, domains, hypotheses, or conclusion.

Standard presentations called the Fredholm alternative are related but not literally identical.
They include a spectral alternative for a compact endomorphism, equivalence between injectivity and
surjectivity of an identity-minus-compact operator, and a Hilbert-space solvability criterion using
the kernel of an adjoint. Selecting one without an inspected source would substitute a proposition.

Pinned mathlib contains
`IsCompactOperator.hasEigenvalue_or_mem_resolventSet`, explicitly documented as the Fredholm
alternative. The intake probe verifies that this declaration and its supporting APIs are available;
it does not identify it with the underspecified repository gloss or credit its proof. The root
therefore remains `[H1, M4, R4]`. Exact commands and results are recorded in `validation.md`.
