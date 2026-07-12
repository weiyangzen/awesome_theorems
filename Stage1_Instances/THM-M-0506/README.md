# THM-M-0506 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Tauberian
theorem". The source inventory supplies only the gloss "the relationship between convergence and
summability", an attribution to Alfred Tauber, and the year 1897. It does not state a proposition.

The date and attribution suggest Tauber's original converse to Abel's theorem, but "Tauberian
theorem" also names a large family of non-equivalent results. Even the original result requires the
source to fix the summability method, scalar field, indexing convention, side from which the Abel
parameter approaches one, and the exact side condition on the coefficients. Choosing these from
the title alone would substitute invented mathematics for the repository target.

The intake therefore freezes the ambiguity and the exclusions rather than a canonical theorem.
The root remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib supplies `HasSum`, the
partial-sum limit interface, and Abel's limit theorem for real and complex power series. These are
encoding and comparison ingredients only, not evidence for a Tauberian converse. Exact commands
and results are recorded in `validation.md`.
