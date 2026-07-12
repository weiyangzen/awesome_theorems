# THM-M-1421 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Pesin entropy formula. The
repository supplies only the name, Yakov Pesin, the year 1977, and the gloss "entropy and Lyapunov
exponents." Its `已验证` label is untrusted metadata and provides no source or machine-proof credit.

The leading primary-source candidate is Ya. B. Pesin's 1977 survey *Characteristic Lyapunov
Exponents and Smooth Ergodic Theory*. Section 5, Theorem 5.1 gives an entropy equality for a
measure-preserving `C^2` diffeomorphism of a compact smooth Riemannian manifold under the paper's
standing smooth-measure convention. That candidate is not yet the canonical claim. Its printed
formula uses negative forward characteristic exponents, while the introduction gives a
positive-exponent formulation; modern statements also vary the differentiability, invariant
measure, ergodicity, multiplicity, entropy, and almost-everywhere conventions. Selecting one form
without a complete definition-chain, sign transport, errata check, and independent source review
would silently change the target.

The intake therefore freezes the source boundary and proposition-changing decisions while leaving
the canonical mathematical and Lean statements null. The provisional root vector is
`[H1, M4, R3]`: a pinpoint primary candidate is identified but not accepted as an exact source
crosswalk, no usable exact Lean artifact is located, and only a route/boundary explanation exists.
`IntakeProbe.lean` checks adjacent pinned APIs for measure preservation, topological entropy,
manifold derivatives, integration, and finite sums. In particular, topological entropy is not the
Kolmogorov-Sinai entropy required by the likely formula; the probe states no target theorem.

All downstream phases remain open in `task-dag.json`. Exact commands and results are recorded in
`validation.md` and the provisional worker receipt. No H0, M0, R0, accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
