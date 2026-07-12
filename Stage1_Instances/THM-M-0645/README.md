# THM-M-0645 rev-5.6 intake

This directory is the `planned` intake dossier for Goedel's completeness theorem for classical
first-order logic. The repository gloss, "logically valid formulas are provable", selects the weak
(validity) form: every closed first-order formula true in every nonempty structure is derivable in
a sound and complete classical first-order proof calculus.

The theorem name alone does not select a concrete syntax, treatment of equality, empty-structure
convention, or deductive calculus. Those choices materially change the Lean type and remain open
for the statement phase. In particular, this dossier does not replace completeness with semantic
compactness, model-theoretic completeness of a particular theory, propositional completeness, or
an abstract predicate that assumes the desired result.

The primary-source candidates and the unresolved source decisions are recorded in the crosswalk.
The pinned mathlib tree supplies first-order syntax and semantics, but intake found no repo-local
artifact whose terminal declaration states syntactic completeness. This discovery observation is
not an anchor audit and carries no proof credit.

The provisional root vector is `[H2, M4, R4]`. The untrusted `已验证` metadata label supplies no
evidence. All downstream tasks remain open, and this dossier claims neither audit completion nor
theorem completion.
