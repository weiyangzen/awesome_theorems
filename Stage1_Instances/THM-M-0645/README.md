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
The completed formal-candidate inventory is recorded in `anchor-audit.json` and
`anchor-audit.md`. Pinned mathlib supplies first-order syntax and semantics but no terminal
syntactic completeness theorem. FormalizedFormalLogic/Foundation has a substantive external Lean 4
proof at an immutable revision; it remains anchor-only because its calculus and dependencies differ
and it is neither integrated nor transported to the exact target.

The provisional root vector remains `[H2, M4, R4]`: neither statement elaboration nor an
anchor-only external proof supplies proof credit. The untrusted `已验证` metadata label supplies no
evidence. The anchor-audit node is self-tested pending master acceptance, all later tasks remain
open, and this dossier claims no theorem completion.
