# THM-M-0778 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository gloss "a consistent
formal system cannot prove its own consistency," attributed to Kurt Godel and dated 1931. That
gloss identifies Godel's second incompleteness theorem, but it does not determine an exact theorem:
the theory, proof calculus, arithmetized provability predicate, consistency sentence, strength and
effectivity assumptions, and metatheory are all unspecified.

The intended direction is provisionally `Con(T) -> not Provable_T(Con(T))`. This is not valid for
every consistent formal system. The statement phase must select a source-faithful class of theories
strong enough to represent syntax and satisfying explicit derivability conditions, and must fix
whether consistency is the sentence `not Provable_T(false)` or a source-proved equivalent.

The root remains `[H1, M4, R4]`. A narrow pinned Lean probe checks only generic first-order theory
and Godel beta-function coding APIs; it does not define arithmetized provability or prove the second
incompleteness theorem. Exact commands and remaining gates are recorded in `validation.md`.
