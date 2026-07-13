# THM-M-0914 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the pigeonhole principle. The
repository gives the literal claim "placing `n + 1` objects into `n` boxes puts at least two
objects in one box," attributes it to Peter Dirichlet in 1834, and labels it `已验证`. The label
is untrusted inventory metadata and supplies neither a source audit nor machine-proof credit.

The claim identifies a standard finite theorem family, but the catalog does not define a
placement as a total function, select `Fin (n + 1)` and `Fin n` or arbitrary finite types, state
the collision as distinct objects with equal images or as a fiber of cardinality at least two, or
settle `n = 0`. These choices are mathematically compatible only after explicit transports. The
intake records them instead of silently choosing a canonical proposition for the dependent
statement phase.

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

Pinned mathlib contains `Fintype.exists_ne_map_eq_of_card_lt`, whose documentation calls it the
finite pigeonhole principle and whose conclusion gives two distinct inputs with equal images.
`IntakeProbe.lean` authenticates that declaration and adjacent cardinality APIs. This is a strong
exact-family candidate, but intake does not select the canonical expression, check the
`Fin (n + 1)` specialization, audit the proof body, or grant `M0` credit.

The provisional vector is `[H1, M3, R4]`: a modern complete source statement and a proof-bearing
pinned exact-family candidate are known, but exact source fidelity and Lean root identity remain
open, and no reviewed proof reconstruction exists. `instance.json` is the structured scope
authority and `task-dag.json` keeps all six downstream phases open. No exact Lean statement, H0,
M0, R0, accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
