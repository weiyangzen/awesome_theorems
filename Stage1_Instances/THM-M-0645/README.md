# THM-M-0645 rev-5.6 intake

This directory is the `planned` intake dossier for Goedel's completeness theorem for classical
first-order logic. The repository gloss, "logically valid formulas are provable", selects the weak
(validity) form: every closed first-order formula true in every nonempty structure is derivable in
a sound and complete classical first-order proof calculus.

The statement phase now fixes mathlib's first-order syntax and semantics with logical equality,
nonempty structures, sentences, and a concrete finite classical natural-deduction calculus. The
exact elaborated target and environment fingerprint are recorded in `statement.json`. In
particular, this dossier does not replace completeness with semantic
compactness, model-theoretic completeness of a particular theory, propositional completeness, or
an abstract predicate that assumes the desired result.

The primary-source candidates and the unresolved source decisions are recorded in the crosswalk.
The pinned mathlib tree supplies first-order syntax and semantics, but intake found no repo-local
artifact whose terminal declaration states syntactic completeness. This discovery observation is
not an anchor audit and carries no proof credit.

The provisional root vector remains `[H2, M4, R4]`: elaborating the statement supplies no proof
credit. The untrusted `已验证` metadata label supplies no evidence. All downstream tasks remain
open, and this dossier claims neither audit completion nor theorem completion.
