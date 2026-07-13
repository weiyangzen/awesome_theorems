# THM-M-0914 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the pigeonhole principle. The
repository gives the literal claim "placing `n + 1` objects into `n` boxes puts at least two
objects in one box," attributes it to Peter Dirichlet in 1834, and labels it `已验证`. The label
is untrusted inventory metadata and supplies neither a source audit nor machine-proof credit.

The statement phase now freezes the literal concrete encoding: a placement is a total function
`f : Fin (n + 1) -> Fin n`, and the conclusion supplies distinct `x` and `y` with equal images.
This preserves exactly the catalog's object and box counts instead of broadening the root to
arbitrary finite types. The `n = 0` case remains included and is vacuous because no total function
`Fin 1 -> Fin 0` exists; a separate kernel check covers the first inhabited `n = 1` case.

An authoritative modern source lead, Lehman, Leighton, and Meyer's *Mathematics for Computer
Science* (2018), states the principle both in the catalog's objects-and-holes language and as a
finite-cardinality total-function rule. It directly supports the intended family. The catalog does
not cite this text, and no independently reviewed source admission, historical Dirichlet passage,
correction audit, or exact source-to-catalog transport is present, so the source status is `H1`,
not `H0`.

The catalog's history also needs correction review. Rittaud and Heeffer's 2014 history article is
titled "The Pigeonhole Principle, Two Centuries Before Dirichlet," and its public reference
metadata points to Dirichlet passages from 1842 and 1863, not 1834. Only bibliographic/reference
metadata was accessible and inspected, not the paywalled article or those primary passages. This
is a provenance warning, not a replacement source or H credit.

`Statement.lean` elaborates the canonical proposition with the pinned Lean 4.29.0 executable and
an empty direct-import set: Lean's Init prelude already supplies all selected `Fin` vocabulary.
It also kernel-checks an iff to the explicit shared-box encoding, distinguishes all four required
structural mutations, and checks the zero- and one-box boundaries. Pinned mathlib's
`Fintype.exists_ne_map_eq_of_card_lt` remains a downstream proof candidate only; it is not imported,
invoked, audited, or credited by this phase.

The provisional vector remains `[H1, M3, R4]`: the exact Lean root is now self-tested, but the
modern source has not passed independent H0 admission, no target proof body is credited, and no
reviewed proof reconstruction exists. `instance.json` is the structured scope authority and
`task-dag.json` remains open pending master acceptance and every downstream phase. No H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
