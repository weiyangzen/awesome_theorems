# THM-M-0921 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry `卡塔兰数`
(Catalan numbers). The complete repository gloss is `多种组合问题的计数` (counting in many
combinatorial problems), attributed to Eugene Catalan in 1838 and marked `已验证`. These fields
identify a famous sequence and a broad enumeration family, not one truth-valued proposition with
ordered binders, hypotheses, and a conclusion. The verified label is untrusted metadata and gives
no source or proof credit.

The gloss could lead to the recursive definition of the sequence, its binomial closed form, its
generating-function equation, or an enumeration theorem for binary trees, Dyck words, lattice
paths, polygon triangulations, parenthesizations, or another Catalan family. Those claims are not
interchangeable. Selecting one familiar identity, or conjoining several convenient identities,
would invent mathematics that the catalog does not specify.

Richard Stanley's author-hosted *Catalan Addendum* was inspected as an authoritative subject-family
lead. It fixes the conventional formula for `C_n` and explicitly continues a long list of distinct
combinatorial interpretations. That source demonstrates rather than resolves the catalog's phrase
"many combinatorial problems": the catalog cites no edition, interpretation, theorem, or proof.
The addendum is therefore a source lead only, not `H0` evidence.

Pinned mathlib has unusually strong adjacent material. `IntakeProbe.lean` checks the recursive
`catalan` sequence, its central-binomial formula and recurrence, a binary-tree cardinality theorem,
a Dyck-word cardinality theorem, and the generating-series equation. These checked declarations
have real proof bodies in pinned mathlib, but none is credited as *the* root because no source-
selected root or approved multi-root package exists yet.

The provisional catalog-target vector is `[H5, M4, R4]`. `H5` says the received family wording is
not yet a stable proposition; it does not refute standard Catalan-number theorems. `M4` applies to
the unidentified exact root, not to the adjacent mathlib declarations. All six downstream phases
remain open. No exact statement, accepted execution state, audit completion, theorem completion,
or master acceptance is claimed.
