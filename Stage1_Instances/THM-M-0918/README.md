# THM-M-0918 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Rogers-Ramanujan identities.
The repository catalog supplies only the gloss "an identity of the partition function," attributes
the item jointly to Leonard Rogers and Srinivasa Ramanujan, dates it to 1894, and labels it
`verified`. Under rev-5.6 that label is untrusted metadata and supplies no source or proof credit.

The conventional name denotes a pair, and it has materially different analytic q-series and
restricted-partition forms. The catalog does not say whether the root is the first identity, the
second, their conjunction, or a checked equivalence between both analytic and combinatorial pairs.
It also fixes no convergence domain, product convention, partition representation, restriction
predicate, ordered binders, or boundary cases. Selecting one familiar formula at intake would
silently invent missing mathematics.

NIST DLMF sections 17.2(vi) and 26.10(iv) were inspected as authoritative modern statement leads.
They display both analytic identities and both combinatorial equivalents, but they are not the
catalog's cited source, do not by themselves supply the historical proof boundary, and have not
received independent source review here. Crossref identifies an original Rogers paper, while its
1893 publication metadata conflicts with the catalog's 1894 date; the publisher text was not
accessible in this run. No source is credited as `H0`.

The provisional root vector is `[H1, M4, R4]`. `IntakeProbe.lean` checks adjacent pinned mathlib
interfaces for partitions, restricted counts, power series, sums, and products. A bounded search
found no Rogers-Ramanujan or q-Pochhammer declaration. Those are discovery facts only, not an
anchor audit or proof. The canonical statement and Lean expression remain null, and all six
downstream phases remain open. No accepted state, audit completion, theorem completion, or master
acceptance is claimed.
