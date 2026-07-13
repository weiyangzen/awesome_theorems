# THM-M-0080 rev-5.6 intake

`THM-M-0080` is the group-theory catalog item named the Kurosh subgroup theorem. The repository
glosses it only as `自由积的子群结构` ("the structure of subgroups of free products"), attributes
it to Alexander Kurosh in 1934, and supplies an untrusted `verified` label.

## Intake result

This directory is a fail-closed `planned` dossier. The gloss identifies the classical theorem
family, but it is not an exact proposition. A familiar formulation decomposes a subgroup of an
indexed free product into a free group and conjugates of subgroups of the original factors. The
catalog does not fix the indexed family, embeddings, conjugation convention, representative sets,
trivial-factor policy, free factor, uniqueness scope, or boundary cases. Selecting a textbook
variant here would add mathematics absent from the repository record.

Kurosch's 1934 paper *Die Untergruppen der freien Produkte von beliebigen Gruppen* was inspected in
the Göttingen Digitization Centre scan. Its `Untergruppensatz` on printed page 651 gives an exact
existential headline: if `G` is the free product of component subgroups, every subgroup `F` of `G`
can be decomposed as a free product whose factors are either infinite cyclic or conjugate to a
subgroup of one component. The source does not put a double-coset indexing or uniqueness clause in
that headline. The scan and OCR are hashed and pinpointed in the crosswalk, but a complete
definition/proof-node map, translation review, correction audit, and independent mathematical
review remain open. The human-source classification is therefore `H1`, not `H0`.

## Formal boundary

`IntakeProbe.lean` elaborates pinned `Monoid.CoprodI`, its factor embeddings and reduced-word API,
the free-product universal property, subgroup interfaces, and the theorem that a free product of
free groups is free. These are substantive `M3` statement and dependency interfaces. The bounded
search found no Kurosh declaration; mathlib's `docs/1000.yaml` contains only the unlinked title.
Neither the probe nor the title is a proof of the subgroup decomposition.

The source-identified human candidate is recorded provisionally, while the canonical Lean
expression remains null. The vector is `[H1, M3, R4]`, and all six downstream tasks remain open.
No accepted execution state, master-frozen exact statement, proof, audit completion, theorem
completion, or master acceptance is claimed.
