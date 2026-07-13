# THM-M-0620 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0620`, Tychonoff's theorem.
The repository gives the gloss `任意多个紧空间的乘积紧` (the product of arbitrarily many
compact spaces is compact), attributes it to Andrey Tychonoff in 1930, and labels it `已验证`.
Those uncited fields identify the theorem family but do not establish exact source fidelity or
machine proof credit.

Crossref and the Springer bibliographic page identify A. Tychonoff's 1930 article *Uber die
topologische Erweiterung von Raumen*, *Mathematische Annalen* 102, 544-561, DOI
`10.1007/BF01782364`. A Goettingen IIIF scan and OCR of the article were then inspected. Section 2,
starting on printed page 548, proves compactness of an arbitrary-cardinality power of a closed
interval as infrastructure for the article's embedding theorems; it does not present an
unambiguous clean source row for the received general compact-space product wording. Exact source
genealogy, definitions, assumptions, corrections, and independent review remain open, so this is
an `H1` lead rather than `H0` evidence.

Pinned mathlib contains three direct candidates in `Mathlib.Topology.Compactness.Compact`:
`isCompact_pi_infinite`, `isCompact_univ_pi`, and `Pi.compactSpace`. `IntakeProbe.lean` authenticates
their exposed types, selected empty-product and empty-factor boundaries, and their reported axioms.
The candidates distinguish products of compact subsets from the space-level product statement and
use mathlib's Pi product topology. Choosing one exact encoding and checking transports belong to
the statement phase, not intake.

The provisional vector is `[H1, M3, R4]`. A direct pinned formal interface exists, but the canonical
statement, exact wrapper, source mapping, and all acceptance gates remain open. `instance.json` is
the structured scope authority and `task-dag.json` leaves all six dependent phases open. No H0,
accepted M0, R0, proof state, audit completion, theorem completion, or master acceptance is claimed.
