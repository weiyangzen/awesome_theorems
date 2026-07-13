# THM-M-0231 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the
Mittag-Leffler theorem. The repository supplies only the gloss "partial-fraction decomposition of
meromorphic functions," attributes it to Magnus Mittag-Leffler in 1884, and labels it verified.
Under rev-5.6 that label is untrusted inventory metadata, not a source audit, an exact proposition,
or proof evidence.

The gloss identifies the classical complex-analysis theorem family but does not state either of its
common directions precisely. It could mean existence of a meromorphic function with prescribed
principal parts on a discrete set, or decomposition of a given meromorphic function into its
principal parts plus a holomorphic remainder. It fixes neither the domain nor its connectedness,
the pole-set and local-finiteness conditions, the representation of principal parts, the required
convergence, nor any uniqueness boundary. Intake therefore leaves the canonical statement and Lean
target null instead of supplying those proposition-changing choices from memory.

The original 1884 Acta Mathematica article and David Ullrich's 2008 textbook chapter were located
as bibliographic leads. Metadata and the AMS table of contents were inspected, but no exact theorem
text, incorporated definitions, assumption crosswalk, errata audit, or independent review was
accepted. They remain discovery leads rather than `H0` evidence.

Pinned mathlib supplies meromorphic predicates, orders and finite divisors, finite-support
factorized rational functions, and the concrete cotangent Mittag-Leffler expansion.
`IntakeProbe.lean` authenticates these APIs. The cotangent formula is one example, not the arbitrary
prescribed-principal-parts theorem, while the category-theory declaration with the same name is
unrelated. A bounded search found no exact analytic theorem in the pinned tree.

The provisional vector is `[H1, M4, R3]`: the classical theorem family is historically established,
but no exact source proposition is accepted; no usable exact formal artifact is credited; and this
scope/blocker account is not a readable proof reconstruction. `instance.json` is the structured
scope authority, and `task-dag.json` keeps all six downstream phases open. No H0, M0, R0, accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
